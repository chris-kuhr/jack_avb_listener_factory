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
    
        self.avdeccctl = AVDECC_Controller(cmd_path ="/home/christoph/source_code/github-kuhr/OpenAvnu.git/avdecc-lib/controller/app/cmdline/avdecccmdline")
        #self.avdeccctl.start()

        self.params = utils.read_params()

        # Create the shared memory and the semaphore.
        #self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"])
        #self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME"])

        # MMap the shared memory
        #self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)

        #self.semaphore.release()
        
        
        self.running = False
        
        self.listeners = []
        self.talkers = []
        
        for i in range(0,4):        
            self.talkers.append( AVDECCEntity(i+1, "test%d"%(i+1),"talker") )
            self.listeners.append( AVDECCEntity(i+1, "test%d"%(i+1),"listener") )
                   
            
        print("start websocket server", self.avdeccctl)
        self.start_server = websockets.serve(self.websocketLoop, ipaddress, port)

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
                        break                        
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
                await self.discovered(ws)
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
  
  
    async def discovered(self, ws):   
        self.talkers.append( AVDECCEntity(len(self.talkers)+1, "discovered%d"%(len(self.talkers)+1),"talker") )
        await ws.send( json.dumps( {"discovered":[self.talkers[-1].getJSONprepObject()]} ) )
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
      


