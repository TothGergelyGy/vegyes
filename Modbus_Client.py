import sys,json,time
from pyModbusTCP.client import ModbusClient
import random
def const_func(func_code,sleeping,address,val,Mclient):
    while True:
        if func_code==2:
            x=Mclient.read_discrete_inputs(address,val)
            print(x)
        elif func_code==1:
            x=Mclient.read_coils(address,val)
            print(x)
        elif func_code==5:
            Mclient.write_single_coil(address,val)
        elif func_code==4:
            x=Mclient.read_input_registers(address,val)
            print(x)
        elif func_code==3: 
            x=Mclient.read_holding_registers(address,val)
            print(x)
        elif func_code==6: 
            Mclient.write_single_register(address,val)
        time.sleep(int(timing))
            
def rand_func(func_code,sleeping,address,Mclient):
    while True:
        if func_code==5: 
            n = random.randint(0,1)
            Mclient.write_single_coil(address,n)
        elif func_code==6:
            n = random.randint(0,2**16)
            Mclient.write_single_register(address,n)
        time.sleep(int(timing))
        
def count_func(func_code,sleeping,address,val,Mclient):
    x=0
    while x<val:
        if func_code==5: 
            Mclient.write_single_coil(address,x)
        elif func_code==6:
            Mclient.write_single_register(address,x)
        time.sleep(int(timing))
        x=x+1
    
print("Lefutott")
    
Json_Input=False
if sys.argv[1]=="config.json":
    Json_Input=True
    
else:
    Json_Input=False
    
if Json_Input:
    print("JSON beolvasas")
    #ide json filebol beolvasni, a beolvasott ertekek alapjan fv-t hivni, majd kiirni
else:
    print("Sys.argv[] beolvasas")
    Server_ip=sys.argv[1]       #ip
    function_code=int(sys.argv[2])   #a function code a weboldalrol, onnan nezd ki
    timing=int(sys.argv[3])        #keres gyakorisaga 0.1 az 0.1 masodperc
    function_type=sys.argv[4]   #const rand count
    start=int(sys.argv[5])           #register/coil kezdo addresse
    value=int(sys.argv[6])           #const ertek irasra / hany db-ot olvassin ki olvasasnal
    c = ModbusClient(Server_ip,502)
    c.open()
    if function_type=="const":
        const_func(function_code,timing,start,value,c)
    elif function_type=="rand":
        rand_func(function_code,timing,start,c)
    elif function_type=="count":
        count_func(function_code,timing,start,value,c)
    c.close()        
            
    


