class AVDECCEntity(object):
    def __init__(self):        
        self.idx = -1
        self.name = "noname"
        self.entityId = b'aabbcc0011ddeeff'
        self.firmwareVersion = "0"
        self.MACAddr = b'aabbccddeeff'
        self.endpointType = 'tl'
        self.channelCount = 2
        self.sampleRate_k = 48
        self.destMAC = b'aabbccddeeff'
        self.streamId = b'aabbcc0011ddeeff'
    #-------------------------------------------

    def encodeString(self):
        return "%d;%s;%s;%s;%s;%s;%d;%d;%s;%s;" %( self.idx, self.name, self.entityId.decode("utf8"), self.firmwareVersion, self.MACAddr.decode("utf8"), self.endpointType, self.channelCount, self.sampleRate_k, self.destMAC.decode("utf8"), self.streamId.decode("utf8")) 
    #-------------------------------------------


    def decodeString(self, strObj):
        propList = strObj.split(";")
        try:
            self.idx = int(propList[0])
        except ValueError:            
            return -1
        self.name = propList[1]
        self.entityId = bytearray(propList[2].encode("utf8"))
        self.firmwareVersion = propList[3]
        self.MACAddr = bytearray(propList[4].encode("utf8"))
        self.endpointType = propList[5]
        self.channelCount = int(propList[6])
        self.sampleRate_k = int(propList[7])
        self.destMAC = bytearray(propList[8].encode("utf8"))
        self.streamId = bytearray(propList[9].encode("utf8"))        
        return 1
    #-------------------------------------------


#=============================================
        
def serializeList2Str(list2ser):
    retStr = ""
    for obj in list2ser:
        if retStr =="":
            retStr += "%s"%obj.encodeString()
        else:
            retStr += "|%s"%obj.encodeString()
    return retStr
#-------------------------------------------


def deserializeStr2List(ser2list):
    retList = ser2list.split("|")
    return retList
#-------------------------------------------
