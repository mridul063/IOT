#!/usr/bin/python

############################################ 
# PROBLEM STATEMENT:
# This program will publish test mqtt messages using the AWS IOT hub
# 
#
############################################

############################################
# STEPS:
#
# 1. Sign in to AWS Amazon > Services > AWS IoT > Settings > copy Endpoint
#    This is your awshost
# 
# 2. Change following things in the below program:
#    a. awshost   (from step 1)
#    b. clientId  (Thing_Name)
#    c. thingName (Thing_Name)
#    d. caPath    (root-CA_certificate_Name)
#    e. certPath  (<Thing_Name>.cert.pem)
#    f. keyPath   (<Thing_Name>.private.key)
# 
# 3. Paste aws_iot_pub.py & aws_iot_sub.py python scripts in folder where all aws key files are kept. 
# 5. Run publisher.py script
#
############################################

# importing libraries
import paho.mqtt.client as paho
import ssl
from time import sleep
from random import uniform
from datetime import datetime
 
connflag = False
 
def on_connect(client, userdata, flags, rc):                # func for making connection
    global connflag
    print("Connected to AWS")
    connflag = True
    #if connection is successful, rc value will be 0
    print("Connection returned result: " + str(rc) )
    #print(flags)
 
def on_message(client, userdata, msg):                      # Func for Sending msg
    print(msg.topic+" "+str(msg.payload))
 
#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))
 
mqttc = paho.Client()    
#create an mqtt client object
#attach call back function
mqttc.on_connect = on_connect
#attach on_connect function written in the
#mqtt class, (which will be invoked whenever
#mqtt client gets connected with the broker)
#is attached with the on_connect function
#written by you.


mqttc.on_message = on_message                               # assign on_message func
#attach on_message function written inside
#mqtt class (which will be invoked whenever
#mqtt client gets a message) with the on_message
#function written by you

#### Change following parameters #### 
awshost = "a9cy15eymz2p8-ats.iot.ap-south-1.amazonaws.com"      # Endpoint
awsport = 8883                                              # Port no.   
clientId = "temperature-sensor"                                     # Thing_Name
thingName = "temperature-sensor"                                    # Thing_Name
caPath = "AmazonRootCA1.pem" #Amazon's certificate from Third party                                     # Root_CA_Certificate_Name
certPath = "3cc3aa0b5fdddf1ca19e542a8447f84fd43f44edd46cd41a331c733ed1379cfa-certificate.pem.crt"   # <Thing_Name>.cert.pem.crt. Thing's certificate from Amazon
keyPath = "3cc3aa0b5fdddf1ca19e542a8447f84fd43f44edd46cd41a331c733ed1379cfa-private.pem.key"        # <Thing_Name>.private.key Thing's private key from Amazon
 
mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)  # pass parameters
 
mqttc.connect(awshost, awsport, keepalive=60)               # connect to aws server
 
mqttc.loop_start()                                          # Start the loop
 
while 1:
    sleep(5)
    if connflag == True:
        timeStamp = datetime.now()
        tempreading = uniform(20.0,25.0)                        # Generating Temperature Readings
        message = '{"timeStamp":"'+str(timeStamp)+'",'+'"temperature":'+str(tempreading)+'}'
        mqttc.publish("temperatureTopic", message, 1)        # topic: temperature # Publishing Temperature values
        print("msg sent: temperature " + "%.2f" % tempreading ) # Print sent temperature msg on console
        #print(message)
    else:
        print("waiting for connection...")                      
