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
print(data)
print(data['clients'])
print(type(data['clients']))

for i in data['clients']:
    print(i)
    data['clients'][i]['modbusclient']=ModbusClient(data['clients'][i]['ip'],data['clients'][i]['port'])
    data['clients'][i]['modbusclient'].open()

    
while True:
    for i in data['commands']:
        if i['type']=="coil" :
            if i['action']=="read_and_write":
                x=data['clients'][i['from']]['modbusclient'].read_coils(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+str(i['readaddress'])+" value: "+str(x))
                if x is not None:
                    data['clients'][i['to']]['modbusclient'].write_multiple_coils(i['writeaddress'],x) #itt (x,1) helyett (writeaddrees,x) kell
                else:
                    print("x none volt")
            elif i['action']=="read":
                x=data['clients'][i['from']]['modbusclient'].read_coils(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+str(i['readaddress'])+" value: "+str(x))
        elif i['type']=="reg":
            if i['action']=="read_and_write":
                x=data['clients'][i['from']]['modbusclient'].read_holding_registers(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+str(i['readaddress'])+" value: "+str(x))
                if x is not None:
                    data['clients'][i['to']]['modbusclient'].write_multiple_registers(i['writeaddress'],x)
                else:
                    print("x none volt")
               
            elif i['action']=="read":
                x=data['clients'][i['from']]['modbusclient'].read_holding_registers(i['readaddress'],1)
                print("read: "+i['type']+" from: "+i['from']+" address: "+str(i['readaddress'])+" value: "+str(x))
f.close()
