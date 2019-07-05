'''
Created on April 16, 2019

@author: christoph
'''
import sys, getopt
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import asyncio

from QtController import QtController
from WebsocketController import WebsocketController
from avdecccmdlineWrapper import AVDECC_Controller
  
def main(argv):
    ipaddress ="127.0.0.1"
    port = 5678
    qt = False
    dev = "ens1f0"
    
    
    try:
       opts, args = getopt.getopt(argv,"hqs:p:d:",["server=","port=","avb-dev="])
    except getopt.GetoptError:
       print ('-q= Qt5 Gui\n -s=server ip\n -p=listening port -d=avb-dev\n')
       sys.exit(2)
           
    for opt, arg in opts:
      if opt == '-h':
         print ('-q= Qt5 Gui\n -s=server ip\n -p=listening port -d=avb-dev\n')
         sys.exit()
      elif opt in ("-s", "--server"):
         ipaddress = arg
      elif opt in ("-d", "--avb-device"):
         avb_dev = arg
      elif opt in ("-p", "--port"):
         port = arg
      elif opt in ("-q", "--qt"):
         qt = True

        

    if qt:    
        qApp = QtWidgets.QApplication(sys.argv)
        pyqtavdecc = QtController()
    
        sys.exit(qApp.exec_())  
    else:    
          
        wsCtl = WebsocketController(sys.argv, ipaddress, port, avb_dev)  
        #self.avdeccctl = AVDECC_Controller(argv, avb_dev, cmd_path ="/opt/OpenAvnu/avdecc-lib/controller/app/cmdline/avdecccmdline")
        avdeccctl = AVDECC_Controller(argv, avb_dev, cmd_path ="/home/christoph/source_code/github-kuhr/OpenAvnu.git/avdecc-lib/controller/app/cmdline/avdecccmdline")
        avdeccctl.start()
        print("run until complete")
        asyncio.get_event_loop().run_until_complete(wsCtl.start_server)
        print("run forever")
        asyncio.get_event_loop().run_forever() 
              
        
        wsCtl.mapfile.close()
        posix_ipc.unlink_shared_memory(wsCtl.params["SHARED_MEMORY_NAME"])

        wsCtl.mq.close()
        posix_ipc.unlink_message_queue(wsCtl.params["MESSAGE_QUEUE_NAME"])

        wsCtl.semaphore.release()
        wsCtl.semaphore_mq_qui.release()
        wsCtl.semaphore_mq_wrapper.release()
        wsCtl.semaphore.unlink()
        wsCtl.semaphore_mq_gui.unlink()
        wsCtl.semaphore_mq_wrapper.unlink()
        sys.exit(0)
    #-------------------------------------------------------------------------------------------------------------------------
#=======================================================================================================================
 
if __name__ == '__main__':
   main(sys.argv[1:])
   
   
   
