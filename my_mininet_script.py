import sys
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink

def create_network_topology(topology, n):
    if topology == "linear":
        create_linear_topology(n)
    elif topology == "tree":
        create_tree_topology(n)
    elif topology == "mesh":
        create_mesh_topology(n)
    else:
        print("Invalid topology. Available options are: linear, tree, mesh")

def create_linear_topology(n):
    net = Mininet(host=CPULimitedHost, link=TCLink)
    hosts = [net.addHost('h%s' % i, cpu=.5/n) for i in range(1, n+1)]
    switches = [net.addSwitch('s%s' % i) for i in range(1, n)]
    for i in range(n-1):
        net.addLink(switches[i], switches[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(n):
        net.addLink(hosts[i], switches[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.start()
    net.pingAll()
    net.stop()

def create_tree_topology(n):
    net = Mininet(host=CPULimitedHost, link=TCLink)
    hosts = [net.addHost('h%s' % i, cpu=.5/n) for i in range(1, n+1)]
    switches = [net.addSwitch('s%s' % i) for i in range(1, n)]
    for i in range(n-1):
        net.addLink(switches[i], switches[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(1, n):
        net.addLink(switches[i], switches[i//2], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(n):
        net.addLink(hosts[i], switches[i], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.start()
    net.pingAll()
    net.stop()

def create_mesh_topology(n):
    net = Mininet(host=CPULimitedHost, link=TCLink)
    hosts = [net.addHost('h%s' % i, cpu=.5/n) for i in range(1, n+1)]
    switches = [net.addSwitch('s%s' % i) for i in range(1, n+1)]
    for i in range(n):
        for j in range(n):
            if i != j:
                net.addLink(switches[i], switches[j], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    for i in range(n):
        net.addLink(hosts[i], switches[i+1], bw=10, delay='5ms', loss=10, max_queue_size=1000)
    net.start()
    net.pingAll()
    net.stop()

if name == 'main':
    if len(sys.argv) != 3:
        print("Usage: runmininet.py [linear|tree|mesh] [n]")
    else:
        topology = sys.argv[1]
        n = int(sys.argv[2])
        create_network_topology(topology, n)
