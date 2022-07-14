'''
Info
'''

code_mode = 'PC' #Possibilities: 'PC' and 'RASP'
data_mode = 'OFFLINE' #Possibilites: 'OFFLINE' and 'INVERTER'

from development import pc, rasp

if code_mode == "RASP":
    rasp.main(data_mode)
elif code_mode == "PC":
    pc.main(data_mode)
else:
    print("No valid mode") 


