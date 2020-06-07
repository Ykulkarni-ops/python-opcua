from opcua import Server
from opcua import ua
from random import randint
from firebase import Firebase
from datetime import timedelta
# from opcua.server.history_sql import HistorySQLite
import time
import  datetime
import sys
sys.path.insert(0, "..")
import csv 

server = Server()
# adding the trust certificate 
url= 'opc.tcp://127.0.0.1:8080'
server.set_endpoint(url)
server.set_security_policy([ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt])
server.load_certificate('certificate-example.der')
server.load_private_key('private-key-example.pem')
uri = "http://examples.freeopcua.github.io"

#adding the namesapce for the nodes and generating the nodes
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()
#generating the parameters 
param = node.add_object(addspace,"Parameter")

iTemp = param.add_variable(addspace,"Temperature",0)
iPress = param.add_variable(addspace,'Pressure',0)
iflow=param.add_variable(addspace,'Flow',0)
Time = param.add_variable(addspace,'Time',0)

iTemp.set_writable()
iPress.set_writable()
iflow.set_writable()
Time.set_writable()
#adding data to history to be viewed later 
# server.iserver.history_manager.set_storage(HistorySQLite('firebaseConfig.sql'))

#starting the server 
server.start()
#historizinng the data
#server.historize_node_data_change(iTemp,period=None,count=1000)
#server.historize_node_data_change(iPress,period=None,count=1000)
#server.historize_node_data_change(iflow,period=None,count=1000)
# firebaseConfig = {
#     # 'apiKey': "AIzaSyCg3wC6dEyr10uclBn2SAEDttYeyu7blsk",
#     # 'authDomain': "crwn-db-dffe3.firebaseapp.com",
#     # 'databaseURL': "https://crwn-db-dffe3.firebaseio.com",
#     # 'projectId': "crwn-db-dffe3",
#     # 'storageBucket': "crwn-db-dffe3.appspot.com",
#     # 'messagingSenderId': "611614610213",
#     # 'appId': "1:611614610213:web:fc705e91b267d2f31b40cc"
#     'apiKey': "AIzaSyAvheAqKVkBCCtCZUzRy3AjTZcf8kWLhp8",
#     'authDomain': "rdmpro-ba669.firebaseapp.com",
#     'databaseURL': "https://rdmpro-ba669.firebaseio.com",
#     'projectId': "rdmpro-ba669",
#     'storageBucket': "rdmpro-ba669.appspot.com",
#     'messagingSenderId': "869898311250",
#     'appId': "1:869898311250:web:523a550062395213df718b"
# }

# firebase = Firebase(firebaseConfig)
# db = firebase.database()
print(f'Server started at {url}')

# def historize_data(data):
with open('historyAccess_server.csv',mode='a', newline='') as historyAccess:
    fieldnames= ['Temperature','Pressure','Flow','Time']
    thewriter = csv.DictWriter(historyAccess,fieldnames=fieldnames)
    thewriter.writeheader()
    while True:
        Temperature = randint(10,50)
        Pressure = randint(200,999)
        Flow=randint(500,1200)
        # TIME = datetime.datetime.now()
        TIME=time.strftime("%D  %H:%M:%S")

        print(f'Temperature is: {Temperature}')
        print(f'Pressure is:{Pressure}')
        print(f'Flow is:{Flow}')
        print(f'Time is : {TIME}')
        iTemp.set_value(Temperature)
        iPress.set_value(Pressure)
        iflow.set_value(Flow)
        Time.set_value(TIME)
        # data={
        # 'iTemp':Temperature,
        # 'iPress': Pressure,
        #     'iflow': Flow,
        #     'Time': TIME
        #     }
        thewriter.writerow(
            {'Temperature':Temperature, 'Pressure': Pressure ,'Flow': Flow,'Time': TIME}
        )
        # db.child('values').push(data)
        # historize_data(data)
        
        
    # time delay additon 
        time.sleep(2)

        
        
#conditions for displaying the random values for the server









