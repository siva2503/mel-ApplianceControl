#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import os
import time

import FF_loggingConfig as config
import FF_threadedSerial as AT
import FF_zigbeeClusters as zcl
            
def setOnOff(strOnOff = 'ON',myNodeId = None):
    """ turn device on/off with periods.
    
    """
    strSPCurrentStatus = getOnOff(myNodeId) 
    if  strSPCurrentStatus == "ON" and strOnOff =="ON":
#         RerporterFile.Reporter.report_pass('The Appliance is already in ON condition')
        print("inside already on")
        return
    elif strSPCurrentStatus == "OFF" and strOnOff =="OFF":
#         RerporterFile.Reporter.report_pass('The Appliance is already in ON condition')
        print("inside already off")
        return
    
    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    if 'ON' in strOnOff.upper():
        AT.onOff(myNodeId, '09','0', '1')
        intSPOnTime = int(time.time())
    else: 
        AT.onOff(myNodeId, '09','0', '0')
        intSPOffTime = int(time.time()) 
    
    AT.stopThreads()
    
    
def getSPConsumption(myNodeId = None):
    """ Get the consumption recorded in the smart plug.
    """
    
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    
    myEP = '09'
    sendMode = '0'
    myClust = '0702'
    myAttr = '0000'
    myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(myNodeId,myEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(myNodeId,
                                                                      myEP,
                                                                      myClust,
                                                                      myAttr, '00')]
        
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)
    print(respValue, 'respValue')
    
    AT.stopThreads()
    intHexaConsumption =  respValue.split(',')[len(respValue.split(','))-1]
    if intHexaConsumption!= "000000000000":
        intHexaConsumption = intHexaConsumption.lstrip('0')
    intDecimalConsumption = int(intHexaConsumption,16)
    print(intHexaConsumption," after hexa decimal conversion ",intDecimalConsumption)
    return intDecimalConsumption
    
def getOnOff(myNodeId = None):
    """ Gets the status of Smart plug. On or Off!!
    """
    
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    myEP = '09'
    sendMode = '0'
    myClust = '0006'
    myAttr = '0000'
    myMsg = 'AT+READATR:{0},{1},{2},{3},{4}'.format(myNodeId,myEP,sendMode,myClust,myAttr)             
    
    expectedResponse=['RESPATTR:{0},{1},{2},{3},{4},(..)'.format(myNodeId,
                                                                      myEP,
                                                                      myClust,
                                                                      myAttr, '00')]
        
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)

    print(respValue, 'respValue')
    
    AT.stopThreads()
    intStatusAttribute = respValue.split(',')[len(respValue.split(','))-1]
    
    if intStatusAttribute == "00":
        strStatusAttribute = "OFF"
    elif intStatusAttribute == "01":
        strStatusAttribute = "ON"
        
    return strStatusAttribute
    
    
def resetSmartPlug(myNodeId = None):
    """ Resets the smart plug to its initial state. this will wipe the consumption earlier recorded.
    """

    AT.stopThread.clear()  
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    if myNodeId is None: myNodeId = discoverNodeIDbyCluster('0006')[2]
    
    myEP = '09'
    myAttr = '0000'
    intResetRequired = '010000'
    myMsg = 'AT+RAWZCL:{0},{1},{2},{3}'.format(myNodeId,myEP,myAttr,intResetRequired)             
    
    expectedResponse=['OK']
        
    respValue = AT.sendCommand(myMsg, expectedResponse)

    print(respValue, 'respValue')
    
    AT.stopThreads()
    
    
def connectToTrilliantZUD(myNodeId = None):
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myMsg = 'ATI'
    expectedResponse=['OK']
    respValue = AT.sendCommand(myMsg, expectedResponse)
    print(respValue, 'respValue')
    AT.stopThreads()
    
def initiateIPAN(strCommsHub):
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myMsg = 'ATI'
    expectedResponse=['OK']
    respValue = AT.sendCommand(myMsg, expectedResponse)
    print(respValue, 'respValue')
    AT.stopThreads()

    
def sendCADCommissioningCommands(myNodeId = None):
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myMsg = 'ATI'
    expectedResponse=['OK']
    respValue = AT.sendCommand(myMsg, expectedResponse)
    print(respValue, 'respValue')
    AT.stopThreads()
    
def startDevicePair(myNodeId = None):
    AT.stopThread.clear()
    AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
    myMsg = 'ATI'
    expectedResponse=['OK']
    respValue = AT.sendCommand(myMsg, expectedResponse)
    print(respValue, 'respValue')
    AT.stopThreads()
    

# def setBind(myNodeId, myEndPoint,  hexClusterID, boolZigbee = None):
#     """ Repeatedly turn device on/off with given periods.
#     """
#     if boolZigbee is None:
#         if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
#         else: boolZigbee = True
#             
#     if not boolZigbee:
#         AT.stopThread.clear()  
#         AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
#         AT.startAttributeListener(printStatus=False)
#         AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
#         
#     # Setup a binding
#     _, _, mySrcAddr = AT.getEUI(myNodeId, myNodeId)
#     _, _, myDstAddr = AT.getEUI('0000', '0000')
#     respState, respCode, respValue = AT.setBinding(myNodeId, mySrcAddr, myEndPoint, hexClusterID, myDstAddr, '01')
#     print(respState, respValue)
#     '''if respState: status = "PASS"
#     else: status = "FAIL"
#     if not respCode == '00':
#         status = respCode'''
#     status = respCode
#     if not boolZigbee: AT.stopThreads()
#     return status, mySrcAddr + "$$" + myEndPoint + "$$" + hexClusterID + "$$" + myDstAddr + "$$" + '01' 
# 
# def setUnBind(myNodeId, myEndPoint,  hexClusterID, boolZigbee = None):
#     """ Repeatedly turn device on/off with given periods.
#     """
#     if boolZigbee is None:
#         if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
#         else: boolZigbee = True
#             
#     if not boolZigbee:
#         AT.stopThread.clear()  
#         AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
#         AT.startAttributeListener(printStatus=False)
#         AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
#         
#     # Setup a binding
#     _, _, mySrcAddr = AT.getEUI(myNodeId, myNodeId)
#     _, _, myDstAddr = AT.getEUI('0000', '0000')
#     respState, respCode, respValue = AT.setUnBind(myNodeId, mySrcAddr, myEndPoint, hexClusterID, myDstAddr, '01')
#     print(respState, respValue)
#     if respState: status = "PASS"
#     else: status = "FAIL"
#     
#     if not boolZigbee: AT.stopThreads()
#     return mySrcAddr + "$$" + myEndPoint + "$$" + hexClusterID + "$$" + myDstAddr + "$$" + '01' + "$$" + status
# 
# def getBind(myNodeId, boolZigbee = None):
#     """ Repeatedly turn device on/off with given periods.
#     """
#     if boolZigbee is None:
#         if not 'ZIGBEE' in getAttribute('common', 'apiValidationType').upper(): boolZigbee = False
#         else: boolZigbee = True
#             
#     if not boolZigbee:
#         AT.stopThread.clear()  
#         AT.startSerialThreads(config.PORT, config.BAUD, printStatus=False)
#         AT.startAttributeListener(printStatus=False)
#         AT.getInitialData(myNodeId, fastPoll=True, printStatus=True)
#         
#     #Get the bindings
#     respState, _, respValue = AT.getBindings(myNodeId)
#     #print(respState, respValue)
#     if not boolZigbee: AT.stopThreads()
#     return respValue

def getNtable(myNodeId):
    
    """  Retrieve neighbor table for the given nodeId
    
    """
    msg = ''
    if myNodeId.upper() == 'FF':
        expectedResponse = ['NTable:{0},(..)'.format('0000')]
    else: expectedResponse = ['NTable:{0},(..)'.format(myNodeId)]
    
    finished = False
    tableRow=0
    rows=[]
    headersDone = False
    
    while not finished:
        
        # Typical Response.
        # BTable:0000,00
        # Length:03
        # No. | SrcAddr | SrcEP | ClusterID | DstAddr | DstEP
        # 0. | 000D6F000059474E | 01 | DEAD |1234567887654321 | 12
        # 1. | 000D6F000059474E | 01 | DEAD |E012345678876543 | E0
        # 2. | 000D6F000059474E | 01 | DEAD | ABCD 
        # ACK:01    
        
        # Read a page of the table
        hexIndex = '%02x' % tableRow
        msg = "AT+NTABLE:{},{}".format('00', myNodeId)
        respState, respCode, respValue = AT.sendCommand(msg, expectedResponse)
        if (not respState) or (respCode!=zcl.statusCodes['SUCCESS']):
            print("Error with binding table read : ",respValue)
            exit()
        header1 = respValue
        
        # Extract the table length    
        header2 = AT.rxQueue.get()
        print(header2)
        if not header2.startswith('Length'):
            print("Error with binding table read - expected 'Length' ",header2)
            exit()
        tableLength = int(header2.split(':')[1],16)
        
        # Read the table header row (only if there are more than zero bindings)
        if tableLength>0:
            header3 = AT.rxQueue.get()
            if not header3.startswith('No.'):
                print("Error with binding table read - Expected 'No.' ", header3)
                exit()
        else:
            header3 = None
        
        if not headersDone:
            rows.append(header1)
            rows.append(header2)
            rows.append(header3)
            headersDone = True
        
        if tableLength == 0:
            finished = True
        else:
            # Read the binding rows            
            pageRow=0
            while pageRow<3 and tableRow<tableLength:
                row=AT.rxQueue.get()
                if int(row.split('|')[0].strip('. '))!=tableRow:
                    print("Error with binding table read - Row number mismatch.")
                    exit()
                tableRow+=1
                pageRow+=1
                #print(row)
                rows.append(row)
                
        if tableRow>=tableLength:
            finished = True
                
    return respState, respCode, rows

def discoverNodeIDbyCluster(nodeSpecificAttribute):
    """ Returns the Node ID of Related to the Cluster
    """
    myMsg = 'AT+DISCOVER:{0}'.format(nodeSpecificAttribute)
    expectedResponse = ['DEV:(..)']
    # DEV:C58A,09
    
    respState, respCode, respValue = AT.sendCommand(myMsg, expectedResponse)

    if respState:
        resp = respValue.split(',')
        resp = resp[0].split(':')[1]
    else:
        resp = respValue
    return respState,respCode,resp

def getAllClustersAttributes(myNodeId, strNodeName):
    """ Uses discoverEndpoints, discoverClusters, discoverAttributes and READATTR to query all
        attribute values on the device and print a summary.
        
        Also recovers any reporting intervals for the attribute
        
        Print the Endpoint list
        Print the Clusters
        Print the Attribute values and Reporting Intervals
        
    """
    
    strEnvironmentFolderPAth = os.path.abspath(__file__ + "/../../../../") + "/02_Manager_Tier/EnviromentFile/"        
    strNodeClustAttrPath = strEnvironmentFolderPAth + '/nodes_clusters_attributes.json'    
    strJson = open(strNodeClustAttrPath, mode='r')
    oNCAJsonDict = json.loads(strJson.read())
    strJson.close() 
    
    oLstNodes = oNCAJsonDict["nodes"]["list_of_nodes"]
    oLstNodes[strNodeName] = {}
    oNode = oLstNodes[strNodeName]
    oNode["node_id"] = myNodeId
    oNode["list_of_endpoints"] = {}
    
    # Retrieve and display the endpoints
    respState,respCode,endpoints = AT.discEndpoints(myNodeId)
    if respState and respCode==zcl.statusCodes['SUCCESS']:
        print("Endpoints: {0}".format(endpoints))
    else:
        print('Error finding endpoints')
        
    # Loop through each endpoint for clusters and attributes
    for ep in endpoints:
        # Discover all clusters on this endpoint
        oNode["list_of_endpoints"][ep] = {}
        oNode["list_of_endpoints"][ep]["list_of_clusters"] = {}
        
        respState,respCode,respValue = AT.discClusters(myNodeId,ep)
        if respState and respCode==zcl.statusCodes['SUCCESS']:
            clusterList = AT.buildClusterList(respValue)
        else:
            print('Problem with Cluster Discovery: ',respValue)
            exit()
        
        for clust in clusterList:
            clustId, clustName = zcl.getClusterNameAndId(clust[1])
            clustType = clust[0]          
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId] = {}
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["cluster_name"] = clustName
            oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"] = {}
            
            
            print("\nEndpoint={0}, Cluster={1},{2},{3}".format(ep, clust[1], clustName, clustType))

            respState,respCode,respValue =AT.discAttrs(myNodeId,ep,clustId,clustType)
            if respState and respCode==zcl.statusCodes['SUCCESS']:
                for attr in respValue:
                    attrId = attr[0]
                    attrType = attr[1]
                    _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clustId,attrId)
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId] = {}
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId]["attrbute_name"] = zclAttrName
                    oNode["list_of_endpoints"][ep]["list_of_clusters"][clustId]["list_of_attributes"][attrId]["attrbute_type"] = zclAttrType
                    '''
                    # Get the attribute value
                    respState,respCode,respVal = AT.getAttribute(myNodeId, ep, clustId, attrId, clustType)
                    if respState and respCode==zcl.statusCodes['SUCCESS']:
                        if respVal=='86':
                            print('{0},Unsupported attribute'.format(attr[0]))
                            attrReport = 'Reporting not retrieved'                                
                        else:
                            attrVal = respVal
                            
                            # Get the reporting intervals for the attribute
                            respStatus,respCode,attrReport = AT.getAttributeReporting(myNodeId, ep, clustId, clustType, attrId)
                            if not respStatus:
                                attrReport = "Problem reading reporting config. {}".format(attrReport)
                            if respStatus and respCode!=zcl.statusCodes['SUCCESS']:
                                attrReport = "Problem reading reporting config. {}".format(zcl.lookupStatusCode(respCode))
                            # Get the attribute name from my library module
                            _, zclAttrName, zclAttrType = zcl.getAttributeNameAndId(clust    Id,attrId)
                            print("{0},{1},{2:32},{3:20},{4}".format(attrId, attrType, zclAttrName, attrVal,attrReport))
                            if attrType != zclAttrType: print("TYPE ERROR in zigbeeCluster Library !!!!!!!!!!!!!!!")
                    
                    else:
                        print("Problem finding attribute value")
                        exit()'''

            else:
                print("Problem with attribute discovery: ", respValue)
                exit()
                
    oNCAJsonDict["nodes"]["list_of_nodes"][strNodeName] = oNode
    
    #Write back the JSON to the GlobalVar.JSON
    oJson = open(strNodeClustAttrPath, mode='w+')
    oJson.write(json.dumps(oNCAJsonDict, indent=4, sort_keys=False))
    oJson.close()
    return 0

if __name__ == '__main__':
    pass

