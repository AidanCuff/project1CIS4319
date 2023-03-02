from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost
from mininet.link import TCLink
import sys


class SingleSwitchTopo(Topo):
    def __init__(self,n=2,**opts):
        Topo.__init__(self,**opts)
        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('h%s'%(h+1,cpu=.5/n))
            self.addLink(host, switch,bw=10, delay='5ms', loss=10, max_queue_size=1000)
            
class LinearTopo(Topo):
    def __init__(self,n=2,**opts):
        Topo.__init__(self,**opts)
        
        # Add switches to the topology
        switches = [self.addSwitch(f's{i+1}') for i in range(n)]
        
        # Add hosts to the topology
        hosts = [self.addHost(f'h{j+1}', cpu=.5/n) for j in range(n)]
        
        # Add links between the switches and hosts
        for i in range(n):
            self.addLink(hosts[i], switches[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
            if i < n-1:
                self.addLink(switches[i], switches[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)


def simpleTest():
    topo = SingleSwitchTopo(n=3)
    net = Mininet(topo)
    net.start()
    print("dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll();
    net.stop()

    topo = LinearTopo(n=3)
    net = Mininet(topo)
    net.start()
    print("dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll();
    net.stop()

if __name__=='__main__':
    setLogLevel('info')
    simpleTest()
