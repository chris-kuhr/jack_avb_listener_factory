'''
Created on April 16, 2019

@author: christoph
'''
import sys, getopt
import asyncio

from WebsocketController import WebsocketController
from avdecccmdlineWrapper import AVDECC_Controller
  
def main(argv):
    ipaddress ="127.0.0.1"
    port = 5678
    qt = False
    dev = "ens1f0"
    
    
    try:
       opts, args = getopt.getopt(argv,"hs:p:d:",["server=","port=","avb-dev="])
    except getopt.GetoptError:
       print ('-s=server ip\n -p=listening port\n -d=avb-dev\n')
       sys.exit(2)
           
    for opt, arg in opts:
      if opt == '-h':
         print ('-s=server ip\n -p=listening port\n -d=avb-dev\n')
         sys.exit()
      elif opt in ("-s", "--server"):
         ipaddress = arg
      elif opt in ("-d", "--avb-device"):
         avb_dev = arg
      elif opt in ("-p", "--port"):
         port = arg

    
    ipc_params = utils.read_params()
    semName = ipc_params["SEMAPHORE_NAME"]
    shmName = ipc_params["SHARED_MEMORY_NAME"]
    mqName = ipc_params["MESSAGE_QUEUE_NAME"]
    semaphore = posix_ipc.Semaphore(semName, posix_ipc.O_CREX)
    memory = posix_ipc.SharedMemory(shmName, posix_ipc.O_CREX, size=ipc_params["SHM_SIZE"])
    mq = posix_ipc.MessageQueue(mqName, posix_ipc.O_CREX)

          
    wsCtl = WebsocketController(sys.argv, semName, shmName, mqName, ipaddress, port, avb_dev)  
    wsCtl.start()
    
    #self.avdeccctl = AVDECC_Controller(argv, avb_dev, cmd_path ="/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline")
    avdeccctl = AVDECC_Controller(sys.argv, semName, shmName, mqName, avb_dev, cmd_path ="/home/soundjack/OpenAvnu.git.kuhr/avdecc-lib/controller/app/cmdline/avdecccmdline")
    avdeccctl.start()
          
    wsCtl.join()
    avdeccctl.join()
    
    posix_ipc.unlink_shared_memory(shmName)
    mq.close()
    posix_ipc.unlink_message_queue(mqName)

    semaphore.release()
    semaphore.unlink()
    sys.exit(0)
    #-------------------------------------------------------------------------------------------------------------------------
#=======================================================================================================================
 
if __name__ == '__main__':
   main(sys.argv[1:])
   
   
   
