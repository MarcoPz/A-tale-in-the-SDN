from mininet.cli import CLI
from mininet.log import lg, info
from mininet.topolib import TreeNet


def createmynet():
    lg.setLogLevel( 'info')
    mynet = TreeNet( depth=3, fanout=4 )
    mynet.addNAT().configDefault()
    mynet.start()
    info( "Running network..\n" )
    info( "'exit' or control-D to shut down network\n" )
    CLI( mynet )
    mynet.stop()	

if __name__ == '__main__':
    createmynet()
