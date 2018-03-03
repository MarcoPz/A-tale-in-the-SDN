#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h1)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    
    print ('SETTING THE VERSION OF OPENFLOW TO BE USED IN EACH ROUTER:\n')
    s1.cmdPrint('ovs-vsctl set Bridge s1 protocols=OpenFlow13')
    
    print('FOR SAFETY I KILLALL CONTROLLER PREVIOUS:\n')
    c0.cmdPrint('killall controller')
    
    print('START REST_FIREWALL ON XTERM OF C0 CONTROLLER:\n')
    c0.cmdPrint('ryu-manager ryu.app.rest_firewall &')
    
    print('FIREWALL STARTED SET TO CUT OFF ALL COMMUNICATION:\n') #when it start, block all connections
    net.pingAll() #test it
    
    print('ENABLE FIREWALL:\n')
    c0.cmdPrint('curl -X PUT http://localhost:8080/firewall/module/enable/0000000000000001 &')
    c0.cmdPrint('curl http://localhost:8080/firewall/module/status  &')
    
    #print('ADD RULES FOR PINGING BETWEEN H1 AND H2:\n')
    #Open an xterm of c0 in the mininet dialog (mininet> xterm c0)
    #c0.cmdPrint(curl -X POST -d '{"nw_src": "10.0.0.1/8", "nw_dst": "10.0.0.2/8", "nw_proto": "ICMP"}' http://localhost:8080/firewall/rules/0000000000000001) add this rule in c0
    #c0.cmdPrint(curl -X POST -d '{"nw_src": "10.0.0.2/8", "nw_dst": "10.0.0.1/8", "nw_proto": "ICMP"}' http://localhost:8080/firewall/rules/0000000000000001) add this rule in c0
    
    print('PING h1->h2\n')
    #net.pingAll() in mininet CLI (mininet> pingAll and you will notice that now h1 ping with success h2, while h3 still not reachable.
   
    #You have added some rules just for the ICMP protocol, but you can add others related to all protcols.
   
    CLI(net)
    net.stop()
    
if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
