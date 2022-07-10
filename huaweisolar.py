'''
import time
from base_solar import HuaweiSolar
import base_solar
import paho.mqtt.client as mqtt
import os

import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

inverter_port = os.getenv('INVERTER_PORT', '/dev/ttyUSB0')
mqtt_host = os.getenv('MQTT_HOST', '192.168.1.15')
broker_port = os.getenv('BROKER_PORT', '1883')

inverter = base_solar.HuaweiSolar(inverter_port, slave=1)
inverter._slave = 1
inverter.wait = 1


#vars = ['state_1','state_2', 'state_3', 'alarm_1', 'alarm_2', 
#'alarm_3', 'pv_01_voltage', 'pv_01_current', 'pv_02_voltage',
#'pv_02_current', 'input_power', 'grid_voltage', 
#'grid_current', 'day_active_power_peak', 'active_power', 
#'reactive_power', 'grid_frequency', 'efficiency', 
#'internal_temperature', 'insulation_resistance', 'device_status', 
#'fault_code', 'startup_time', 'shutdown_time', 
#'accumulated_yield_energy', 'daily_yield_energy', 'grid_A_voltage', 
#'active_grid_A_current', 'power_meter_active_power', 
#'grid_exported_energy', 'grid_accumulated_energy']

#vars = ['alarm_1', 'pv_01_voltage', 'pv_01_current', 'pv_02_voltage',
#'pv_02_current', 'input_power', 'grid_voltage', 'grid_current', 
#'day_active_power_peak', 'active_power', 'reactive_power', 
#'grid_frequency', 'efficiency', 'internal_temperature', 
#'insulation_resistance', 'device_status', 'fault_code', 'startup_time', 
#'shutdown_time', 'accumulated_yield_energy', 'daily_yield_energy', 
#'grid_A_voltage', 'active_grid_A_current', 'power_meter_active_power', 
#'grid_exported_energy', 'grid_accumulated_energy']

def on_connect(client, userdata, flags, rc):
    
    if rc==0:
        client.connected_flag=True
        log.info("MQTT OK!")
    else:
        log.info("MQTT FAILURE. ERROR CODE: %s",rc)

def settingUpMQTT():

    mqtt.Client.connected_flag=False
    clientMQTT = mqtt.Client()
    clientMQTT.on_connect=on_connect 
    clientMQTT.loop_start()
    log.info("Connecting to MQTT broker: %s ", mqtt_host)
    log.info("AQUI 0")
    #clientMQTT.username_pw_set(username="", password="")
    log.info("AQUI 1")
    clientMQTT.connect(mqtt_host, 1883, 60) 
    log.info("AQUI 2")
    while not clientMQTT.connected_flag: 
        log.info("...")
    time.sleep(1)
    log.info("START MODBUS...")

    return clientMQTT


def modbusAccess(clientMQTT):

    vars_immediate = ['pv_01_voltage', 'pv_01_current', 'pv_02_voltage',
    'pv_02_current', 'input_power', 'grid_voltage', 
    'grid_current', 'active_power', 
    'grid_A_voltage', 'active_grid_A_current',
    'power_meter_active_power']

    vars_calculated = ['day_active_power_peak', 'efficiency', 
    'internal_temperature', 'insulation_resistance', 'device_status', 
    'fault_code', 'accumulated_yield_energy',
    'daily_yield_energy', 'grid_exported_energy', 
    'grid_accumulated_energy']

    cont = 0
    while True:
        
        log.info("--> Started transmission")
        for i in vars_immediate:
            try:
                mid = inverter.get(i)
                log.info(i)
                log.info(mid)

                #clientMQTT.publish(topic="emon/NodeHuawei/"+i, 
                #payload= str(mid.value), qos=1, retain=False)
            except:
                pass

        if(cont > 0):
            for i in vars_calculated:
                try:
                    mid = inverter.get(i)
                    log.info(i)
                    log.info(mid)

                    #clientMQTT.publish(topic="emon/NodeHuawei/"+i, 
                    #payload= str(mid.value), qos=1, retain=False)
                except:
                    pass
            cont = 0

        cont = cont + 1 
        log.info("--> Ended transmission") 
        # time.sleep(300) # 5min
        time.sleep(15) # 15seg

#clientMQTT = settingUpMQTT()
#modbusAccess(clientMQTT)

#clientMQTT = ""
#modbusAccess(clientMQTT)

# clientMQTT.loop_stop()
'''

#TEST
'''
import paho.mqtt.client as mqtt
import time
import logging

FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

def on_connect(client, userdata, flags, rc):
    time.sleep(10)
    log.info(f"Connected with result code {rc}")

client = mqtt.Client()
client.on_connect = on_connect
#client.username_pw_set(username="raspberrypie", password="rasp1234")
#client.connect("7497a8feacd44088b913f9341d61a918.s1.eu.hivemq.cloud", 8883, 60) #Comunicação mosquitto

# client.connect("192.168.100.108", 1883, 60) #Comunicação mosquitto
for i in range(10000):
    client.publish('raspberryTopic', payload=str(i), qos=0,
    retain=False)
    log.info(f"send {i} to raspberryTopic")
    time.sleep(10)

client.loop_forever()
'''

