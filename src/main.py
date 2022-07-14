'''
Info from the project
'''

code_mode = 'PC' #Possibilities: 'PC', 'RASP' and 'TEST'
data_mode = 'TEST_FILE' #Possibilites: 'TEST_FILE' and 'INVERTER'

from development import pc, rasp, test_rasp

if code_mode == "RASP":
    rasp.main()
elif code_mode == "PC":
    pc.main()
elif code_mode == "TEST":
    test_rasp.main()
else:
    print("No valid mode") 


