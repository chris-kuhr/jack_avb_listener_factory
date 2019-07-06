#!/usr/bin/env python3
import asyncio
import datetime
import random
import websockets
import json

import mmap
import os
import time


import threading
import posix_ipc
import ipc_utils as utils

from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List


class WebsocketController(threading.Thread):
    def __init__(self, argv, semName, shmName, mqName, ipaddress='127.0.0.1', port=5678, avb_dev="ens2f1"):        
        super().__init__()
        print("setup websocket server")    
        self.avb_dev = avb_dev

        # Create the message queue.
        self.mq = posix_ipc.MessageQueue(mqName)
                
        # Create the shared memory and the semaphore.
        self.memory = posix_ipc.SharedMemory(shmName)
        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)
                
        self.semaphore = posix_ipc.Semaphore(semName)
        self.semaphore.release()
                            
        self.running = False
        
        self.listeners = []
        self.talkers = []
        
        self.serList = []
               
        print("start websocket server")
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
            await self.updateAVBEntityList(ws)
            
        print("List lengths: \n listeners", len(self.listeners),  " talkers ",len(self.talkers),  " serList ",len(self.serList))
                
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
                        await self.newHostEndpoint(ws, key, msg_dec)              
                    elif key == "reqListener":
                        await self.reqListener(ws, key, msg_dec)
                    elif key == "reqTalker":
                        await self.reqTalker(ws, key, msg_dec)
                    elif key == "connect":
                        await self.connect(ws, key, msg_dec)
                    elif key == "disconnect":
                        await self.disconnect(ws, key, msg_dec)
                              
            except asyncio.TimeoutError:    
                  
                if self.readList():
                    await self.updateAVBEntityList(ws)
                    
                print("List lengths: \n listeners", len(self.listeners),  " talkers ",len(self.talkers),  " serList ",len(self.serList))
                pass    
    #-------------------------------------------------------------------------------------------------------------------------
  
  
    async def newHostEndpoint(self, ws, key, msg_dec):
        newEndpoint = AVDECCEntity(0,"","")
        if msg_dec[key][0]["EPType"] == "talker":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.talkers)+1)
            if not any(talker.name == entity.name for talker in self.talkers):
                self.talkers.append(newEndpoint)
        if msg_dec[key][0]["EPType"] == "listener":
            newEndpoint.setfromJSONObject(msg_dec[key][0], len(self.listener)+1)
            if not any(listener.name == entity.name for listener in self.listeners):
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
        await ws.send( json.dumps( {"discovered":[endpointObj.getJSONprepObject()]} ) )
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

        if len(serList) != len(self.serList):
            self.serList = serList
            return True
        
        return False
    #-------------------------------------------------------------------------------------------------------------------------
        
    async def updateAVBEntityList(self, ws):
        for device in self.serList: 
            print("ws_server: ", device) 
            entity = AVDECCEntity(0, "","")  
            print("endpointtype", entity.endpointType)
            
            if entity.decodeString(device) > 0:
                print("endpointtype", entity.endpointType)
                if "talker" in entity.endpointType: 
                    entity.idx = len(self.talkers)+1
                    if not any(talker.name == entity.name for talker in self.talkers):
                        self.talkers.append(entity)
                        await self.discovered(ws, entity )
                elif "listener" in entity.endpointType: 
                    entity.idx = len(self.listeners)+1 
                    if not any(listener.name == entity.name for listener in self.listeners):
                        self.listeners.append(entity)
                        await self.discovered(ws, entity )
                print("endpointtype", entity.endpointType)
            else:
                break
            
            print("endpointtype", entity.endpointType)
    #-------------------------------------------------------------------------------------------------------------------------
     
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever() 
    #--------------------------------------------------------------------------------------
    
#=======================================================================================================================
      


