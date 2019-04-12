'''
Created on May 16, 2017

@author: christoph
'''
import threading
import time
import _thread

import asyncio
import concurrent.futures
from asyncio import AbstractEventLoop
from datetime import datetime
import random
import websockets
import json
import ssl
import MySQLdb 


""" 

OPCODE Definition taken from /usr/local/lib/python3.5/dist-packages/websockets/framing.py 

"""
OP_CONT, OP_TEXT, OP_BINARY = range(0x00, 0x03)
OP_CLOSE, OP_PING, OP_PONG = range(0x08, 0x0b)

listenSocket = ["192.168.2.100", 1234]
sjServer = None
mySQL_Connector = None

def getSjServer():
    return sjServer

class MyMySQL(object):
    def __init__(self):
        self.sqlDB = None 
        self.lock_access = False
        self.connect2DB()
    #----------------------------------------------------------------------------------
    
    def connect2DB(self):           
        try:
            self.sqlDB=MySQLdb.connect(db="joomla_sj",
                               port=3306,
                               host="127.0.0.1",
                               user="root",                           
                               passwd="fastMUSIC2016!")
            print("connected to MYSQL DB.")
            
        except MySQLdb.Error as e:
            try:
                print( "[MySQLdb] Error Connecting to MYSQL DB: %d %s" %(e.args[0], e.args[1]))
            except IndexError:
                print("[MySQLdb] Error Connecting to MYSQL DB: %s" % (str(e)))
    #----------------------------------------------------------------------------------
                
    def getDBDescription(self,  database):
        cursor = self.acquire_db_lock()
        try:
            cursor.execute("""DESCRIBE %s"""%(database))
            dataRow = cursor.fetchall()
            if dataRow:
                for row in dataRow:
                    print(row)
            else:
                print( "no results")
        except MySQLdb.Error as e:
            try:
                print( "[MySQLdb] Fehler beim Init SELECT: %d %s" %(e.args[0], e.args[1]))
                if e.args[0] == 2006:
                    return self.resetDBConnection()
            except IndexError:
                print("[MySQLdb] Fehler beim  Init SELECT: %s" % (str(e)))
        
        self.release_db_lock()
    #----------------------------------------------------------------------------------
    
    def acquire_db_lock(self):        
        while self.lock_access:
            time.sleep(0.1)
            
        return self.sqlDB.cursor()
    #----------------------------------------------------------------------------------
    
    def release_db_lock(self):        
        if self.lock_access:
            self.lock_access = False
    #----------------------------------------------------------------------------------
    
    def disconnect(self):
        self.sqlDB.close()
    #----------------------------------------------------------------------------------
    
    def resetDBConnection(self):       
        print("resetting DB Connection!")
        self.disconnect()
        self.connect2DB()
        return 1
    #----------------------------------------------------------------------------------
    
    def exceptionHandling(self,  occurance,  error):        
        try:
            print( "[MySQLdb] %s: %d %s" %(occurance, error.args[0], error.args[1]))
            if error.args[0] == 2006:      
                return self.resetDBConnection()
        except IndexError:
            print("[MySQLdb] %s: %s" % (str(error)))
    #----------------------------------------------------------------------------------
#========================================================================================

class SJClient(object):
    def __init__(self, websocket ):
        self.websocket = websocket
        self.current_RemoteUDPSocket = []
    #----------------------------------------------------------------------------------
    
    def startCurrentUDPPort(self,  peer,  udpPort):
        foundSocket = False
        for remoteSocket in self.current_RemoteUDPSocket:
            if remoteSocket[0] == peer:
                foundSocket = True
                return foundSocket
        
        if not foundSocket:
            self.current_RemoteUDPSocket.append( [peer, int(udpPort)] )
            return foundSocket
    #----------------------------------------------------------------------------------
    
    def removeCurrentUDPPort(self,  peer):
        foundSocket = False
        for remoteSocket in self.current_RemoteUDPSocket:
            if remoteSocket[0] == peer:
                foundSocket = True
                self.current_RemoteUDPSocket.remove(remoteSocket)
                return foundSocket
                
        if not foundSocket:
            return foundSocket
    #----------------------------------------------------------------------------------
    
    def incrementUDPPort(self,  peer):
        for idx, remoteSocket in enumerate( self.current_RemoteUDPSocket ):
            if remoteSocket[0] == peer:
                self.current_RemoteUDPSocket[idx][1] += 1
    #----------------------------------------------------------------------------------
    
    def decrementUDPPort(self, peer):
        for idx, remoteSocket in enumerate( self.current_RemoteUDPSocket ):
            if remoteSocket[0] == peer:
                self.current_RemoteUDPSocket[idx][1] -= 1
    #----------------------------------------------------------------------------------
    
    def getUDPPort(self, peer):
        for idx, remoteSocket in enumerate( self.current_RemoteUDPSocket ):
            if remoteSocket[0] == peer:
                return int(self.current_RemoteUDPSocket[idx][1])
        return -1
    #----------------------------------------------------------------------------------
    
    def getPeerInfo(self):
        peer = str(self.websocket.writer.get_extra_info('peername')).replace("'","").replace("(","").replace(" ","").replace(")","").split(",")
        return peer
    #----------------------------------------------------------------------------------
#========================================================================================

class SJServer(object):
    def __init__(self, mySQL_Connector, port, parent, debug = False ):
        self.sendString = "undefined"
        self.sendObject = None
        self.clients = []
        self.debug = debug
        self.mySQL_Connector = mySQL_Connector
        self.mySQL_Connector.getDBDescription("sj_userlist")
        self.mySQL_Connector.getDBDescription("jos_users")
    #----------------------------------------------------------------------------------

    def onNewConnection(self, websocket):
        newClient = SJClient( websocket )
        self.clients.append( newClient )
        peer = self.clients[-1].getPeerInfo()
        print("new client %s" % peer)
        cursor = self.mySQL_Connector.acquire_db_lock()
        retryTransaction = 3
        while retryTransaction > 0:
            try:
                ret = cursor.execute("""INSERT INTO sj_userlist(ip,portTCP,pong,name,portUDP,portUDP2,portUDP3,audio,connected) VALUES('%s','%s','HERE','undefined','undefined','undefined','undefined','No','undefined')"""%(peer[0], peer[1]))
               
                dataRows = cursor.fetchall()            
                print( ret , dataRows )            
                if not ret:
                    self.mySQL_Connector.sqlDB.rollback()
                    print( "Peer %s NOT inserted" % peer)
                    retryTransaction -= 1         
                else:
                    self.mySQL_Connector.sqlDB.commit()
                    print( "Peer %s inserted" % peer)
                    retryTransaction = 0  
            except MySQLdb.Error as e:
                self.mySQL_Connector.exceptionHandling( "INSERT PROBLEM: Peer %s NOT inserted"%(peer), e)
                retryTransaction -= 1  
                cursor = self.mySQL_Connector.acquire_db_lock()
        self.mySQL_Connector.release_db_lock()
    #----------------------------------------------------------------------------------
    
    def socketDisconnect(self, websocket):
        print("socketDisconnect")
        cursor = self.mySQL_Connector.acquire_db_lock()
        for client in self.clients:
            if client.websocket == websocket:
                dataRow = None      
                peer = client.getPeerInfo(  )
                print(peer)    
                 
                retryTransaction = 3
                while retryTransaction > 0:    
                    """ INFO UND AUS DATENBANK LÖSCHEN"""
                    try:
                        ret = cursor.execute("""DELETE FROM sj_userlist WHERE ip  = '%s' AND portTCP = '%s'"""%(peer[0], peer[1]))
                        dataRow = cursor.fetchone()
                        if not ret:
                            retryTransaction -= 1                              
                        else:
                            print( "Peer %s went offline" % peer)
                            retryTransaction = 0  
                    except MySQLdb.Error as e:
                        self.mySQL_Connector.exceptionHandling( "DELETE Peer %s went offline"%(peer), e)
                        retryTransaction -= 1  
                        cursor = self.mySQL_Connector.acquire_db_lock()
                    
                retryTransaction = 3
                while retryTransaction > 0:    
                    """SET AUTO INCREMENT (AI) TO ZERO IF POSSIBLE"""
                    try:
                        ret = cursor.execute("""ALTER TABLE sj_userlist AUTO_INCREMENT=1""")
                        if not ret:
                            retryTransaction -= 1    
                            print( "ALTER PROBLEM: AUTO INCREMENT NICHT ERFOLGREICH GESETZT")
                        else:
                            print( "AUTO INCREMENT ERFOLGREICH GESETZT")
                            retryTransaction = 0  
                    except MySQLdb.Error as e:
                        self.mySQL_Connector.exceptionHandling( "ALTER PROBLEM: AUTO INCREMENT KONNTE NICHT GESETZT WERDEN", e)
                        retryTransaction -= 1  
                        cursor = self.mySQL_Connector.acquire_db_lock()
                
                """NOTIFY ALL USERS ABOUT DISCONNECTED PEER"""
                dataDict = {"type":"system", 
                            "message":"Logout: %s:%s"%(peer[0], peer[1]), 
                            "action":"Delete user", 
                            "remoteIP":peer[0], 
                            "remotePort":peer[1]}
                self.send_reply_wrapper(  dataDict )
                self.clients.remove( client )                     
        self.mySQL_Connector.release_db_lock()
        return
    #----------------------------------------------------------------------------------
   
    def send_reply_wrapper(self, dataDict, print_message=False):
        loop = asyncio.get_event_loop()
        future = asyncio.Future()
        asyncio.ensure_future(self.send_reply(dataDict, future,  print_message))
        loop.run_until_complete(future)
        print(future.result())
        loop.close()
    #----------------------------------------------------------------------------------


    async def send_reply(self, dataDict, future=None,  print_message=False):         
        sendObject = json.dumps( dataDict )
        if print_message:
            print( sendObject )
        for client in self.clients:
            try:
                await client.websocket.send(sendObject)
            except websockets.exceptions.ConnectionClosed as err:      
                print("[Send Reply] Websocket Exception, Websocket closed",  err)      
                self.socketDisconnect(client.websocket)
        if future != None:        
            future.set_result('sent!')
    #----------------------------------------------------------------------------------
        
    """ 
    
    Changes made to /usr/local/lib/python3.5/dist-packages/websockets/protocol.py 
    
    """
    def pongReceived(self, thisSJClient, frame):
        print("Pong Received", frame)
        dataRow = None
        [pongIP, pongPort] = frame.replace("{","").replace("}","").split(":")
        cursor = self.mySQL_Connector.acquire_db_lock()
        retryTransaction = 3
        while retryTransaction > 0:    
            try:
                ret = cursor.execute("""UPDATE sj_userlist SET pong = 'HERE' WHERE ip = '%s' AND portTCP = '%s'"""%(pongIP, pongPort))
                #dataRow = cursor.fetchone()
            except MySQLdb.Error as e:
                self.mySQL_Connector.exceptionHandling( "UPDATE FEHLER BEI Pong Received", e)  
                retryTransaction -= 1  
                cursor = self.mySQL_Connector.acquire_db_lock()
            retryTransaction = 0
        self.mySQL_Connector.release_db_lock()
    #----------------------------------------------------------------------------------
        
    async def processTextMessage(self, sjClient, frame ): 
        json_msg = json.loads( json.dumps( {"type":"None"} ), encoding="utf-8")
        try:        
            """ JSON MESSAGE ENTPACKEN """
            json_msg = json.loads(frame, encoding="utf-8")
        except json.decoder.JSONDecodeError as err:
            #print("No Text Message, trying Pong")
            try:        
                self.pongReceived(sjClient, frame)
            except Exception as e:
                print("No Text Message, no Pong")
                return
        
        dataRow = None  
        peer = sjClient.getPeerInfo( )
        cursor = self.mySQL_Connector.acquire_db_lock()        
        if json_msg['type'] == "Login":
            ownName = json_msg['ownName']
            ownUDPPort = json_msg['ownUDPPort']
            ownUDPPort2 = json_msg['ownUDPPort2']
            retryTransaction = 3
            while retryTransaction > 0:    
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET name ='%s', portUDP = '%s', portUDP2 = '%s' WHERE ip = '%s' AND portTCP = '%s'"""
                                   %( ownName, ownUDPPort, ownUDPPort2, peer[0], peer[1] ) )
                    if not ret:
                        self.mySQL_Connector.sqlDB.rollback()
                        print( "UPDATE FEHLER BEI LOGIN" )
                        retryTransaction -= 1  
                    else:
                        self.mySQL_Connector.sqlDB.commit()
                        retryTransaction = 0
                        retryTransaction2 = 3
                        while retryTransaction2 > 0:    
                            #print( "AUSLESEN DER ID FÜR DIESEN DATENSATZ, UM DEN FERTIGEN DATENSATZ DANACH AN ALLE USER ZU VERSENDEN" )
                            try:
                                ret = cursor.execute("""SELECT id FROM sj_userlist WHERE name='%s'"""%(ownName) )
                                dataRow = cursor.fetchall()
                                if not ret:
                                    print( "SELECT FEHLER BEI LOGIN" )
                                    retryTransaction2 -= 1  
                                else:
                                    self.mySQL_Connector.sqlDB.commit()
                                    for row in dataRow:
                                        """VERSENDEN DES DATENSATZES (NAME,IP,PORT,PORT_UDP,SJ-ID) AN ALLE"""
                                        dataDict = {"type":"system", 
                                                    "message":"Userlist update", 
                                                    "action":"Add user", 
                                                    "remoteName":ownName,
                                                    "remoteIP":peer[0], 
                                                    "remotePort":peer[1], 
                                                    "remoteUDPPort":ownUDPPort, 
                                                    "remoteUDPPort2":ownUDPPort2, 
                                                    "remoteID":row[0], 
                                                    "ownIP":peer[0],
                                                    "ownPort":peer[1]}                        
                                        await self.send_reply( dataDict, print_message=True )   
                                    retryTransaction2 = 0   
              
                            except MySQLdb.Error as e:
                                self.mySQL_Connector.exceptionHandling( "SELECT FEHLER BEI LOGIN", e)
                                retryTransaction2 -= 1  
                                cursor = self.mySQL_Connector.acquire_db_lock()
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE FEHLER BEI LOGIN", e)
                    retryTransaction -= 1                    
                    cursor = self.mySQL_Connector.acquire_db_lock()
                    
                
        elif json_msg['type'] == "Chat":
            ownName = json_msg['ownName']
            userMessage = json_msg['message']
            userColor = json_msg['color']
            dataDict = {"type":"usermsg", 
                        "ownName":ownName, 
                        "message":userMessage, 
                        "color":userColor}
            await self.send_reply( dataDict, print_message=True )  
                        
        elif json_msg['type'] == "Set-Soundcard-Status":
            soundIsRunning = json_msg['soundIsRunning']
            retryTransaction = 3
            while retryTransaction > 0:    
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET audio = '%s' WHERE ip = '%s' AND portTCP = '%s'"""
                                   %( soundIsRunning, peer[0], peer[1] ) )
                    if not ret:
                        self.mySQL_Connector.sqlDB.rollback()
                        print( "UPDATE PROBLEM: SETZEN DES SOUNDCARD STATUS - ID Check" )
                        retryTransaction -= 1  
                    else: 
                        self.mySQL_Connector.sqlDB.commit()
                        retryTransaction = 0
                        retryTransaction2 = 3
                        while retryTransaction2 > 0:    
                            try:
                                ret = cursor.execute("""SELECT id FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""
                                               %( peer[0], peer[1] ) )
                                dataRow = cursor.fetchone()
                                if not ret:
                                    print( "SELECT PROBLEM: SETZEN DES SOUNDCARD STATUS" )
                                    retryTransaction2 -= 1  
                                else:
                                    dataDict = {"type":"system", 
                                                "message":"Audio Status Update", 
                                                "action":"Update Audio Status", 
                                                "audioStatus":soundIsRunning, 
                                                "remoteID":dataRow[0], 
                                                "ownIP":peer[0],
                                                "ownPort":peer[1]}
                                    await self.send_reply( dataDict, print_message=True )  
                                    retryTransaction2 = 0
                            except MySQLdb.Error as e:
                                self.mySQL_Connector.exceptionHandling( "SELECT PROBLEM: SETZEN DES SOUNDCARD STATUS", e)
                                retryTransaction2 -= 1  
                                cursor = self.mySQL_Connector.acquire_db_lock()
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: SETZEN DES SOUNDCARD STATUS", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
    
        elif json_msg['type'] == "Set-App-Status":
            appStatus = json_msg['appStatus']
            retryTransaction = 3
            while retryTransaction > 0:    
                try:
                    print("UPDATE sj_userlist SET audio = '%s' WHERE ip = '%s' AND portTCP = '%s'" %( appStatus, peer[0], peer[1] ) )
                    ret = cursor.execute("""UPDATE sj_userlist SET audio = '%s' WHERE ip = '%s' AND portTCP = '%s'"""
                                   %( appStatus, peer[0], peer[1] ) )
                    if not ret:
                        print( "UPDATE PROBLEM: SETZEN DES APP STATUS - ID Check Step 1" )
                        retryTransaction -= 1  
                    else:
                        retryTransaction = 0
                        retryTransaction2 = 3
                        while retryTransaction2 > 0:    
                            try:
                                ret = cursor.execute("""SELECT id FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""
                                               %( peer[0], peer[1] ) )
                                dataRow = cursor.fetchone()
                                if not ret:
                                    print( "SELECT PROBLEM: SETZEN DES APP STATUS - ID Check Step 2" )
                                    retryTransaction2 -= 1  
                                else:
                                    dataDict = {"type":"system", 
                                                "message":"App Status Update", 
                                                "action":"Update App Status", 
                                                "audioStatus":appStatus, 
                                                "remoteID":dataRow[0], 
                                                "ownIP":peer[0],
                                                "ownPort":peer[1]}
                                    await self.send_reply( dataDict, print_message=True ) 
                                    retryTransaction2 = 0 
                            except MySQLdb.Error as e:
                                self.mySQL_Connector.exceptionHandling( "SELECT PROBLEM: SETZEN DES APP STATUS", e)
                                retryTransaction2 -= 1  
                                cursor = self.mySQL_Connector.acquire_db_lock()
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: SETZEN DES APP STATUS", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
    
        elif json_msg['type'] == "Connect":    
            remoteIP = json_msg['remoteIP']
            remotePortTCP = json_msg['remotePortTCP']
            dataDict = {"type":"system", 
                        "message":"Connect %s:%s to %s:%s" %(peer[0], peer[1], remoteIP, remotePortTCP), 
                        "action":"Connect", 
                        "remoteIP":peer[0], 
                        "remotePort":peer[1], 
                        "ownIP":remoteIP,
                        "ownPort":remotePortTCP}
#                        "ownIP":peer[0], 
#                        "ownPort":peer[1], 
#                        "remoteIP":remoteIP,
#                        "remotePort":remotePortTCP}
            await self.send_reply( dataDict, print_message=True )  
                
        elif json_msg['type'] == "Disconnect":
            remoteIP = json_msg['remoteIP']
            remotePortTCP = json_msg['remotePortTCP']
            dataDict = {"type":"system", 
                        "message":"Disconnect %s:%s to %s:%s" %(peer[0], peer[1], remoteIP, remotePortTCP), 
                        "action":"Disconnect", 
                        "remoteIP":peer[0], 
                        "remotePort":peer[1], 
                        "ownIP":remoteIP,
                        "ownPort":remotePortTCP}
            await self.send_reply( dataDict, print_message=True )  
                
        elif json_msg['type'] == "connectionACK":
            remoteIP = json_msg['remoteIP']
            remotePortTCP = json_msg['remotePort']
            yesno = json_msg['yesno']
            dataDict = {"type":"system", 
                        "message":"connection ACK received", 
                        "action":"connectionACK", 
                        "remoteIP":peer[0], 
                        "remotePort":peer[1], 
                        "ownIP":remoteIP,
                        "ownPort":remotePortTCP,
                        "yesno":yesno}
            await self.send_reply( dataDict, print_message=True )  
                    
        elif json_msg['type'] == "UDP-Port-Update":
            ownUDPPort = json_msg["ownUDPPort"];
            ownUDPPort2 = json_msg["ownUDPPort2"];
            nat = json_msg["NAT"];
            print("NAT: %s"%nat)
            """NAT-TYPE IN JOS-USERLIST SCHREIBEN"""  
            retryTransaction = 3
            while retryTransaction > 0:                   
                try:
                    ret = cursor.execute("""SELECT name FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""%( peer[0], peer[1] ))
                    dataRow = cursor.fetchone()
                    print( ">>>>>>>>>>>>>>>>> NAT DATAROW: ", dataRow)
                    
                    if not ret:
                        self.mySQL_Connector.sqlDB.rollback()
                        print("PROBLEM: AUSLESEN DES NAMENS AUS SJ-USERLIST")
                        retryTransaction -= 1  
                    else:
                        self.mySQL_Connector.sqlDB.commit()
                        retryTransaction = 0  
                        retryTransaction2 = 3
                        while retryTransaction2 > 0:    
                            try:#"""UPDATE sj_userlist SET audio = '%s' WHERE ip = '%s' AND portTCP = '%s'"""
                                print("""UPDATE jos_users SET NAT = '%s' WHERE username = '%s'"""%( nat, dataRow[0] ))
                                ret = cursor.execute("""UPDATE jos_users SET NAT = '%s' WHERE username = '%s'"""%( nat, dataRow[0] ))
                                if not ret:
                                    self.mySQL_Connector.sqlDB.rollback()
                                    print("PROBLEM: NAT-UPDATE")
                                    retryTransaction2 -= 1  
                                else:
                                    self.mySQL_Connector.sqlDB.commit()
                                    retryTransaction2 = 0  
                            except MySQLdb.Error as e:
                                self.mySQL_Connector.exceptionHandling( "PROBLEM: NAT-UPDATE", e)
                                retryTransaction2 -= 1  
                                cursor = self.mySQL_Connector.acquire_db_lock()
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: AUSLESEN DES NAMENS AUS SJ-USERLIST", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
                
            """PORTS IN SJ-USERLIST SCHREIBEN UND INFO VIA WEBSOCKET VERTEILEN"""    
            retryTransaction = 3
            while retryTransaction > 0:    
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET portUDP = '%s',portUDP2 = '%s',portUDP3 = '%s' WHERE ip = '%s' AND portTCP = '%s'"""%( ownUDPPort, ownUDPPort2, nat, peer[0], peer[1] ))
                    if not ret:
                        self.mySQL_Connector.sqlDB.rollback()
                        print("PROBLEM: SETZEN DER NEUEN UDP-PORTS")
                        retryTransaction -= 1  
                    else:
                        retryTransaction = 0  
                        retryTransaction2 = 3
                        while retryTransaction2 > 0:    
                            try:
                                ret = cursor.execute("""SELECT id FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""%( peer[0], peer[1] ))
                                dataRow =  cursor.fetchone()
                                if not ret:
                                    print("PROBLEM: SETZEN DER NEUEN UDP-PORTS")
                                    retryTransaction2 -= 1  
                                else:
                                    dataDict = {"type":"system", 
                                                "message":"UDP port update", 
                                                "action":"Update UDP port", 
                                                "remoteUDPPort":ownUDPPort, 
                                                "remoteUDPPort2":ownUDPPort2, 
                                                "remoteUDPPort3":nat,
                                                "remoteID":dataRow[0], 
                                                "ownIP":peer[0],
                                                "ownPort":peer[1]}
                                    await self.send_reply( dataDict, print_message=True )
                                    retryTransaction2 = 0  
                            except MySQLdb.Error as e:
                                self.mySQL_Connector.exceptionHandling( "PROBLEM: SETZEN DER NEUEN UDP-PORTS", e)
                                retryTransaction2 -= 1  
                                cursor = self.mySQL_Connector.acquire_db_lock()
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: AUSLESEN DES NAMENS AUS SJ-USERLIST", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
                
        elif json_msg['type'] == "UDP-Port-Increment":
            remoteID = json_msg['remoteID']
            countDown = json_msg['countDown']     
            retryTransaction = 3
            while retryTransaction > 0:    
                try:
                    #ret = cursor.execute("""SELECT name FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""%( peer[0], peer[1] ))
                    ret = cursor.execute("""SELECT ip,portTCP,id FROM sj_userlist""")
                    #print( dataRow )
                    #ret = cursor.execute("""SELECT ip,portTCP FROM sj_userlist WHERE id = '%s'"""% remoteID)
                    if not ret:
                        print("PROBLEM: UDP PORT INCREMENT - ID CHECK")
                        retryTransaction -= 1  
                    else:
                        dataRow = cursor.fetchall()
                        print( dataRow,  remoteID ,  json_msg['remoteID'])
                        for row in dataRow:
                            print( row[2],  remoteID,  json_msg['remoteID'] )
                            if row[2] == remoteID:
                                print("Increase @ Peer-IP %s Port %s UDP Port %d"%( row[0], row[1],  sjClient.getUDPPort([row[0], row[1]]) ))
            #                    foundPeer = sjClient.startCurrentUDPPort([dataRow[0][0], dataRow[0][1]],  50000)
            #                    if foundPeer and int(countDown) > 0:
            #                        sjClient.incrementUDPPort( [dataRow[0][0], dataRow[0][1]] )
            #                    elif foundPeer and int(countDown) == 0:
            #                        sjClient.removeCurrentUDPPort( [dataRow[0][0], dataRow[0][1]] )
            #                    else:
            #                        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>should not be reached!")
                                dataDict = {"type":"system", 
                                            "message":'%s requests portchange of ID: %s ("%s")' %( peer[0], remoteID, countDown ), 
                                            "action":"Port up", 
                                            "remoteIP":peer[0],
                                            "remotePort":peer[1], 
                                            "ownIP":dataRow[0], 
                                            "ownPort":dataRow[1] }
                                await self.send_reply( dataDict,   )  
                        retryTransaction = 0  
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: UDP PORT INCREMENT - ID CHECK", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
            
        elif json_msg['type'] == "Set-Current-UDP-Send-Port":
            id = json_msg['id']
            currentUDPPort = json_msg['currentUDPPort']    
            retryTransaction = 3
            while retryTransaction > 0:     
                try:
                    #ret = cursor.execute("""SELECT name FROM sj_userlist WHERE ip = '%s' AND portTCP = '%s'"""%( peer[0], peer[1] ))
                    ret = cursor.execute("""SELECT ip,portTCP FROM sj_userlist WHERE id = '%s'"""% remoteID)
                    dataRow = cursor.fetchall()
                    if not ret:
                        print("PROBLEM: SET CURRENT UDP SEND PORT")
                        retryTransaction -= 1  
                    else:
                        print("Send new UDP Port from: %s Port %s to: %s"%( dataRow[0], dataRow[1], currentUDPPort ))
                        dataDict = {"type":"system", 
                                    "message":"", 
                                    "action":"Set-Current-UDP-Send-Port", 
                                    "remoteIP":peer[0],
                                    "remotePort":peer[1], 
                                    "ownIP":dataRow[0][0], 
                                    "ownPort":dataRow[0][1],
                                    "currentUDPPort":currentUDPPort}
                        await self.send_reply( dataDict, print_message=True )  
                        retryTransaction = 0 
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: SET CURRENT UDP SEND PORT", e)
                    retryTransaction -= 1  
                    cursor = self.mySQL_Connector.acquire_db_lock()
                
        elif json_msg['type'] == "Set-Soundcard-Config":            
            inputIndex = json_msg['inputIndex']
            outputIndex = json_msg['outputIndex']     
            channels = json_msg['channels']
            frameSize = json_msg['frameSize']
            localVolume = json_msg['localVolume']
            frameSizeSend = json_msg['frameSizeSend']
            codecQuality = json_msg['codecQuality']
            callAnswerMode = json_msg['callAnswerMode']
            configMode = json_msg['configMode']
            joomlaID = json_msg['joomlaID']
            print("ID: %s >>>>>>>>>>>> IN: %s OUT: %s callAnswerMode: %s configMode: %s"%( joomlaID,  inputIndex, outputIndex, callAnswerMode, configMode ))
            print("UPDATE jos_users SET inputIndex = '%s', outputIndex = '%s', channels = '%s', frameSize = '%s', frameSizeSend = '%s', quality = '%s', callAnswerMode = '%s', configMode = '%s'  WHERE id = '%s'"
                               %( inputIndex, outputIndex, channels, frameSize, frameSizeSend, codecQuality, callAnswerMode, configMode, joomlaID ))
            retryTransaction = 3
            while retryTransaction > 0:
                try:
                    ret = cursor.execute("""UPDATE jos_users SET inputIndex = '%s', outputIndex = '%s', channels = '%s', frameSize = '%s', frameSizeSend = '%s', quality = '%s', callAnswerMode = '%s', configMode = '%s'  WHERE id = '%s'"""
                                   %( inputIndex, outputIndex, channels, frameSize, frameSizeSend, codecQuality, callAnswerMode, configMode, joomlaID ))
                    if not ret:
                        self.mySQL_Connector.sqlDB.rollback()
                        print("PROBLEM: SETTING SOUNDCARD-CONFIG") 
                        retryTransaction -= 1 
                    else:
                        self.mySQL_Connector.sqlDB.commit()
                        print("Set Soundcard-Config at Joomla-ID: %s"%( joomlaID ))
    #                     for client in self.clients:
    #                         remotePeer = client.getPeerInfo()
    #                         dataDict = {"type":"system", 
    #                                     "message":"", 
    #                                     "action":"Set-Current-UDP-Send-Port", 
    #                                     "remoteIP":remotePeer[0], 
    #                                     "remotePort":remotePeer[1], 
    #                                     "ownIP":peer[0],
    #                                     "ownPort":peer[1],
    #                                     "currentUDPPort":currentUDPPort}
    #                            await self.send_reply( client, dataDict )  
                        retryTransaction = 0
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: SETTING SOUNDCARD-CONFIG", e)   
                    retryTransaction -= 1          
                    cursor = self.mySQL_Connector.acquire_db_lock()
    
        elif json_msg['type'] == "Get-Soundcard-Config":            
            joomlaID = json_msg['joomlaID']   
            retryTransaction = 3
            while retryTransaction > 0:         
                try:
                    cursor.execute("""SELECT inputIndex,outputIndex,channels,frameSize,localVolume,frameSizeSend,quality,callAnswerMode FROM jos_users WHERE id='%s'"""
                                   %( joomlaID ))
                    dataRow = cursor.fetchone()
                    if not ret:
                        print("PROBLEM: LESEN DER SOUNDCARD PARAMETER")
                        retryTransaction -= 1          
                    else:
                        """HIER NEUE VARIABLEN EINFÜHREN - SO IST ES IM MOMENT IMPROVISIERT"""
                        inputIndex = dataRow[0]
                        outputIndex = dataRow[1]
                        channels = dataRow[2]
                        frameSize = dataRow[3]
                        frameSizeSend = dataRow[5]
                        codecQuality = dataRow[6]
                        callAnswerMode = dataRow[7]
                        retryTransaction = 0
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "PROBLEM: LESEN DER SOUNDCARD PARAMETER", e)
                    retryTransaction -= 1          
                    
            print("IN: %s OUT: %S callAnswerMode: %s configMode: %s"%( inputIndex, outputIndex, callAnswerMode, configMode ))
            dataDict = {"type":"system",
                        "message":"ID %s received soundcard settings"%( joomlaID ),
                        "action":"Update soundcard settings",        
                        "ownIP":peer[0],
                        "ownPort":peer[1],    
                        "inputIndex":inputIndex,
                        "outputIndex":outputIndex,
                        "channels":channels,
                        "frameSize":frameSize,
                        "localVolume":0,
                        "frameSizeSend":frameSizeSend,
                        "codecQuality":codecQuality,
                        "callAnswerMode":callAnswerMode}
            await self.send_reply( dataDict, print_message=True )  
            
        elif json_msg['type'] == "ACK":
            dataDict = {"type":"system", 
                        "message":"ACK: %s %s" %(peer[0], peer[1]), 
                    "action":"none"}
            await self.send_reply( dataDict, print_message=True )  
                
        elif json_msg['type'] == "HEARTBEAT":               
            dataDict = {"type":"system", 
                        "message":"none", 
                        "action":"HEARTBEAT"}
            await self.send_reply( dataDict, print_message=True )  
                
        self.mySQL_Connector.release_db_lock()
    #----------------------------------------------------------------------------------
#========================================================================================

class PingPongTimeout(threading.Thread):
    def __init__(self, __sjServer, mySQL_Connector):
        threading.Thread.__init__(self, daemon = True)
        self.loop = asyncio.get_event_loop()
        self.__sjServer = __sjServer
        self.mySQL_Connector = mySQL_Connector                        
        self.mySQL_Connector.getDBDescription("sj_userlist")
    #----------------------------------------------------------------------------------
        
    def run(self):
        self.pingPongTimeout(self.__sjServer)
        self.loop.close()
    #----------------------------------------------------------------------------------
    
    @asyncio.coroutine    
    def send_ping(self, __websocket, peer):
        yield from __websocket.ping("%s:%s"%(peer[0], peer[1]))
    #----------------------------------------------------------------------------------
        
    def pingPongTimeout(self, __sjServer):
        print("Init PingPong Timer")
        dataRow = None
        while True:
            time.sleep(7)
            cursor = self.mySQL_Connector.acquire_db_lock()
            
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET pong = 'NOPE_4' WHERE pong = 'NOPE_3'""")
                    if not ret:
                        self.mySQL_Connector.sqlDB.commit()
                        print( "FAILED NOPE_3 AUF NOPE_4 GESETZT" )
                        retryTransaction -= 1       
                    else:
                        self.mySQL_Connector.sqlDB.rollback()  
                        print( "NOPE_3 AUF NOPE_4 GESETZT" )
                        retryTransaction = 0         
                except  MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: BEIM SETZEN VON NOPE_3 AUF NOPE_4", e)
                    retryTransaction -= 1         
                    cursor = self.mySQL_Connector.acquire_db_lock()
            
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET pong = 'NOPE_3' WHERE pong = 'NOPE_2'""")
                    if not ret:
                        self.mySQL_Connector.sqlDB.commit()
                        print( "FAILED NOPE_2 AUF NOPE_3 GESETZT" )
                        retryTransaction -= 1    
                    else:
                        self.mySQL_Connector.sqlDB.rollback()
                        print( "NOPE_2 AUF NOPE_3 GESETZT" )  
                        retryTransaction = 0        
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: BEIM SETZEN VON NOPE_2 AUF NOPE_3", e)
                    retryTransaction -= 1   
                    cursor = self.mySQL_Connector.acquire_db_lock()
             
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""UPDATE sj_userlist SET pong = 'NOPE_2' WHERE pong = 'NOPE'""")
                    if not ret:
                        self.mySQL_Connector.sqlDB.commit()
                        print( "FAILED NOPE AUF NOPE_2 GESETZT" )
                        retryTransaction -= 1   
                    else:
                        self.mySQL_Connector.sqlDB.rollback()
                        print( "NOPE AUF NOPE_2 GESETZT" )
                        retryTransaction = 0          
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: BEIM SETZEN VON NOPE AUF NOPE_2", e)
                    retryTransaction -= 1   
                    cursor = self.mySQL_Connector.acquire_db_lock()
        
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""SELECT ip,portTCP FROM sj_userlist WHERE pong = 'NOPE_3'""")
                    dataRow = cursor.fetchall()
                    #print("NOPE3 CHECK: ", dataRow)
                    if not ret:
                        print( "FAILED CHECK3" )
                        retryTransaction -= 1        
                    else:
                        print( "CHECK3", dataRow )
                        retryTransaction = 0           
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "SELECT PROBLEM: CHECK3 FAILED", e)
                    retryTransaction -= 1   
                    cursor = self.mySQL_Connector.acquire_db_lock()
        
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""SELECT ip,portTCP FROM sj_userlist WHERE pong = 'NOPE_2'""")
                    dataRow =  cursor.fetchall()
#                    print("NOPE2 CHECK: ", dataRow)
                    if not ret:
                        print( "FAILED CHECK2" )  
                        retryTransaction -= 1      
                    else:
                        print( "CHECK2" , dataRow)
                        retryTransaction = 0         
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "SELECT PROBLEM: CHECK2 FAILED", e)
                    retryTransaction -= 1   
                    cursor = self.mySQL_Connector.acquire_db_lock()
        
            retryTransaction = 3
            while retryTransaction > 0: 
                try:
                    ret = cursor.execute("""SELECT ip,portTCP FROM sj_userlist WHERE pong = 'NOPE_4'""")
                    if not ret:
                        print("FAILED CHECK4")
                        retryTransaction -= 1   
                    else:
                        dataRow = cursor.fetchall()
                        print("NOPE4 CHECK: ", dataRow)
                        for row in dataRow:
                            deleteIP = row[0]
                            deletePort = row[1]
                        
                            for client in __sjServer.clients:
                                peer = client.getPeerInfo(  )   
                                if deleteIP == peer[0] and deletePort == peer[1]:
                                    print("PONG EVENTUALLY GONE --> DELETED IP: %s PORT: %s"%(deleteIP, deletePort))
                                    __sjServer.socketDisconnect(client.websocket)
                        retryTransaction = 0     
                except MySQLdb.Error as e:
                    self.mySQL_Connector.exceptionHandling( "SELECT PROBLEM:  ip,portTCP WHERE pong = 'NOPE_4'", e)
                    retryTransaction -= 1   
                    cursor = self.mySQL_Connector.acquire_db_lock()
                
            print( __sjServer.clients )
            
            for client in __sjServer.clients:    
                peer = client.getPeerInfo(  )  
                retryTransaction = 3
                while retryTransaction > 0:                     
                    try:
                        ret = cursor.execute("""UPDATE sj_userlist SET pong = 'NOPE' WHERE pong = 'HERE' AND ip = '%s' AND portTCP = '%s'""" %( peer[0],peer[1] ) )
                        if not ret: 
                            self.mySQL_Connector.sqlDB.rollback()
                            retryTransaction -= 1   
                        else:
                            self.mySQL_Connector.sqlDB.commit()
                            retryTransaction = 0     
                    except MySQLdb.Error as e:
                        self.mySQL_Connector.exceptionHandling( "UPDATE PROBLEM: PONG KONNTE NICHT AUF FALSE GESETZT WERDEN", e)
                        retryTransaction -= 1   
                        cursor = self.mySQL_Connector.acquire_db_lock()
                        
                """ping the peer"""          
                print("PING: %s" %peer)
                asyncio.run_coroutine_threadsafe( self.send_ping(client.websocket, peer), loop=self.loop )
                       
            self.mySQL_Connector.release_db_lock()
    #----------------------------------------------------------------------------------
#========================================================================================

    
class MyWebsocket(threading.Thread):    
    def __init__(self, __sjServer, listenSocket):
        threading.Thread.__init__(self, daemon = True)
        self.__sjServer = __sjServer
        self.loop = asyncio.get_event_loop() 
        self.listenSocket = listenSocket
    #----------------------------------------------------------------------------------

    async def waiting_for_timeout(self, future):
        while True:
            await asyncio.sleep(8)
    #----------------------------------------------------------------------------------
    
    async def serverLoopWebsockets(self, websocket, path):
#         __sjServer = getSjServer()
        print("serverLoop", self.__sjServer)
        if len(self.__sjServer.clients) == 0:
            self.__sjServer.onNewConnection( websocket )
        else: 
            foundClient = False
            for client in self.__sjServer.clients:
                print(client.getPeerInfo())
                if websocket == client.websocket:
                    foundClient = True
            if foundClient:
                print("Client already present")
                return
            else:
                self.__sjServer.onNewConnection( websocket )
        thisSJClient = None
        for client in self.__sjServer.clients:
            if websocket == client.websocket:
                thisSJClient = client
        if thisSJClient is None:
            print("SJ Client not created, exiting...")
            return
        print("start server loop")
        while True:
            try:
                frame = await websocket.recv()
            except websockets.exceptions.ConnectionClosed as err:
                print("[Receive] Websocket Exception, Websocket closed",  err) 
                self.__sjServer.socketDisconnect(websocket)
                return
            if frame is None:
                continue
            else:            
                """ 
                
                Returning Pong Frame modified in /usr/local/lib/python3.5/dist-packages/websockets/protocol.py 
                
                """
                #print(type(frame), frame)
                await self.__sjServer.processTextMessage( thisSJClient, frame)
    #---------------------------------------------------------------------------------- 
    
    def run(self):
        self.run_websockets(self.__sjServer, self.listenSocket)
    #---------------------------------------------------------------------------------- 
        
    def run_websockets(self, __sjServer, listenSocket):
        print("prepare SSL")
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.check_hostname = False
#        ssl_context.load_cert_chain('server.crt', 'server.key')
        start_server = websockets.serve(self.serverLoopWebsockets, listenSocket[0], listenSocket[1], loop=self.loop)#, ssl = ssl_context)
        print("start websocket server")             
        self.loop.run_until_complete(start_server)
        try:
            self.loop.run_forever()
        finally:
            self.loop.close()
    #----------------------------------------------------------------------------------
    
#========================================================================================

if __name__ == "__main__":
    print("test soundjack server")     
    mySQL_Connector = MyMySQL()
    sjServer = SJServer(mySQL_Connector, listenSocket[1], None) 
    
    pingPongTimer = PingPongTimeout(sjServer, mySQL_Connector)
    pingPongTimer.start()
    
    websocketsServer = MyWebsocket(sjServer, listenSocket)
    websocketsServer.start()
    
    websocketsServer.join()
    pingPongTimer.join()
    print("end")
#----------------------------------------------------------------------------------
