'''
Info
'''
import time
import json
from libraries.docker_log import log_for_me
from libraries.wait_to_certain_time import wait_minutes_after_round_minute
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
    data = {
                'ID': 'INV_1',
                'Valor': info['value'],
                'Aplicacao': 'PFC_Vitor_Moraes',
                'Local': 'Salas Ds',
                'Tipo': 'Inversor',
                'Variavel': info['variable'],
                'Unidade': info['unit'],
                'Rede': 'Wi-Fi',
                'Professor': 'Paciencia'
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
            json = format_data_to_serialized_json({'variable': imm_var,
                                                   'value': imm_response.value, 
                                                   'unit': imm_response.unit})
            send_data(client, json)
        except:
            pass
    log_for_me("Getting calculated variables")
    for cal_var in CALCULATED_VARS:
        try:
            cal_response = get_solar_data(cal_var)
            log_for_me(cal_var + ' | ' + str(cal_response))
            json = format_data_to_serialized_json({'variable': cal_var,
                                                   'value': cal_response.value,
                                                   'unit': cal_response.unit})
            send_data(client, json)
        except:
            pass
    log_for_me("--> Ended transmission")

log_for_me("Begin:") 
client = connect()
wait_minutes_after_round_minute(2)
while True:
    response = pick_up_and_send_inverter_data(client)
    time.sleep(600) # 10min
    # time.sleep(5) # 5seg
# client.loop_forever()
