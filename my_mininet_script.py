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

        hosts = [self.addHost(f'h{i+1}',cpu=.5/n) for i in range(n)]
        for j in range(n):
            self.addLink(hosts[i], switch,bw=10, delay='5ms', loss=10, max_queue_size=1000)
            
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

class TreeTopo(Topo):
    def __init__(self,n=2,**opts):
        Topo.__init__(self,**opts)
        
        # Add switches to the topology
        switches = [self.addSwitch(f's{i+1}') for i in range(n)]
        
        # Add hosts to the topology
        hosts = [self.addHost(f'h{j+1}', cpu=.5/n) for j in range(n)]
        
        # Add links between the root switch and hosts
        for h in hosts:
            self.addLink(h, switches[0], bw=10, delay='5ms', loss=10, max_queue_size=1000)
        
        # Add links between switches
        for i in range(n//2):
            self.addLink(switches[i], switches[2*i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)
            self.addLink(switches[i], switches[2*i+2], bw=10, delay='5ms', loss=10, max_queue_size=1000)

class MeshTopo(Topo):
    def __init__(self,n=2,**opts):
        Topo.__init__(self,**opts)
        
        # Add switches to the topology
        switches = [self.addSwitch(f's{i+1}') for i in range(n)]
        
        # Add hosts to the topology
        hosts = [self.addHost(f'h{j+1}', cpu=.5/n) for j in range(n)]
        
        # Add links between hosts and switches
        for i in range(n):
            for j in range(n):
                self.addLink(hosts[i], switches[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)
        
        # Add links between switches
        for i in range(n):
            for j in range(i+1, n):
                self.addLink(switches[i], switches[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)


def simpleTest():
    if sys.argv[1] == "single":
        topo = SingleSwitchTopo(int(sys.argv[2]))
    if sys.argv[1] =="linear":
            topo = LinearTopo(int(sys.argv[2]))
    if sys.argv[1] =="tree":
            topo = TreeTopo(int(sys.argv[2]))
    if sys.argv[1] =="mesh":
            topo = MeshTopo(int(sys.argv[2]))
    else:
            print("unknown topology")
        
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
