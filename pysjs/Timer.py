'''
Created on May 16, 2017

@author: christoph
'''

import threading
import time

class ThreadedTimer(threading.Thread):
    def __init__(self, sec, callback, callbackData):
        threading.Thread.__init__(self)
        print("Init Timer %s" % sec)
        self.sec = sec
        self.callback = callback
        self.callbackData = callbackData
    #----------------------------------------------------------------------------------

    def run(self):
        while True:
            print("timeout")
            if self.callbackData:
                self.callback(self.callbackData)
            else:
                self.callback()
                
            time.sleep(self.sec)
    #----------------------------------------------------------------------------------

#========================================================================================
    