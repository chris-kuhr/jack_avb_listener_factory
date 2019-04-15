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

    def __init__(self):
        super().__init__()
        self.avdecccmdline_cmd = "/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline"


        # open shared mem segment

        self.params = utils.read_params()

        # Mrs. Premise has already created the semaphore and shared memory.
        # I just need to get handles to them.
        self.memory = posix_ipc.SharedMemory(self.params["SHARED_MEMORY_NAME"])
        self.semaphore = posix_ipc.Semaphore(self.params["SEMAPHORE_NAME"])

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
            self.result_avdeccctl_list(readLines)
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
            print(cmd, "is not implemented yet...")

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
            self.result_avdeccctl_view(readLines)
    #--------------------------------------------------------------------------------------


    async def prompt_avdeccctl_netdev():
        print("prompt_avdeccctl_netdev")
        await self.readStdOut("netdev", 2)
    #--------------------------------------------------------------------------------------

    async def choose_avdeccctl_netdev(readLines, process, mapfile, semaphore):
        print("choose_avdeccctl_netdev")
        for line in readLines: 
            if line[0] == "2":
                resultStr = line.split("\n")[0]
                print(resultStr)
                self.writeStdin("2\n")
                await self.readStdOut("", 2)
    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_list():
        print("command_avdeccctl_list")
        self.writeStdin("list\n")
        await self.readStdOut("list", 2)
    #--------------------------------------------------------------------------------------

    def result_avdeccctl_list(readLines):
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

                    for idx, field in enumerate(resultStr):
                        if idx == 0:
                            ll = field.split(" ")
                            for idx2, l in  enumerate(ll):
                                if idx2 > 0 and l != "":
                                    avdecc_entity.idx = int(l)
                        elif idx == 1:
                            avdecc_entity.name = field.lstrip().rstrip()
                        elif idx == 2:
                            avdecc_entity.entityId = bytearray(field.lstrip().rstrip().split("x")[1].encode("utf8"))
                        elif idx == 3:
                            avdecc_entity.firmwareVersion = field.lstrip().rstrip()
                        elif idx == 4:
                            avdecc_entity.MACAddr = bytearray(field.lstrip().rstrip().encode("utf8"))

                    entity_list.append(avdecc_entity)
                    #print(entity_list[-1].encodeString())

        serStr = serializeList2Str(entity_list)

        self.semaphore.acquire()
        utils.write_to_memory(self.mapfile, serStr)
        self.semaphore.release()

    #--------------------------------------------------------------------------------------

    async def command_avdeccctl_view():
        print("command_avdeccctl_view")
        self.writeStdin("list\n")
        await self.readStdOut("list", 2)
    #--------------------------------------------------------------------------------------

    def result_avdeccctl_view(readLines):
        print("result_avdeccctl_view")
        foundList = False
        print(cmd, "is not implemented yet...")
        for line in readLines:
            pass 
    #--------------------------------------------------------------------------------------

    async def run_command(self, *args, timeout=None):
    
        # start child process
        # NOTE: universal_newlines parameter is not supported
        self.process = await asyncio.create_subprocess_exec(*args, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        # read line (sequence of bytes ending with b'\n') asynchronously
        await self.prompt_avdeccctl_netdev()
        await self.command_avdeccctl_list()

        self.process.kill() 
        self.semaphore.release()
        self.semaphore.close()
        self.mapfile.close()
        return await self.process.wait() # wait for the child process to exit
    #--------------------------------------------------------------------------------------

    def run_avdecccmdline_thread(self):    
        loop = asyncio.new_event_loop();
        asyncio.set_event_loop(loop)
        #loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_command(self.avdecccmdline_cmd, timeout=10))
        loop.close()
    #--------------------------------------------------------------------------------------
