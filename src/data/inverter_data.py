from libraries.base_solar import HuaweiSolar
import os

IMMEDIATE_VARS = ['pv_01_voltage', 'pv_01_current', 'pv_02_voltage',
                'pv_02_current', 'input_power', 'grid_voltage', 
                'grid_current', 'active_power', 
                'grid_A_voltage', 'active_grid_A_current',
                'power_meter_active_power']

CALCULATED_VARS = ['day_active_power_peak', 'efficiency', 
                'internal_temperature', 'insulation_resistance', 'device_status', 
                'fault_code', 'accumulated_yield_energy',
                'daily_yield_energy', 'grid_exported_energy', 
                'grid_accumulated_energy']

def get_data(var_name):
    return inverter.get(var_name)
    
inverter_port = os.getenv('INVERTER_PORT', '/dev/ttyUSB0')
inverter = HuaweiSolar(inverter_port, slave=1)
inverter._slave = 1
inverter.wait = 1