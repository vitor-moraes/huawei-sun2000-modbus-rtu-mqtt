from libraries.base_solar import HuaweiSolar
import os

IMMEDIATE_VARS = [
'pv_01_voltage',
'pv_01_current',
'pv_02_voltage',
'pv_02_current',
'input_power',
'grid_voltage',
'grid_current',
'active_power', 
'grid_A_voltage',
'active_grid_A_current',
'power_meter_active_power',

'reactive_power',
'grid_frequency',
'startup_time',
'shutdown_time', 
"rated_power",
"P_max",
"S_max",
"Q_max_out",
"Q_max_in",
"grid_voltage",
"line_voltage_A_B",
"line_voltage_B_C",
"line_voltage_C_A",
"phase_A_voltage",
"phase_B_voltage",
"phase_C_voltage",
"grid_current",
"phase_A_current",
"phase_B_current",
"phase_C_current",
"grid_A_voltage",
"grid_B_voltage",
"grid_C_voltage",
"active_grid_A_current",
"active_grid_B_current",
"active_grid_C_current",
"power_meter_active_power",
"active_grid_power_factor",
"active_grid_frequency",
"grid_exported_energy",
"grid_accumulated_energy",
"active_grid_A_B_voltage",
"active_grid_B_C_voltage",
"active_grid_C_A_voltage",
"active_grid_A_power",
"active_grid_B_power",
"active_grid_C_power",
]

CALCULATED_VARS = ['day_active_power_peak',
'efficiency', 
'internal_temperature',
'insulation_resistance',
'device_status', 
'fault_code',
'accumulated_yield_energy',
'daily_yield_energy',
'grid_exported_energy', 
'grid_accumulated_energy'
]

def get_data(var_name):
    return inverter.get(var_name)
    
inverter_port = os.getenv('INVERTER_PORT', '/dev/ttyUSB0')
inverter = HuaweiSolar(inverter_port, slave=1)
inverter._slave = 1
inverter.wait = 1