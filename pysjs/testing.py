'''
Created on May 18, 2017

@author: christoph
'''
import json

if __name__ == '__main__':
    
    dataDict = {"a":1,"b":2,"c":3,"d":4,"e":5}
    
    json_obj = json.dumps([{"type":"action", "message":"Logout", "action":"all"}, dataDict])
    
    print( json_obj )
    
    pyObj = json.loads( json_obj )
    
    print( pyObj[0]['type'] )
    print( pyObj["message"] )
    print( pyObj["action"] )
    print( pyObj["a"] )
    print( pyObj["b"] )
    print( pyObj["c"] )
    print( pyObj["d"] )
    print( pyObj["e"] )
    
    
    pass