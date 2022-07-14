import os
import time
import paho.mqtt.client as mqtt
from libraries.docker_log import log_info

mqtt_host = os.getenv('MQTT_HOST', '192.168.1.15')
broker_port = os.getenv('BROKER_PORT', '1883')
have_credentials = os.getenv('USE_CREDENTIALS', 'NO')
user_name = os.getenv('USER_NAME', '')
password = os.getenv('PASSWORD', '')

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        log_info("MQTT OK!")
    else:
        log_info("MQTT FAILURE. ERROR CODE: " + rc)

def settingUpMQTT():
    mqtt.Client.connected_flag=False
    clientMQTT = mqtt.Client()
    clientMQTT.on_connect=on_connect 
    clientMQTT.loop_start()
    log_info("Connecting to MQTT broker: " + mqtt_host)
    log_info("Port: " + broker_port)
    if have_credentials == "YES":
        clientMQTT.username_pw_set(username=user_name, password=password)
    clientMQTT.connect(mqtt_host, int(broker_port), 60) 
    while not clientMQTT.connected_flag: 
        log_info("...")
        time.sleep(1)
    log_info("START MODBUS...")
    return clientMQTT

def connect():
    clientMQTT = settingUpMQTT()
    return clientMQTT