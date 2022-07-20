import random
from libraries.docker_log  import log_info

POSSIBLE_SAMPLE_UNITS = [
    "EXEMPLE_UNIT_A","EXEMPLE_UNIT_B","EXEMPLE_UNIT_C",
    "EXEMPLE_UNIT_D","EXEMPLE_UNIT_E","EXEMPLE_UNIT_F"
]

class DataExample:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

def get_example_data(var_name):
    log_info("Getting a NON-REAL value to " + var_name)
    sample_value = random.randint(0, 100)
    sample_unit = random.choice(POSSIBLE_SAMPLE_UNITS)
    sample = DataExample(sample_value, sample_unit)
    return sample
