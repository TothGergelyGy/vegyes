import sys,json,time
from pyModbusTCP.client import ModbusClient
import random
#sys.argv bemenet: slave1.ip slave1.port slave2.ip slave2.port
print("Modbus Master elindult")
    
Slave1_IP=sys.argv[1]
Slave1_Port=int(sys.argv[2])
Slave2_IP=sys.argv[3]
Slave2_Port=sys.argv[4]
Slave1=ModbusClient(Slave1_IP,Slave1_Port)
Slave2=ModbusClient(Slave2_IP,Slave2_Port)
timing=0.5


#Input register 	Read-only   16 bits
#Holding register 	Read-write  16 bits
print("coil:coilt olvas es ir")
print("h_register:holding registert olvas es ir")
print("i_register:input registert olvas es holding registerbe ir")
print("all:coilt olvas es ir, majd holding registert olvas es ir")
mode=input() 



if mode=="coil":
    print("Olvasas kezdo bit cime:")
    read_from=int(input())
    print("Olvasas utolso bit cime(amit mar nem olvas):")
    read_until=int(input())
    print("Iras kezdo bitje:")
    write_from=int(input())
    write_until=write_from+(read_until-read_from)
    while True:
        for x in range(read_from, read_until):
            Slave1.open()
            y=Slave1.read_coils(x,1) #az y egy bool lista
            Slave1.close()
            print("coil ertek "+str(x)+": "+str(y))
            if y==None:
               print("Nem tudott olvasni")
            Slave2.open()
            Slave2.write_multiple_coils((write_from+x-read_from),y) #azert nem write_single_coil mert bool listat ad vissza a read
            Slave2.close()
            time.sleep(timing)  

          
          
elif mode=="h_register":
    print("Olvasas kezdo bit cime:")
    read_from=int(input())
    print("Olvasas utolso bit cime(amit mar nem olvas):")
    read_until=int(input())
    print("Iras kezdo bitje:")
    write_from=int(input())
    write_until=write_from+(read_until-read_from)
    while True:
        for x in range(read_from, read_until):
            Slave1.open()
            y=Slave1.read_holding_registers(x,1) #az y egy lista
            Slave1.close()
            print("holding register ertek "+str(x)+": "+str(y))
            if y==None:
               print("Nem tudott olvasni")
            Slave2.open()
            Slave2.write_multiple_registers((write_from+x-read_from),y)
            Slave2.close()
            time.sleep(timing)   
          
          
            
elif mode=="i_register":#read only, holdingba kell irni
    print("Olvasas kezdo bit cime:")
    read_from=int(input())
    print("Olvasas utolso bit cime(amit mar nem olvas):")
    read_until=int(input())
    print("Iras kezdo bitje:")
    write_from=int(input())
    write_until=write_from+(read_until-read_from)
    while True:
        for x in range(read_from, read_until):
            Slave1.open()
            y=Slave1.read_input_registers(x,1) #az y egy int lista
            Slave1.close()
            print("input register ertek "+str(x)+": "+str(y))
            if y==None:
               print("Nem tudott olvasni")
            Slave2.open()
            Slave2.write_multiple_registers((write_from+x-read_from),y)
            Slave2.close()
            time.sleep(timing) 
    
    
    
elif mode=="all":#coil es holding register is
    print("Coil olvasas kezdo bit cime:")
    coil_read_from=int(input())
    print("Coil olvasas utolso bit cime(amit mar nem olvas):")
    coil_read_until=int(input())
    print("Coil iras kezdo bitje:")
    coil_write_from=int(input())
    coil_write_until=coil_write_from+(coil_read_until-coil_read_from)
    
    print("Holding register olvasas kezdo bit cime:")
    reg_read_from=int(input())
    print("Holding register olvasas utolso bit cime(amit mar nem olvas):")
    reg_read_until=int(input())
    print("Holding register iras kezdo bitje:")
    reg_write_from=int(input())
    reg_write_until=reg_write_from+(reg_read_until-reg_read_from)
    
    while True:
        for x in range(coil_read_from, coil_read_until):
            Slave1.open()
            y=Slave1.read_coils(x,1) #az y egy bool lista
            Slave1.close()
            print("coil ertek "+str(x)+": "+str(y))
            if y==None:
               print("Nem tudott olvasni")
            Slave2.open()
            Slave2.write_multiple_coils((coil_write_from+x-coil_read_from),y)
            Slave2.close()
            time.sleep(timing)  
        
        for x in range(reg_read_from, reg_read_until):
            Slave1.open()
            y=Slave1.read_holding_registers(x,1) #az y egy int lista
            Slave1.close()
            print("holding register ertek "+str(x)+": "+str(y))
            if y==None:
               print("Nem tudott olvasni")
            Slave2.open()
            Slave2.write_multiple_registers((reg_write_from+x-reg_read_from),y)
            Slave2.close()
            time.sleep(timing)
