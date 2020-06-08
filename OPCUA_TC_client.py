from opcua import Client
from firebase import Firebase
import csv
import time
import datetime
# url and security 
url= 'opc.tcp://7.110.226.20:4840'
client = Client(url)
client.set_security_string("Basic256Sha256,SignAndEncrypt,Beckhoff_OpcUaServer.der,Beckhoff_OpcUaServer.pem") # add "server" certificate.dem file and private-key.pem file (Beckhoff_OpcUaServer.der,Beckhoff_OpcUaServer.pem)
client.application_uri = "urn:BeckhoffAutomation:TcOpcUaServer" # use the uri of the server. (urn:BeckhoffAutomation:TcOpcUaServer)

# client connection 
client.connect()
print('CLIENT CONNECTED SUCCESSFULLY')
# firebase initialization 
firebaseConfig = {
   #the firebase database configuration goes here
}

firebase = Firebase(firebaseConfig)
db = firebase.database()
with open('historyAccess_client.csv',mode='a', newline='') as historyAccess:
    fieldnames= ['Temperature','Pressure','Flow','Time']
    thewriter = csv.DictWriter(historyAccess,fieldnames=fieldnames)
    thewriter.writeheader()
    while True:
        iTemp = client.get_node('ns=4;s=MAIN.iTemp')         
        Temperature = iTemp.get_value()
        print(f'Temperature is: {Temperature}')

        iprssure = client.get_node('ns=4;s=MAIN.iprssure')     
        Pressure = iprssure.get_value()
        print(f'Pressure is:{Pressure}')   

        iflow = client.get_node('ns=4;s=MAIN.iflow')                 
        Flow = iflow.get_value()
        print(f'Flow is :{Flow}')
        print(datetime.datetime.now())
        # TIME = client.get_node('ns=4;s=MAIN.TIME')
        # TIME_Value = TIME.get_value()
        # # TIME_Value= TIME_Value
        # TIME_firebase= str(TIME_Value)
        # TIME_csv=TIME_Value
        # print(f'Time is : {TIME_Value}')
        # sending data to firebase
        data={
            'iTemp':Temperature,
            'iPress': Pressure,
            'iflow': Flow,
            # 'Time': TIME_firebase
        }
        db.child('values').push(data)
        thewriter.writerow(
            {'Temperature':Temperature, 'Pressure': Pressure ,'Flow': Flow}
        )
        time.sleep(2)
