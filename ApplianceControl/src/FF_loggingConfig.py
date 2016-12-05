# Config file for attribute logging script
# Make sure USB is inserted and joined to the wanted network
# Enter BM node Id below.
import FF_zigbeeClusters as zbc

# Logging on/off and name of logfile to use.  Data is appended to that file.
loggingOn=True
logfile='/Users/keith/Google Drive/Python/attribute-logs/test-log1.txt'
firmwareRootFilePath = '/Users/Keith/Google Drive/Projects & Suppliers/Hive/firmware-release-notes/'

# nodes & endpoints
node1 = 'A87D'
#node1 = '9B73'
#node1 = '1C05'
ep1 = '05'
ep1b = '06'
 
node2 = '5E78'
#ep1 = '09'

tstat_heat_attrs =  [('0000','0001','003C'),
                     ('0012','0001','0708'),
                     ('001C','0001','0708'),                 
                     ('0023','0001','0708'),
                     ('0024','0001','0708'),
                     ('0029','0001','0708')]

tstat_water_attrs = [('001C','0001','0708'),
                     ('0023','0001','0708'),
                     ('0024','0001','0708'),
                     ('0029','0001','0708')]

bg_clust_attrs    = [('0020','0001','0708'),
                     ('0021','0001','0708'),
                     ('0022','0001','0708'),
                     ('0023','0001','0708'),
                     ('0024','0001','0708'),
                     ('0025','0001','0708'),                 
                     ('0026','0001','0708'),                   
                     ('0031','0001','0708')]

attrReports = [{'nodeId':node1,'epId':'05','clustName':'Thermostat Cluster', 'attrs':tstat_heat_attrs},
               {'nodeId':node1,'epId':'06','clustName':'Thermostat Cluster', 'attrs':tstat_water_attrs},
               {'nodeId':node1,'epId':'05','clustName':'BG Cluster', 'attrs':bg_clust_attrs}]

#temp_log_attrs = [('0000','0000','003C')]
#attrReports = [{'nodeId':node1,'epId':'05','clustName':'Thermostat Cluster', 'attrs':temp_log_attrs},
#               {'nodeId':node2,'epId':'05','clustName':'Thermostat Cluster', 'attrs':temp_log_attrs}]


# Serial Port Parameters
PORT = '/dev/tty.SLAB_USBtoUART'
BAUD = 19200

def bindTest(myNode):
    
    heat0201 =  [('0000','003C','0000'),
                 ('0012','0001','0708'),
                 ('001C','0001','0708'),                 
                 ('0023','0001','0708'),
                 ('0024','0001','0708'),
                 ('0029','0001','0708')]
    
    water0201 = [('0000','0000','FFFF'),
                 ('0012','0001','FFFF'),
                 ('001C','0001','0708'),
                 ('0023','0001','0708'),
                 ('0024','0001','0708'),
                 ('0029','0001','0708')]
    
    heatFD00  = [('0020','0001','0708'),
                 ('0021','0001','0708'),
                 ('0022','0001','0708'),
                 ('0023','0001','0708'),
                 ('0024','0001','0708'),
                 ('0025','0001','0708'),                 
                 ('0026','0001','0708'),
                 ('0027','0001','FFFF'),                 
                 ('0028','0001','FFFF'),
                 ('0029','0001','FFFF'),                    
                 ('0031','0001','0708')]
    
    heat0000  = [('0010','0001','FFFF')]
    

#     heat0201 =  [('0000','0001','003C'),
#                  ('0012','0001','0000'),
#                  ('001C','0001','0000'),                 
#                  ('0023','0001','0000'),
#                  ('0024','0001','0000'),
#                  ('0029','0001','0000')]
#      
#     water0201 = [('0000','0000','FFFF'),
#                  ('0012','0001','FFFF'),
#                  ('001C','0001','0000'),
#                  ('0023','0001','0000'),
#                  ('0024','0001','0000'),
#                  ('0029','0001','0000')]
#      
#     heatFD00  = [('0020','0001','0000'),
#                  ('0022','0001','0000'),
#                  ('0023','0001','0000'),
#                  ('0024','0001','0000'),
#                  ('0025','0001','0000'),                 
#                  ('0026','0001','0000'),
#                  ('0027','0001','FFFF'),                 
#                  ('0028','0001','FFFF'),
#                  ('0029','0001','FFFF'),                    
#                  ('0031','0001','0000')]
#      
#     heat0000  = [('0010','0001','FFFF')] 
    
    
    t = [{'ep':'05','clust':'Basic Cluster','attrs':heat0000},
         {'ep':'05','clust':'Thermostat Cluster', 'attrs':heat0201},
         {'ep':'05','clust':'BG Cluster', 'attrs':heatFD00},
         {'ep':'06','clust':'Thermostat Cluster', 'attrs':water0201}]
    
    
    # Get the node addresses
    AT.startSerialThreads(PORT, BAUD, printStatus=False)
    _, mySrcAddr = AT.getEUI(myNode, myNode)
    _, myDstAddr = AT.getEUI('0000', '0000')

    # Setup bindings
    for b in t:
        print(b['ep'])
        mySrcEp=b['ep']
        myDstEp='01'
        myCluster,_ = zbc.getClusterNameAndId(b['clust'])
        AT.setBinding(myNode, mySrcAddr, mySrcEp, myCluster, myDstAddr, myDstEp)    
    
    # Setup Reporting
    for b in t:
        for a in b['attrs']:
            myEp=b['ep']
            myClustId,_=zbc.getClusterNameAndId(b['clust'])
            myAttrId=a[0]
            minRep=a[1]
            maxRep=a[2]
            changeRep=getChangeRep(myClustId,myAttrId)
            AT.debug=True
            respState,respVal = AT.setAttributeReporting(myNode, myEp, myClustId, myAttrId, minRep, maxRep, changeRep)
            if not respState:
                print(respState,respVal)
    
    return

def getChangeRep(myClust,myAttr):
    """ Build the word for minimum reportable change.
        Digital Attrs -> None
        Analogue Attrs -> One zero per nibble e.g. 1byte = 00
        
    """
    _,_,attrType = zbc.getAttributeNameAndId(myClust, myAttr)
    AorD = zbc.dataTypes[attrType]['type']
    nibbles = zbc.dataTypes[attrType]['nibbles']
    if AorD == 'A':
        changeRep='0' * nibbles
    elif AorD == 'D':
        changeRep= ''
    return changeRep
    
# Main Program Starts

if __name__ == "__main__":
    
    # Only import this if we are the main module (to prevent circular reference)
    import src.FF_threadedSerial as AT

    print("**** Logging Configuration")
    print("")
    print("LoggingOn = {}".format(loggingOn))
    print("Port      = {}".format(PORT))
    print("Baud      = {}".format(BAUD))
    print("Firmware  = {}".format(firmwareRootFilePath))
    print("Logfile   = {}".format(logfile))
    print("")

    # Print the nodes/endpoints/clusters/attributes and reporting configuration
    # Build a list of dicts containing the details for each attribute report config
    configList = []
    for node in attrReports:
        myNode = node['nodeId']
        myEp = node['epId']
        myClust=node['clustName']
        
        print("NodeId={0}, EP={1}, Clust={2}".format(myNode,myEp,myClust))

        attrs = node['attrs']
        # Print the clusters/attributes
        for attr in attrs:
            attrId = attr[0]
            minRep = attr[1]
            maxRep = attr[2]            
            changeRep = getChangeRep(myClust, attrId)
            _,attrName,_ = zbc.getAttributeNameAndId(myClust,attrId)
            print('    {},{:35},{},{},{}'.format(attrId,attrName,minRep,maxRep,changeRep))
            
            #nodeId, epId, clustId, attr, minRep, maxRep, changeRep
            clustId,_ = zbc.getClusterNameAndId(myClust)
            configList.append({'nodeId':myNode,
                               'epId':myEp,
                               'clustId':clustId,
                               'attrId':attrId,
                               'minRep':minRep,
                               'maxRep':maxRep,
                               'changeRep':changeRep})
        
        print("")
    
    # Setup bindings and attribute reporting
    i = input("Do you want to setup bindings and attribute reporting on these attributes? y/n ")
    if i.upper()=='Y':
        
        AT.startSerialThreads(PORT, BAUD, printStatus=False)
        AT.debug=True
        AT.getInitialData(node1, fastPoll=True, printStatus=True)
 
        print('Starting binding/reporting setup:')
        
        # Set required bindings
        for node in attrReports:
            nodeId = node['nodeId']
            epId = node['epId']
            clustId,_ = zbc.getClusterNameAndId(node['clustName'])
            print('Setting binding on {0},{1},{2}'.format(nodeId,epId,clustId))
            
            # Setup a binding
            _, _, mySrcAddr = AT.getEUI(nodeId, nodeId)
            _, _, myDstAddr = AT.getEUI('0000', '0000')
            respState, _, respValue = AT.setBinding(nodeId, mySrcAddr, epId, clustId, myDstAddr, '01')
            if respState==False:
                print('Binding failed: ',respState,respValue)

        # Set attribute reporting on each attribute
        for attr in configList:
            respState,_,respValue = AT.setAttributeReporting(attr['nodeId'],
                                                             attr['epId'],
                                                             attr['clustId'],
                                                             attr['attrId'],
                                                             attr['minRep'],
                                                             attr['maxRep'],
                                                             attr['changeRep'])
            if respState==False:
                print('Setting attribute reporting failed: ',respState,respValue)
                
    print('All Done') 