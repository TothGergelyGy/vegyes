//Ez a program a szakdogahoz keszult
//RPI ket interfacen csatlakozik az Exatahoz, a ket cime mappelve van emulalt node-hoz
//Ez a program az
//
// ->eth1->eth0 
//
//iranyt hajtja vegre a tovabbitasban.
#include <tins/tins.h>
#include <iostream>
#include <functional>
#include <string>
using std::bind;
using namespace Tins;
using std::string;

/*
RPI eth0    192.168.222.80              ->  Server eth2     192.168.222.2
            B8:27:EB:46:87:2A                               00:1F:29:60:0D:15

RPI eth1    192.168.221.81              ->  Server eth3     192.168.221.3
            00:24:32:17:5F:55                               00:1F:29:60:0D:14


192.0.1.2 -> 192.0.1.1 -> 192.0.0.2 -> 192.0.0.1
(192.0.1.2->192.0.0.1)

*/



class arp_monitor {
public:

    NetworkInterface iface_eth0 = NetworkInterface("eth0"); //"eth0" rpi interface
    NetworkInterface iface_eth1 = NetworkInterface("eth1"); //"eth1" rpi interface
    NetworkInterface::Info info_eth0 = info_eth0.addresses(); //rpi interface cimeit kiolvassa
    NetworkInterface::Info info_eth1 = info_eth1.addresses(); //rpi interface cimeit kiolvassa
    PacketSender sender;

    void run(Sniffer& sniffer) {                                                                               //libtins ilyen formaban koveteli meg a callbackfv meghivasat, folyamatos packet sniffing
        sniffer.sniff_loop(bind(&arp_monitor::callback, this, std::placeholders::_1)
        );
    }
private:
    void BasicPacket(string source) 
    {
        EthernetII eth2("00:1F:29:60:0D:14", "00:24:32:17:5F:55");
        eth2 /= IP("192.0.1.2", source);
        eth2 /= UDP(13, 15);
        eth2 /= RawPDU("Im a payload");
        sender.send(eth2, iface_eth1);
    }
    bool callback(PDU& pdu) {


        //eth /=IP("dest","source")
        //RPI eth1 192.168.221.81
        //random 192.0.3.4
        //random 179.243.24.17
        //exata eth3 192.168.221.3
        //exata eth2 192.168.222.2
        //szimulacioban levo 192.0.2.2
        //szimulacioban levo 192.0.1.3
        std::cout << "RPI 192.168.221.81 forrás küldése";
        for (int i = 0; i < 15; i++) 
        {
            BasicPacket("192.168.221.81");
        }
        std::cin.get();
        std::cout << "random 192.0.3.4 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("192.0.3.4");
        }
        std::cin.get();
        std::cout << "random 179.243.24.17 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("179.243.24.17");
        }
        std::cin.get();
        std::cout << "exata eth3 192.168.221.3 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("192.168.221.3");
        }
        std::cin.get();
        std::cout << "exata eth2 192.168.222.2 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("192.168.222.2");
        }
        std::cin.get();
        std::cout << "szimulacioban levo 192.0.2.2 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("192.0.2.2");
        }
        std::cin.get();
        std::cout << "szimulacioban levo 192.0.1.3 forrás küldése";
        for (int i = 0; i < 15; i++)
        {
            BasicPacket("192.0.1.3");
        }



        return true;    //a callback addig folytatodik amig true a visszateresi ertek
    }
};


int main() {
    arp_monitor monitor;
    SnifferConfiguration config;
    config.set_promisc_mode(true);
    config.set_immediate_mode(true); // minden forgalmat, folyamatosan sniffeljen   


    try {
        Sniffer sniffer("eth1", config);  //az eth1 interfacen bejovo forgalmat figyeljuk
        monitor.run(sniffer);       //loop sniffing, a callback fv intezi a mukodesi logikat
    }
    catch (std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
    }
}

