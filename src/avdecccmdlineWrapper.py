import asyncio
from asyncio.subprocess import PIPE, STDOUT
import mmap
import os
import sys
import time
import posix_ipc
import ipc_utils as utils
from avdeccEntity import AVDECCEntity, serializeList2Str, deserializeStr2List
from PyQt5.QtCore import QObject, QThread


class AVDECC_Controller(QThread):

    def __init__(self, avb_dev):
        super().__init__()
        self.avdecccmdline_cmd = "/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline"
        self.avb_dev = avb_dev
        self.sformats = []

        # open shared mem segment

        self.params = utils.read_params()

        # Mrs. Premise has already created the semaphore and shared memory.
        # I just need to get handles to them.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"])
        self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME"])
        self.mq = posix_ipc.MessageQueue(self.params["MESSAGE_QUEUE_NAME"])

        # MMap the shared memory
        self.mapfile = mmap.mmap(self.memory.fd, self.memory.size)
        self.semaphore.release()

        # Once I've mmapped the file descriptor, I can close it without
        # interfering with the mmap. This also demonstrates that os.close() is a
        # perfectly legitimate alternative to the SharedMemory's close_fd() method.
        os.close(self.memory.fd)
        
        
        #avdecccmdline_commands = ["list" # show all avdecc enabled devices
        #                    "select 0x50c2fffed43574 0 0", # select endstation to read descriptors from
        #                    "view descriptor STREAM_INPUT 0", # lookup channel count in stream descriptor
        #                    "view descriptor STREAM_OUTPUT 0"
        #                 ] 
    #--------------------------------------------------------------------------------------

    def writeStdin(self, cmdStr):
        #print("writeStdin")
        self.process.stdin.write(cmdStr.encode("utf-8"))
    #--------------------------------------------------------------------------------------

    async def readStdOut(self, cmd, timeout): 
        #print("readStdOut")
        readLines = []
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

        elif cmd == "controller": 
            print(cmd, "is not implemented yet...")

        elif cmd == "disconnect": 
            print(cmd, "is not implemented yet...")

        elif cmd == "entity": 
            print(cmd, "is not implemented yet...")

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
            await self.result_avdeccctl_view(readLines)
            
    #--------------------------------------------------------------------------------------


    async def prompt_avdeccctl_netdev(self):
        print("prompt_avdeccctl_netdev")
        await self.readStdOut("netdev", 2)
    #--------------------------------------------------------------------------------------

    async def choose_avdeccctl_netdev(self, readLines):
        print("choose_avdeccctl_netdev")
        for line in readLines: 
            if line[0] == "2":
                print(self.avb_dev)
                resultStr = line.split("\n")[0]
                print(resultStr)
                self.writeStdin("2\n")
                await self.readStdOut("", 2)
    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_list(self, cmd):
        print("command_avdeccctl_list")
        self.writeStdin("%s\n"%(cmd))
        await self.readStdOut("list", 2)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_list(self, readLines):
        print("result_avdeccctl_list")
        foundList = False
        entity_list = []
        for line in readLines: 
            if "----------------------------------------------------------------------------------------------------" in line:
                print("AVDECC devices online:")
                foundList = True
            elif foundList:
                if "|" in line:
                    resultStr = line.split("\n")[0].split("|")
                    #print(resultStr)
                        
                    avdecc_entity = AVDECCEntity()
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


                    print("select entity: select [e_s] [e_i] [c_i] \n Parameters:  e_s      : the End Station (index as int or Entity ID) \n e_i      : the entity index (type int) \n c_i      : the configuration index (type int)" )
                                        
                    await self.command_avdeccctl_select("select %s %d %d"%(entityId, 0, 0))
                    # $ get stream_info STREAM_OUTPUT 0
                    # AEM_DESC_STREAM_OUTPUT 1
                    # AEM_DESC_STREAM_OUTPUT 2
                    # AEM_DESC_STREAM_OUTPUT 3
                    # AEM_DESC_STREAM_OUTPUT 4
                    # AEM_DESC_STREAM_OUTPUT 5
                    # AEM_DESC_STREAM_OUTPUT 6
                    # AEM_DESC_STREAM_OUTPUT 7
                    # AEM_DESC_STREAM_OUTPUT 8
                    # Stream format: IEC...48KHZ_8CH
                    # Stream ID: 0x00019f1c391e0000
                    # Stream Destination MAC: 91e0f000fe80
                    # Stream VLAN ID: 2


                    print("view descriptor")
                    await self.command_avdeccctl_view("view descriptor STREAM_INPUT 0")
                    for sformat in self.sformats:
                        if int(sformat[0].split("KHZ")[0]) == avdecc_entity.sampleRate_k:
                            avdecc_entity.channelCountListener = int(sformat[1].split("CH")[0])
                            
                    await self.command_avdeccctl_view("view descriptor STREAM_OUTPUT 0")
                    for sformat in self.sformats:
                        if int(sformat[0].split("KHZ")[0]) == avdecc_entity.sampleRate_k:
                            avdecc_entity.channelCountTalker = int(sformat[1].split("CH")[0])
                    
                    entity_list.append(avdecc_entity)
                    #print(entity_list[-1].encodeString())

        serStr = serializeList2Str(entity_list)

        self.semaphore.acquire()
        utils.write_to_memory(self.mapfile, serStr)
        self.semaphore.release()


    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_select(self, cmd):
        print("command_avdeccctl_select")
        self.writeStdin("%s\n"%(cmd))
        await self.readStdOut("select", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_select(self, readLines):
        print("result_avdeccctl_select")
        for line in readLines:
            print(line.split("\n")[0])
    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_view(self, cmd):
        print("command_avdeccctl_view")
        self.writeStdin("%s\n"%(cmd))
        await self.readStdOut("view", 0.5)
    #--------------------------------------------------------------------------------------

    async def result_avdeccctl_view(self, readLines):
        print("result_avdeccctl_view")
        self.sformats = []
        for line in readLines:
            if "stream_format" in line:
                sformat = line.split("\n")[0].split("IEC...")[1].split("_")
                print( sformat ) 
                self.sformats.append(sformat)            
    #--------------------------------------------------------------------------------------

    async def run_command(self, *args, timeout=None):
    
        # start child process
        # NOTE: universal_newlines parameter is not supported
        self.process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        await self.prompt_avdeccctl_netdev()

        while(True):
            # read notification
            # check mqueue
            print("waiting for msg")
            msg, _ = self.mq.receive()
            msg = msg.decode()
            if "list" in msg:
                print("received list cmd")
                await self.command_avdeccctl_list("list")
                self.mq.send("ack")
            elif "connect" in msg:
                pass
            elif "view" in msg:
                pass
            elif "quit" in msg:
                self.writeStdin("quit")
                break
           

        self.process.kill() 
        self.semaphore.release()
        self.semaphore.close()
        self.mapfile.close()
        self.mq.close()
        return await self.process.wait() # wait for the child process to exit
    #--------------------------------------------------------------------------------------

    def run_avdecccmdline_thread(self):    
        loop = asyncio.new_event_loop();
        asyncio.set_event_loop(loop)
        #loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_command(self.avdecccmdline_cmd, timeout=10))
        loop.close()
    #--------------------------------------------------------------------------------------
