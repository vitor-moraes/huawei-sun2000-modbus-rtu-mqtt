'''
Info
'''
import time
import json
from libraries.docker_log import log_for_me
from connection.mqtt import connect
from data.inverter_data import IMMEDIATE_VARS, CALCULATED_VARS, get_data

DATA_MODE = 'INVERTER' #Possibilites: 'OFFLINE' and 'INVERTER'
TOPIC = 'raspberryTopic'

def send_data(client, storable_data):
    try:
        client.publish(TOPIC, payload=storable_data, qos=0, retain=False)
    except:
        log_for_me('ERROR PUBLISHING DATA TO MQTT BROKER')

def format_data_to_serialized_json(info):
    log_for_me(info)
    data = {
                'ID': 0,
                'Valor': 0,
                'Aplicacao': 0,
                'Local': 0,
                'Tipo': 0,
                'Variavel': 0,
                'Unidade': 0,
                'Rede': 0,
                'Professor': 0
            }
    serialized_data = json.dumps(data)
    return serialized_data

def get_solar_data(variable):
    if DATA_MODE == 'INVERTER':
        return get_data(variable)
    else:
        log_for_me('To develop offiline data')
        return '???'

def pick_up_and_send_inverter_data(client):
    log_for_me("--> Started transmission")
    log_for_me("Getting Immediate variables")
    for imm_var in IMMEDIATE_VARS:
        try:
            imm_response = get_solar_data(imm_var)
            log_for_me(imm_var + ' | ' + str(imm_response))
            json = format_data_to_serialized_json({'variable': imm_var, 'response': imm_response})
            send_data(client, json)
        except:
            pass
    log_for_me("Getting calculated variables")
    for cal_var in CALCULATED_VARS:
        try:
            cal_response = get_solar_data(cal_var)
            log_for_me(cal_var + ' | ' + str(cal_response))
            json = format_data_to_serialized_json({'variable': cal_var, 'response': cal_response})
            send_data(client, json)
        except:
            pass
    log_for_me("--> Ended transmission") 

client = connect()
# --> add here function to wait to start in right time
while True:
    response = pick_up_and_send_inverter_data(client)
    time.sleep(5)
    # time.sleep(300) # 5min
# client.loop_forever()
