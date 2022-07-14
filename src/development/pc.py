'''
Info from the project
'''

code_mode = 'PC' #Possibilities: 'PC', 'RASP' and 'TEST'
data_mode = 'TEST_FILE' #Possibilites: 'TEST_FILE' and 'INVERTER'

import time
from library.base_solar import HuaweiSolar
import library.base_solar as base_solar
import paho.mqtt.client as mqtt
import os
import logging
import json

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

def main():

    log.info("||| STARTING PC MODE |||")
    def on_connect(client, userdata, flags, rc):
        time.sleep(10)
        log.info(f"Connected with result code {rc}")
        
    client = mqtt.Client()
    client.on_connect = on_connect
    #client.username_pw_set(username="raspberrypie", password="rasp1234") #How to use credentials
    client.connect("192.168.100.108", 1883, 60) #Mosquitto comunication

    for i in range(10000):

        # Sending a JSON
        data = {"sepalLength": "6.4","sepalWidth":  "3.2","petalLength": "4.5","petalWidth":  "1.5"}
        print(json.dumps(data))
        data = json.dumps(data)
        client.publish('raspberryTopic', payload=data, qos=0,
        retain=False)
        log.info(f"send {i} to raspberryTopic")

        #A info
        # client.publish('raspberryTopic', payload=json, qos=0,
        # retain=False)
        # log.info(f"send {i} to raspberryTopic")
        time.sleep(10)

    client.loop_forever()
    return 0




