from opcua import Client
from firebase import Firebase
import csv
import time
# url and security 
url= 'opc.tcp://127.0.0.1:8080'
client = Client(url)
client.set_security_string("Basic256Sha256,SignAndEncrypt,certificate-example.der,private-key-example.pem") # add "server" certificate.dem file and private-key.pem file (Beckhoff_OpcUaServer.der,Beckhoff_OpcUaServer.pem)
client.application_uri = "urn:example.org:FreeOpcUa:python-opcua" # use the uri of the server. (urn:BeckhoffAutomation:TcOpcUaServer)

# client connection 
client.connect()
print('CLIENT CONNECTED SUCCESSFULLY')
# firebase initialization 
firebaseConfig = {
   3 here the firebase configuration should be entered
}

firebase = Firebase(firebaseConfig)
db = firebase.database()
with open('historyAccess_client.csv',mode='a', newline='') as historyAccess:
    fieldnames= ['Temperature','Pressure','Flow','Time']
    thewriter = csv.DictWriter(historyAccess,fieldnames=fieldnames)
    thewriter.writeheader()
    while True:
        iTemp = client.get_node('ns=2;i=3')         
        Temperature = iTemp.get_value()
        print(f'Temperature is: {Temperature}')

        iprssure = client.get_node('ns=2;i=2')          
        Pressure = iprssure.get_value()
        print(f'Pressure is:{Pressure}')   

        iflow = client.get_node('ns=2;i=4')                 
        Flow = iflow.get_value()
        print(f'Flow is :{Flow}')

        TIME = client.get_node('ns=2;i=5')
        TIME_Value = TIME.get_value()
        # TIME_Value= TIME_Value
        TIME_firebase= str(TIME_Value)
        TIME_csv=TIME_Value
        print(f'Time is : {TIME_Value}')
        # sending data to firebase
        data={
            'iTemp':Temperature,
            'iPress': Pressure,
            'iflow': Flow,
            'Time': TIME_firebase
        }
        db.child('values').push(data)
        thewriter.writerow(
            {'Temperature':Temperature, 'Pressure': Pressure ,'Flow': Flow,'Time': TIME_csv}
        )
        time.sleep(2)
