'''
Info from the project
'''

code_mode = 'PC' #Possibilities: 'PC', 'RASP' and 'TEST'
data_mode = 'TEST_FILE' #Possibilites: 'TEST_FILE' and 'INVERTER'

import time
import paho.mqtt.client as mqtt
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

def main():
        log.info("||| STARTING TEST MODE |||")
        def on_connect(client, userdata, flags, rc):
                time.sleep(10)
                log.info(f"Connected with result code {rc}")
        
        client = mqtt.Client()
        client.on_connect = on_connect
        #client.username_pw_set(username="raspberrypie", password="rasp1234") #How to use credentials
        #client.connect("192.168.100.108", 1883, 60) #Mosquitto comunication

        for i in range(10000):
                client.publish('raspberryTopic', payload=str(i), qos=0,
                retain=False)
                log.info(f"send {i} to raspberryTopic")
                time.sleep(10)

        client.loop_forever()
        return 0



