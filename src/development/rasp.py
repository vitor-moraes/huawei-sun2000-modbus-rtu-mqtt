import os
import time
import json
from libraries.docker_log import log_for_me
from development.connection.mqtt import connect
from development.data.inverter_data import IMMEDIATE_VARS, CALCULATED_VARS, get_data

def main(data_mode):
    log_for_me("||| STARTING RASP MODE |||")

    # def modbusAccess(clientMQTT):
    #     cont = 0
    #     while True:
    #         log_for_me("--> Started transmission")
    #         for i in IMMEDIATE_VARS:
    #             try:
    #                 mid = get_data(i)
    #                 log_for_me(i)
    #                 log_for_me(mid)
    #                 #clientMQTT.publish(topic="emon/NodeHuawei/"+i, 
    #                 #payload= str(mid.value), qos=1, retain=False)
    #             except:
    #                 pass
    #         if(cont > 0):
    #             for i in CALCULATED_VARS:
    #                 try:
    #                     mid = get_data(i)
    #                     log_for_me(i)
    #                     log_for_me(mid)
    #                     #clientMQTT.publish(topic="emon/NodeHuawei/"+i, 
    #                     #payload= str(mid.value), qos=1, retain=False)
    #                 except:
    #                     pass
    #             cont = 0
    #         cont = cont + 1 
    #         log_for_me("--> Ended transmission") 
    #         # time.sleep(300) # 5min
    #         time.sleep(15) # 15seg

    def get_solar_data():
        data = {}
        if data_mode == 'INVERTER':
            data = {"Index": 0,"Type": "Inverter"}
            data = json.dumps(data)
        else:
            data = {"Index": 1,"Type": "Offline"}
            data = json.dumps(data)
        return data
    
    client = connect()
    while True:
        data = get_solar_data()
        client.publish('raspberryTopic', payload=data, qos=0, retain=False)
        log_for_me(f"send to raspberryTopic")
        time.sleep(10)

    client.loop_forever()
    return 0




