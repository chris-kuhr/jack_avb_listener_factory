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
    def __init__(self, argv, ipaddress='127.0.0.1', port=5678):
        print("setup websocket server")    
    

        self.params = utils.read_params()
        self.serList = []

        # Create the message queue.
        self.mq = posix_ipc.MessageQueue(self.params["MESSAGE_QUEUE_NAME"], posix_ipc.O_CREX)
        
        
        # Create the shared memory and the semaphore.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"], posix_ipc.O_CREX, size=self.params["SHM_SIZE"])
        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)
        
        
        self.semaphore = 0
        while self.semaphore == 0:
            try:
                self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME1"], posix_ipc.O_CREX)
            except posix_ipc.ExistentialError:
                pass
        self.semaphore.release()
            
            
        self.semaphore_mq_gui = 0
        while self.semaphore_mq_gui == 0:
            try:
                self.semaphore_mq_gui = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME2"], posix_ipc.O_CREX)  
            except posix_ipc.ExistentialError:
                pass  
        self.semaphore_mq_gui.release()
             
             

        

        
        
        
        self.avdeccctl = AVDECC_Controller(argv, "ens2f1", cmd_path ="/home/soundjack/OpenAvnu.git.kuhr/avdecc-lib/controller/app/cmdline/avdecccmdline")
        #self.avdeccctl = AVDECC_Controller(argv, "enp1s0", cmd_path ="/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline")
        self.avdeccctl.start()
        
        self.semaphore_mq_wrapper = 0
        while self.semaphore_mq_wrapper == 0:
            try:
                self.semaphore_mq_wrapper = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME3"])
            except posix_ipc.ExistentialError:
                pass
        self.semaphore_mq_wrapper.release()
                
        self.running = False
        
        self.listeners = []
        self.talkers = []
        
        
        #for i in range(0,4):        
        #    self.talkers.append( AVDECCEntity(i+1, "test%d"%(i+1),"talker") )
        #    self.listeners.append( AVDECCEntity(i+1, "test%d"%(i+1),"listener") )
              
            
        
        print("start websocket server", self.avdeccctl)
        self.start_server = websockets.serve(self.websocketLoop, ipaddress, port)

    #-------------------------------------------------------------------------------------------------------------------------
    def waitForMsg(self, recv_msg):
        msg_dec = ""
        while recv_msg not in msg_dec:
            print("waiting for %s"%recv_msg)
            msg, _ = self.mq.receive()
            msg_dec = msg.decode()
            

        return    
    #-------------------------------------------------------------------------------------------------------------------------

    
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
        
        self.listeners = []
        self.talkers = []
        
        self.mq.send("discover")
        self.waitForMsg("ack")    
        if self.readList():
            await self.updateAVBEntityList()
        
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
                if self.readList():
                    await self.updateAVBEntityList()
                    
                pass
    #-------------------------------------------------------------------------------------------------------------------------
  
    async def newEndpoint(self, ws, key, msg_dec):
        newEndpoint = AVDECCEntity(0,"","")
        if msg_dec[key][0]["EPType"] == "talker":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.talkers)+1)
            newEndpoint.execDomain = "h"
            self.talkers.append(newEndpoint)
            await self.discovered(ws, self.talkers[-1])
        if msg_dec[key][0]["EPType"] == "listener":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.listener)+1)
            newEndpoint.execDomain = "h"
            self.listener.append(newEndpoint)        
            await self.discovered(ws, self.listener[-1])
            
    
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
  
    def readList(self):
        self.semaphore.acquire()
        serStr = utils.read_from_memory(self.mapfile)
        self.semaphore.release()
        
        #
        #
        #   create List from JSON object
        #
        #
        
        serList = deserializeStr2List(serStr)

        if len(self.serList) != len(serList):
            self.serList = serList
        
            return True
        return False
    #-------------------------------------------------------------------------------------------------------------------------
        

    async def updateAVBEntityList(self):
        for device in self.serList: 
            print("ws_server: ", device) 
            entity = AVDECCEntity(0, "","")  
            print("endpointtype", entity.endpointType)
            
            if entity.decodeString(device) > 0:
                print("endpointtype", entity.endpointType)
                if "talker" in entity.endpointType: 
                    entity.idx = len(self.talkers)+1
                    entity.execDomain = "n"
                    self.talkers.append(entity)
                    await self.discovered(ws, self.talkers[-1])
                elif "listener" in entity.endpointType: 
                    entity.idx = len(self.listeners)+1 
                    entity.execDomain = "n"   
                    self.listeners.append(entity)
                    await self.discovered(ws, self.listeners[-1])
                print("endpointtype", entity.endpointType)
            else:
                break
            
            print("endpointtype", entity.endpointType)            
        
        print("List lengths: ", len(self.listeners), len(self.talkers))
    #-------------------------------------------------------------------------------------------------------------------------
     
    
  
    async def discovered(self, ws, endpointObj): 
        await ws.send( json.dumps( {"discovered":[endpointObj.getJSONprepObject()]} ) )
    #-------------------------------------------------------------------------------------------------------------------------
        
#=======================================================================================================================
      


