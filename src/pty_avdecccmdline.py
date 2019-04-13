import asyncio
from asyncio.subprocess import PIPE, STDOUT

avdecccmdline = "/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline"

avdecccmdline_commands = ["list" # show all avdecc enabled devices
                            "select 0x50c2fffed43574 0 0", # select endstation to read descriptors from
                            "view descriptor STREAM_INPUT 0", # lookup channel count in stream descriptor
                            "view descriptor STREAM_OUTPUT 0"
                         ] 

def writeStdin(process, cmdStr):
    #print("writeStdin")
    process.stdin.write(cmdStr.encode("utf-8"))

async def readStdOut(process, cmd, timeout): 
    #print("readStdOut")
    readLines = []
    while(True):
        line = ''
        try:
            line = await asyncio.wait_for(process.stdout.readline(), timeout)            
            if line != '':
                readLines.append(line.decode("utf-8"))
        except asyncio.TimeoutError:
                break
    if cmd == "netdev": 
        await choose_avdeccctl_netdev(readLines, process)
    elif cmd == "list":       
        result_avdeccctl_list(readLines)

async def prompt_avdeccctl_netdev(process):
    print("prompt_avdeccctl_netdev")
    await readStdOut(process, "netdev", 2)

async def choose_avdeccctl_netdev(readLines, process):
    print("choose_avdeccctl_netdev")
    for line in readLines: 
        if line[0] == "2":
            resultStr = line.split("\n")[0]
            print(resultStr)
            writeStdin(process, "2\n")
            await readStdOut(process, "", 2)

async def command_avdeccctl_list(process):
    print("command_avdeccctl_list")
    writeStdin(process, "list\n")
    await readStdOut(process, "list", 2)

def result_avdeccctl_list(readLines):
    print("result_avdeccctl_list")
    foundList = False
    for line in readLines: 
        if "----------------------------------------------------------------------------------------------------" in line:
            print("AVDECC devices online:")
            foundList = True
        elif foundList:
            if "|" in line:
                resultStr = line.split("\n")[0]
                print(resultStr)

async def run_command(*args, timeout=None):
    # start child process
    # NOTE: universal_newlines parameter is not supported
    process = await asyncio.create_subprocess_exec(*args,
            stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    # read line (sequence of bytes ending with b'\n') asynchronously
    await prompt_avdeccctl_netdev(process)
    await command_avdeccctl_list(process)

    process.kill() 
    return await process.wait() # wait for the child process to exit


loop = asyncio.get_event_loop()
loop.run_until_complete(run_command(avdecccmdline, timeout=10))
loop.close()
