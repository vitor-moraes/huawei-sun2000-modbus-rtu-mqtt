import os
import time
import json
from libraries.docker_log import log_info
from libraries.wait_to_certain_time import wait_minutes_after_round_to_10_minute
from connection.mqtt import connect
from data.inverter_data import IMMEDIATE_VARS, CALCULATED_VARS, get_data
from data.offline import get_example_data

INTERVAL_BETWEEN_GROUP_OF_REQUESTS = 300 # Standard = 300
INTERVAL_BETWEEN_REQUESTS = 0 # Standard = 0
MINUTE_TO_START_GETTING_DATA_AFTER_ROUND_TO_10 = 2 # Standard = 2

DATA_MODE = os.getenv('DATA_MODE', 'INVERTER')
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'raspberryTopic')

def send_data(client, storable_data):
    try:
        client.publish(MQTT_TOPIC, payload=storable_data, qos=0, retain=False)
    except:
        log_info('ERROR PUBLISHING DATA TO MQTT BROKER')

def format_data_to_serialized_json(info):
    data = {
                'ID': 'SUN2000_1',
                'Valor': info['value'],
                'Aplicacao': 'Geração Solar',
                'Local': 'BLOCO D',
                'Tipo': 'Inversor',
                'Variavel': info['variable'],
                'Unidade': info['unit'],
                'Rede': 'MQTT',
                'Professor': 'Paciencia'
            }
    serialized_data = json.dumps(data)
    return serialized_data

def get_solar_data(variable):
    if DATA_MODE == 'INVERTER':
        return get_data(variable)
    else:
        return get_example_data(variable)

def pick_up_and_send_inverter_data(client):
    log_info("--> Started transmission")
    log_info("Getting Immediate variables")
    for imm_var in IMMEDIATE_VARS:
        try:
            imm_response = get_solar_data(imm_var)
            log_info(imm_var + ' = ' + str(imm_response.value) + " " + str(imm_response.unit))
            json = format_data_to_serialized_json({'variable': imm_var,
                                                   'value': imm_response.value, 
                                                   'unit': imm_response.unit})
            send_data(client, json)
        except:
            pass
        time.sleep(INTERVAL_BETWEEN_REQUESTS)
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
        time.sleep(INTERVAL_BETWEEN_REQUESTS)
    log_info("--> Ended transmission")

log_info("| === START === |") 
client = connect()
wait_minutes_after_round_to_10_minute(MINUTE_TO_START_GETTING_DATA_AFTER_ROUND_TO_10)
while True:
    response = pick_up_and_send_inverter_data(client)
    time.sleep(INTERVAL_BETWEEN_GROUP_OF_REQUESTS)
# client.loop_forever()
