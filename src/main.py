'''
Info
'''
import time
import json
from libraries.docker_log import log_info
from libraries.wait_to_certain_time import wait_minutes_after_round_minute
from connection.mqtt import connect
from data.inverter_data import IMMEDIATE_VARS, CALCULATED_VARS, get_data

DATA_MODE = 'INVERTER' #Possibilites: 'OFFLINE' and 'INVERTER'
TOPIC = 'raspberryTopic'

def send_data(client, storable_data):
    try:
        client.publish(TOPIC, payload=storable_data, qos=0, retain=False)
    except:
        log_info('ERROR PUBLISHING DATA TO MQTT BROKER')

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
        log_info('To develop offiline data')
        return {'value': 0, 'unit': 'none'}

def pick_up_and_send_inverter_data(client):
    log_info("--> Started transmission")
    log_info("Getting Immediate variables")
    for imm_var in IMMEDIATE_VARS:
        try:
            imm_response = get_solar_data(imm_var)
            log_info(imm_var + ' | ' + str(imm_response))
            json = format_data_to_serialized_json({'variable': imm_var,
                                                   'value': imm_response.value, 
                                                   'unit': imm_response.unit})
            send_data(client, json)
        except:
            pass
    log_info("Getting calculated variables")
    for cal_var in CALCULATED_VARS:
        try:
            cal_response = get_solar_data(cal_var)
            log_info(cal_var + ' | ' + str(cal_response))
            json = format_data_to_serialized_json({'variable': cal_var,
                                                   'value': cal_response.value,
                                                   'unit': cal_response.unit})
            send_data(client, json)
        except:
            pass
    log_info("--> Ended transmission")

log_info("| === START === |") 
client = connect()
wait_minutes_after_round_minute(2)
while True:
    response = pick_up_and_send_inverter_data(client)
    time.sleep(300) # 5min
# client.loop_forever()
