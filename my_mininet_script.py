#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, CPULimitedHost
from mininet.link import TCLink
from mininet.topo import SingleSwitchTopo, LinearTopo, TreeTopo, MeshTopo
import sys

if len(sys.argv) != 3:
    print("Usage: python runmininet.py <topology> <n>")
    print("  topology: single, linear, tree, mesh")
    print("  n: number of nodes")
    sys.exit(1)

topology = sys.argv[1]
n = int(sys.argv[2])

if topology == "single":
    topo = SingleSwitchTopo(n)
elif topology == "linear":
    topo = LinearTopo(n)
elif topology == "tree":
    topo = TreeTopo(n)
elif topology == "mesh":
    topo = MeshTopo(n)
else:
    print("Invalid topology. Please choose from single, linear, tree, or mesh.")
    sys.exit(1)

net = Mininet(topo=topo, controller=Controller, switch=OVSKernelSwitch, link=TCLink)

for host in net.hosts:
    host.setCPUFraction(0.5 / n)

for link in net.links:
    link.intf1.config(bw=10, delay='5ms', loss=10, max_queue_size=1000)
    link.intf2.config(bw=10, delay='5ms', loss=10, max_queue_size=1000)

net.start()
net.pingAll()
net.stop()
