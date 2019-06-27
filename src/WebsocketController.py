#!/usr/bin/env python3
import asyncio
import datetime
import random
import websockets
import json

import mmap
import os
import time


import posix_ipc
import ipc_utils as utils

from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List
from avdecccmdlineWrapper import AVDECC_Controller


class WebsocketController():
    def __init__(self, ipaddress='127.0.0.1', port=5678):
        print("setup websocket server")    
    

        self.params = utils.read_params()

        # Create the shared memory and the semaphore.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"], posix_ipc.O_CREX, size=self.params["SHM_SIZE"])
        self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME1"], posix_ipc.O_CREX)
        self.semaphore_mq_gui = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME2"], posix_ipc.O_CREX)
        self.semaphore_mq_wrapper = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME3"], posix_ipc.O_CREX)

        # Create the message queue.
        self.mq = posix_ipc.MessageQueue(self.params["MESSAGE_QUEUE_NAME"], posix_ipc.O_CREX)
        
        
        #self.avdeccctl = AVDECC_Controller("enp1s0", cmd_path ="/home/christoph/source_code/github-kuhr/OpenAvnu.git/avdecc-lib/controller/app/cmdline/avdecccmdline")
        self.avdeccctl = AVDECC_Controller("enp1s0", cmd_path ="opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline")
        self.avdeccctl.start()
        
        self.running = False
        
        self.listeners = []
        self.talkers = []
        
        self.mq.send("discover")
        self.waitForACK()    
        self.updateAVBEntityList()
        
        for i in range(0,4):        
            self.talkers.append( AVDECCEntity(i+1, "test%d"%(i+1),"talker") )
            self.listeners.append( AVDECCEntity(i+1, "test%d"%(i+1),"listener") )
              
            
        print("start websocket server", self.avdeccctl)
        self.start_server = websockets.serve(self.websocketLoop, ipaddress, port)

    #-------------------------------------------------------------------------------------------------------------------------
    def waitForACK(self):
        msg_dec = ""
        while "ack" not in msg_dec:
            print("waiting for msg")
            msg, _ = self.mq.receive()
            msg_dec = msg.decode()

        return    #-------------------------------------------------------------------------------------------------------------------------

    
    async def recvCatcher(self, ws):    
        msg = None
        try:
            msg = await ws.recv()
            
        except websockets.exceptions.ConnectionClosed:    
            pass
        
        return msg
    #-------------------------------------------------------------------------------------------------------------------------
          
  
    async def websocketLoop(self, ws, path):
    
        self.running = True        
        
        for l in self.listeners:
            await self.discovered(ws, l)
            
        for t in self.talkers:
            await self.discovered(ws, t)
        
        while(self.running):
            '''
            Wait for Websockets Messages from crossmatrix.js
            '''
            try:  
                msg = await asyncio.wait_for(self.recvCatcher(ws), 10)
                
                msg_dec = None
                            
                try:
                    msg_dec = json.loads(msg)
                except:
                    continue
                    
                print(msg_dec)
                
                for key in msg_dec:   
                    print(key, msg_dec[key])         
                    if key == "Quit":
                        self.running = False
                        
                        '''
                            Write config file on exit!!!
                        '''
                        
                        
                        
                         
                        break          
                    elif key == "newEndpoint":
                        await self.newEndpoint(ws, key, msg_dec)              
                    elif key == "reqListener":
                        await self.reqListener(ws, key, msg_dec)
                    elif key == "reqTalker":
                        await self.reqTalker(ws, key, msg_dec)
                    elif key == "connect":
                        await self.connect(ws, key, msg_dec)
                    elif key == "disconnect":
                        await self.disconnect(ws, key, msg_dec)
                              
            except asyncio.TimeoutError:    
                '''
                Talk to AVDECC Wrapper
                '''
               
                #await self.discovered(ws, None)
                pass
    #-------------------------------------------------------------------------------------------------------------------------
  
    async def newEndpoint(self, ws, key, msg_dec):
        newEndpoint = AVDECCEntity(0,"","")
        if msg_dec[key][0]["EPType"] == "talker":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.talkers)+1)
            self.talkers.append(newEndpoint)
        if msg_dec[key][0]["EPType"] == "listener":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.listener)+1)
            self.listener.append(newEndpoint)
            

        await self.discovered(ws, newEndpoint )
    
    #-------------------------------------------------------------------------------------------------------------------------  
  
    async def reqListener(self, ws, key, msg_dec):
        for listener in self.listeners:
            if listener.idx == int(msg_dec[key]):
                await ws.send( json.dumps( {"respListener":[listener.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
  
  
    async def reqTalker(self, ws, key, msg_dec):
        for talker in self.talkers:
            if talker.idx == int(msg_dec[key]):
                await ws.send( json.dumps( {"respTalker":[talker.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
  
  
    async def connect(self, ws, key, msg_dec):
        talkerErrorString = "talker not found! ";
        foundTalker = None
        for talker in self.talkers:
            if talker.name == msg_dec[key][0]["talker"]:
                foundTalker = talker
                talkerErrorString = "O"
        
        listenerErrorString = "listener not found! ";
        foundListener = None        
        for listener in self.listeners:
            if listener.name == msg_dec[key][0]["listener"]:
                foundListener = listener
                listenerErrorString = "K"
                
        status = {"status":talkerErrorString+listenerErrorString}
        
        if foundListener is None or foundTalker is None:
            await ws.send( json.dumps( {"connected":[status]} ) )
        else:                            
            await ws.send( json.dumps( {"connected":[status, foundTalker.getJSONprepObject(),foundListener.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
  
  
    async def disconnect(self, ws, key, msg_dec): 
        talkerErrorString = "talker not found! ";
        foundTalker = None
        for talker in self.talkers:
            if talker.name == msg_dec[key][0]["talker"]:
                foundTalker = talker
                talkerErrorString = "O"
        
        listenerErrorString = "listener not found! ";
        foundListener = None        
        for listener in self.listeners:
            if listener.name == msg_dec[key][0]["listener"]:
                foundListener = listener
                listenerErrorString = "K"
                
        status = {"status":talkerErrorString+listenerErrorString}
        
        if foundListener is None or foundTalker is None:
            await ws.send( json.dumps( {"disconnected":[status]} ) )
        else:                            
            await ws.send( json.dumps( {"disconnected":[status, foundTalker.getJSONprepObject(),foundListener.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
  
  
    async def discovered(self, ws, endpointObj): 
        if endpointObj is None:
            self.talkers.append( AVDECCEntity(len(self.talkers)+1, "discovered%d"%(len(self.talkers)+1),"talker") )
            await ws.send( json.dumps( {"discovered":[self.talkers[-1].getJSONprepObject()]} ) )
        else:
            await ws.send( json.dumps( {"discovered":[endpointObj.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
        
    def updateAVBEntityList(self):
        self.semaphore.acquire()
        serStr = utils.read_from_memory(self.mapfile)
        self.semaphore.release()

        #
        #
        #   create List from JSON object
        #
        #
        
        serList = deserializeStr2List(serStr)

        for device in serList:    
            entity = AVDECCEntity()  
            if entity.decodeString(device) > 0: # return values -1, 1
                if "t" in entity.endpointType:               
                    self.talkers.append(entity)
                if "l" in entity.endpointType:     
                    self.listeners.append(entity)
            else:
                break
    #-------------------------------------------------------------------------------------------------------------------------
     
    
#=======================================================================================================================
      


