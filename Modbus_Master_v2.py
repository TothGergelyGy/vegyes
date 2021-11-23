import sys,json,time
from pyModbusTCP.client import ModbusClient
import random
#sys.argv bemenet: commands.json
print("Modbus Master_v2 elindult")
timing=0.1
#Input register 	Read-only   16 bits
#Holding register 	Read-write  16 bits


commandfile=open(sys.argv[1])
data=json.load(commandfile)


for i in data['clients']:
    i['modbusclient']=ModbusClient(i['ip'],i['port'])
    i['modbusclient'].open()

    
while True
    for i in data['commands']:
        if i['type']=="coil" 
            if i['action']="read_and_write"
                x=data['clients'][i['from']]['modbusclient'].read_coils(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+i['readaddress']+" value: "+str(x))
                data['clients'][i['to']]['modbusclient'].write_multiple_coils(x,1)
            elif i['action']="read"
                x=data['clients'][i['from']]['modbusclient'].read_coils(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+i['readaddress']+" value: "+str(x))
        elif i['type']=="reg"
            if i['action']="read_and_write"
                x=data['clients'][i['from']]['modbusclient'].read_holding_register(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+i['readaddress']+" value: "+str(x))
                data['clients'][i['to']]['modbusclient'].write_multiple_registers(x,1)
               
            elif i['action']="read"
                x=data['clients'][i['from']]['modbusclient'].read_holding_register(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+i['readaddress']+" value: "+str(x))
f.close()