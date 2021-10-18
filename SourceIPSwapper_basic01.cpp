//Ez a program a szakdogahoz keszult
//RPI ket interfacen csatlakozik az Exatahoz, a ket cime mappelve van emulalt node-hoz
//Ez a program az
//
// ->eth0->eth1 
//
//iranyt hajtja vegre a tovabbitasban.
#include <tins/tins.h>
#include <iostream>
#include <functional>
using std::bind;
using namespace Tins;


    /*
    RPI eth0    192.168.222.80              ->  Server eth2     192.168.222.2
                B8:27:EB:46:87:2A                               00:1F:29:60:0D:15

    RPI eth1    192.168.222.81              ->  Server eth3     192.168.222.3
                00:24:32:17:5F:55                               00:1F:29:60:0D:14


    192.0.0.1 -> 192.0.0.2 -> 192.0.1.1 -> 192.0.1.2
    (192.0.0.1->192.0.1.2)

    */
    
    

class arp_monitor {
public:
    
    NetworkInterface iface_eth0 = NetworkInterface("eth0"); //"eth0" rpi interface
    NetworkInterface iface_eth1 = NetworkInterface("eth1"); //"eth1" rpi interface
    NetworkInterface::Info info_eth0 = info_eth0.addresses(); //rpi interface cimeit kiolvassa
    NetworkInterface::Info info_eth1 = info_eth1.addresses(); //rpi interface cimeit kiolvassa
    PacketSender sender;
    //info_eth0.hw_addr
    //EthernetII eth2drive = 
    void run(Sniffer& sniffer){                                                                               //libtins ilyen formaban koveteli meg a callbackfv meghivasat, folyamatos packet sniffing
        sniffer.sniff_loop(bind(&arp_monitor::callback,this,std::placeholders::_1)
            );
    }
private:
    bool callback(PDU& pdu) { 
        
        EthernetII& eth=pdu.rfind_pdu<EthernetII>();     //Ethernet szintu protokollt keresunk a packetban
        EthernetII *eth2=eth.clone();                    //lemasoljuk az Ethernet szinttol felfele a packetet, igy szabadon modosithatjuk
        
        //ha tartalmaz IP-t,  irjuk at es kuldjuk ki a masik oldalon
        if ( (eth2->find_pdu<IP>())!=0 && 
             (eth2->find_pdu<IP>().dst_addr() == "192.0.1.2" || (eth2->find_pdu<IP>().dst_addr() == "192.168.222.80" && eth2->find_pdu<IP>().src_addr() == "192.0.0.1"))
            ) 
        {  
            eth2->src_addr("00:24:32:17:5F:55"); 
            eth2->dst_addr("00:1F:29:60:0D:14"); 
            eth2->find_pdu<IP>().src_addr("192.168.222.81"); 
            eth2->find_pdu<IP>().dst_addr("192.0.1.2");
            sender.send(*eth2, iface_eth1);                     //az eth1 interfacere kuldjuk
            delete eth2;
            return true;
        }   


        delete eth2;    //eth2-t sajat felelossegunk felszabaditani
        return true;    //a callback addig folytatodik amig true a visszateresi ertek
    }
};


int main() {
    arp_monitor monitor;
    SnifferConfiguration config;
    config.set_promisc_mode(true);
    config.set_immediate_mode(true); // minden forgalmat, folyamatosan sniffeljen   
    
    
    try {
        Sniffer sniffer("eth0", config);  //az eth0 interfacen bejovo forgalmat figyeljuk
        monitor.run(sniffer);       //loop sniffing, a callback fv intezi a mukodesi logikat
    }
    catch (std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
    }
}

