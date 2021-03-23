import os
import pathlib

class Switch:
	def __init__(self, cid, subnet, port_count, ip_offset=0):
		self.cid = cid
		self.subnet = subnet
		self._ip_prefix = '%d.0.%d.' % (self.subnet, self.cid)
		self.port_count = port_count
		self.forbidden_ports = []
		self.ports = [port for port in range(1, port_count+1) if port not in self.forbidden_ports]
		self.ip_offset = ip_offset

	def disable_ports(self, ports):
		self.forbidden_ports = ports
		self.ports = [port for port in range(1, self.port_count+1) if port not in self.forbidden_ports]

	def dump_host_definitions(self):
		host_def = []
		for port in self.ports:
			ip = port + self.ip_offset
			hostname = 'SW%dPORT%d' % (self.cid, port)
			if ip < 255:
				ip = self._ip_prefix + str(ip)
				host_def.append("""
				host %s  {
					host-identifier option agent.circuit-id "%d.%d";
					fixed-address %s;
				}""" % (hostname, self.cid, port, ip))
		return host_def

SW1 = Switch(0, 172, 28, ip_offset=20)
SW1.disable_ports([1,2,23,24,25,26,27,28])

SW2 = Switch(1, 172, 18)
SW2.disable_ports([15,17,18])

host_definitions = SW1.dump_host_definitions() + SW2.dump_host_definitions()

os.chdir(pathlib.Path(__file__).parent.absolute())
with open('./dhcpd.opt82', 'w+') as file:
	for host in host_definitions:
		file.write(host)

with open('./dhcpd.opt82', 'a') as file:
	pass
