import asyncio
from asyncio.subprocess import PIPE, STDOUT
import mmap
import os
import sys
import time


import threading

import posix_ipc
import ipc_utils as utils

from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List
from PyQt5.QtCore import QObject



class AVDECC_Controller(threading.Thread):

    def __init__(self, argv, avb_dev, cmd_path="/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline"):
        super().__init__()
        self.argv = argv
        self.avdecccmdline_cmd = cmd_path
        self.avb_dev = avb_dev
        self.sformats = []
        self.endpointType = ""
        self.streamId = ""
        self.destMAC = ""

        # open shared mem segment

        self.params = utils.read_params()

        # Mrs. Premise has already created the semaphore and shared memory.
        # I just need to get handles to them.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"])
        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)
        
        self.semaphore = 0
        while self.semaphore == 0:
            try:
                self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME1"])
            except posix_ipc.ExistentialError:
                pass
        self.semaphore.release()
            
            
        self.semaphore_mq_gui = 0
        while self.semaphore_mq_gui == 0:
            try:
                self.semaphore_mq_gui = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME2"])  
            except posix_ipc.ExistentialError:
                pass  
        self.semaphore_mq_gui.release()
             
             
        self.semaphore_mq_wrapper = 0
        while self.semaphore_mq_wrapper == 0:
            try:
                self.semaphore_mq_wrapper = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME3"], posix_ipc.O_CREX)
            except posix_ipc.ExistentialError:
                pass
        self.semaphore_mq_wrapper.release()
        
        
        
        self.mq = posix_ipc.MessageQueue(self.params["MESSAGE_QUEUE_NAME"])


        # Once I've mmapped the file descriptor, I can close it without
        # interfering with the mmap. This also demonstrates that os.close() is a
        # perfectly legitimate alternative to the SharedMemory's close_fd() method.
        os.close(self.memory.fd)
        
        
        #avdecccmdline_commands = ["list" # show all avdecc enabled devices
        #                    "select 0x50c2fffed43574 0 0", # select endstation to read descriptors from
        #                    "view descriptor STREAM_INPUT 0", # lookup channel count in stream descriptor
        #                    "view descriptor STREAM_OUTPUT 0"
        #                 ] 
        print("AVDECC controller setup done.")
    #--------------------------------------------------------------------------------------

    def writeStdin(self, cmdStr):
        #print("writeStdin")
        self.process.stdin.write(cmdStr.encode("utf-8"))
    #--------------------------------------------------------------------------------------

    async def readStdOut(self, cmd, timeout): 
        #print("readStdOut")
        readLines = []
        result = None
        while(True):
            line = ''
            try:
                line = await asyncio.wait_for(self.process.stdout.readline(), timeout)            
                if line != '':
                    readLines.append(line.decode("utf-8"))
            except asyncio.TimeoutError:
                    break
        if cmd == "netdev": 
            await self.choose_avdeccctl_netdev(readLines)
        elif cmd == "list":       
            await self.result_avdeccctl_list(readLines)
        elif cmd == "acquire": 
            print(cmd, "is not implemented yet...")

        elif cmd == "audio_mappings": 
            print(cmd, "is not implemented yet...")

        elif cmd == "clr": 
            print(cmd, "is not implemented yet...")

        elif cmd == "connect": 
            print(cmd, "is not implemented yet...")

        elif cmd == "notification": 
            await self.notification_new_entity(readlines)

        elif cmd == "controller": 
            print(cmd, "is not implemented yet...")

        elif cmd == "disconnect": 
            print(cmd, "is not implemented yet...")

        elif cmd == "entity": 
            print(cmd, "is not implemented yet...")

        elif cmd == "get stream_info input": 
            await self.result_avdeccctl_get_stream_info(readLines, "l")

        elif cmd == "get stream_info output": 
            await self.result_avdeccctl_get_stream_info(readLines, "t")

        elif cmd == "get": 
            print(cmd, "is not implemented yet...")

        elif cmd == "help": 
            print(cmd, "is not implemented yet...")

        elif cmd == "identify": 
            print(cmd, "is not implemented yet...")

        elif cmd == "lock": 
            print(cmd, "is not implemented yet...")

        elif cmd == "log": 
            print(cmd, "is not implemented yet...")

        elif cmd == "param": 
            print(cmd, "is not implemented yet...")

        elif cmd == "path": 
            print(cmd, "is not implemented yet...")

        elif cmd == "q": 
            print(cmd, "is not implemented yet...")

        elif cmd == "quit": 
            print(cmd, "is not implemented yet...")

        elif cmd == "read": 
            print(cmd, "is not implemented yet...")

        elif cmd == "reboot": 
            print(cmd, "is not implemented yet...")
            
        elif cmd == "select": 
            await self.result_avdeccctl_select(readLines)
        elif cmd == "set": 
            print(cmd, "is not implemented yet...")

        elif cmd == "show": 
            print(cmd, "is not implemented yet...")

        elif cmd == "start": 
            print(cmd, "is not implemented yet...")

        elif cmd == "stop": 
            print(cmd, "is not implemented yet...")

        elif cmd == "unlog": 
            print(cmd, "is not implemented yet...")

        elif cmd == "unsolicited": 
            print(cmd, "is not implemented yet...")

        elif cmd == "upgrade": 
            print(cmd, "is not implemented yet...")

        elif cmd == "version": 
            print(cmd, "is not implemented yet...")
            
        elif cmd == "view": 
            result = await self.result_avdeccctl_view(readLines)
        
        return result
    #--------------------------------------------------------------------------------------


    async def prompt_avdeccctl_netdev(self):
        print("prompt_avdeccctl_netdev")
        return await self.readStdOut("netdev", 0.5)
    #--------------------------------------------------------------------------------------

    async def choose_avdeccctl_netdev(self, readLines):
        print("choose_avdeccctl_netdev")
        for line in readLines: 
            if line[0] == "2":
                print(self.avb_dev)
                resultStr = line.split("\n")[0]
                print(resultStr)
                self.writeStdin("2\n")
                return await self.readStdOut("", 0.5)
    #--------------------------------------------------------------------------------------
    
    async def command_avdeccctl_list(self, cmd):
        print("command_avdeccctl_list")
        self.writeStdin("%s\n"%(cmd))
        return await self.readStdOut("list", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_list(self,readLines):
        print("result_avdeccctl_list")
        foundList = False
        entity_list = []
        
        for line in readLines: 
            print(line)
            if "----------------------------------------------------------------------------------------------------" in line:
                print("AVDECC devices online:")
                foundList = True
            elif foundList:
                if "|" in line:
                    resultStr = line.split("\n")[0].split("|")
                    print(resultStr)
                        
                    avdecc_entity = AVDECCEntity(0,"","")
                    entityId = ""

                    for idx, field in enumerate(resultStr):
                        if idx == 0:
                            ll = field.split(" ")
                            for idx2, l in  enumerate(ll):
                                if idx2 > 0 and l != "":
                                    avdecc_entity.idx = int(l)
                        elif idx == 1:
                            avdecc_entity.name = field.lstrip().rstrip()
                        elif idx == 2:
                            entityId = field.lstrip().rstrip()
                            avdecc_entity.entityId = bytearray(entityId.split("x")[1].encode("utf8"))
                        elif idx == 3:
                            avdecc_entity.firmwareVersion = field.lstrip().rstrip()
                        elif idx == 4:
                            avdecc_entity.MACAddr = bytearray(field.lstrip().rstrip().encode("utf8"))
                    
                    await self.command_avdeccctl_select("select %s 0 0"%(entityId))
                    
                    
                    numEndpoints = await self.command_avdeccctl_view("view descriptor ENTITY 0")
                    
                    #avdecc_entity.endpointType = self.endpointType
                    print(numEndpoints)
                    
                    for endpoint in  numEndpoints:
                        avdecc_entity.endpointType = endpoint
                        
                        if "listener" in endpoint:
                            await self.command_avdeccctl_get_stream_info("get stream_info STREAM_INPUT 0")     
                            for sformat in self.sformats:
                                if int(sformat[0].split("KHZ")[0]) == avdecc_entity.sampleRate_k:
                                    avdecc_entity.channelCount = int(sformat[1].split("CH")[0]) 
            
                        elif "talker" in endpoint:
                            await self.command_avdeccctl_get_stream_info("get stream_info STREAM_OUTPUT 0") 
                            for sformat in self.sformats:
                                if int(sformat[0].split("KHZ")[0]) == avdecc_entity.sampleRate_k:
                                    avdecc_entity.channelCount = int(sformat[1].split("CH")[0]) 
                            avdecc_entity.streamId = bytearray(self.streamId.encode("utf8"))
                            print(avdecc_entity.streamId)
                            avdecc_entity.destMAC = bytearray(self.destMAC.encode("utf8"))
                            print(avdecc_entity.destMAC)
                        
                        
                        entity_list.append(avdecc_entity)
                        print("AVDECC ctl: ", entity_list[-1].encodeString())



        #
        #
        #   create json object
        #
        #


        serStr = serializeList2Str(entity_list)

        self.semaphore.acquire()
        utils.write_to_memory(self.mapfile, serStr)
        self.semaphore.release()


    #--------------------------------------------------------------------------------------





    async def notification_new_entity(self, readlines):
        """ [NOTIFICATION] (END_STATION_CONNECTED, 0xa0369ffffebd9493, 0, 0, 0, 0 (nil)) 
            [NOTIFICATION] (END_STATION_READ_COMPLETED, 0xa0369ffffebd9493, 0, 0, 0, 0 (nil)) 
        """
        print("Notification: \n", readlines)
    #--------------------------------------------------------------------------------------












    async def command_avdeccctl_get_stream_info(self, cmd):
        print("command_avdeccctl_get_stream_info")
        self.writeStdin("%s\n"%(cmd))
        if "INPUT" in cmd:
            return await self.readStdOut("get stream_info input", 0.5)
        elif "OUTPUT" in cmd:
            return await self.readStdOut("get stream_info output", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_get_stream_info(self, readLines, endpointType):
        print("result_avdeccctl_get_stream_info", endpointType)
        self.sformats = []
        self.streamId = ""
        self.destMAC = ""
        for line in readLines:
            # Stream format: IEC...48KHZ_8CH
            # Stream ID: 0x00019f1c391e0000
            # Stream Destination MAC: 91e0f000fe80
            # Stream VLAN ID: 2
            
            if "Stream format" in line:
                try:
                    sformat = line.split("\n")[0].split("IEC...")[1].split("_")
                    print( sformat ) 
                    self.sformats.append(sformat)  
                except IndexError:
                    self.sformats.append("2")  
                    
            if "t" in endpointType:    
                if "Stream ID" in line:
                    self.streamId = line.split("\n")[0].split(":")[1].lstrip().split("x")[1]
                    print( self.streamId ) 
                if "Stream Destination MAC" in line:
                    self.destMAC = line.split("\n")[0].split(":")[1].lstrip()
                    print( self.destMAC )            
    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_select(self, cmd):
        print("command_avdeccctl_select")
        self.writeStdin("%s\n"%(cmd))
        return await self.readStdOut("select", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_select(self, readLines):
        print("result_avdeccctl_select")
        for line in readLines:
            print(line.split("\n")[0])
    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_view(self, cmd):
        print("command_avdeccctl_view")
        self.writeStdin("%s\n"%(cmd))
        return await self.readStdOut("view", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_view(self, readLines):
        print("result_avdeccctl_view")
        self.endpointType = ""
        res = []
        for line in readLines:
            if "talker_stream_sources" in line and int(line.split("\n")[0].split(" ")[2]) > 0: 
                self.endpointType = "talker"  
                res.append(self.endpointType)
            if "listener_stream_sinks" in line and int(line.split("\n")[0].split(" ")[2]) > 0:
                self.endpointType = "listener"  
                res.append(self.endpointType)
                
        return res
        
    #--------------------------------------------------------------------------------------
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.run_command(self.avdecccmdline_cmd))
 #--------------------------------------------------------------------------------------

        
    async def run_command(self, *args, timeout=None):
        print("run controller loop.")
        self.process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        await self.prompt_avdeccctl_netdev()
        self.mq.send("ready")
        print("have sent ready")
        
        while(True):
            # read notification
            # check mqueue
            print("waiting for msg")
            try:
                msg, = self.mq.receive(5)
                msg = msg.decode()
                if "discover" in msg:
                    print("received discover cmd")
                    await self.command_avdeccctl_list("list")
                    self.mq.send("ack")
                elif "connect" in msg:
                    pass
                elif "view" in msg:
                    pass
                elif "quit" in msg:
                    self.writeStdin("quit")
                    break
                    
            except (posix_ipc.BusyError, ValueError):
                self.readStdOut("notification",10)
            
           
        self.process.kill() 
    
        # I could call memory.unlink() here but in order to demonstrate
        # unlinking at the module level I'll do it that way.
        posix_ipc.unlink_shared_memory(self.params["SHARED_MEMORY_NAME"])
        
        self.semaphore.release()
        self.semaphore_mq_gui.release()
        self.semaphore_mq_wrapper.release()
        self.semaphore.unlink()
        self.semaphore_mq_gui.unlink()
        self.semaphore_mq_wrapper.unlink()
        self.mapfile.close()
        self.mq.close()
        return await self.process.wait() # wait for the child process to exit
    #--------------------------------------------------------------------------------------

