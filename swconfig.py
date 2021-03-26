_format_string = """ host %s  {
	host-identifier option agent.circuit-id %s;
	fixed-address %s;
}"""

class Switch:
	def __init__(self, rid, subnet, port_count, ip_offset=0):
		self.rid = rid
		self.subnet = subnet
		self._ip_prefix = '%s.%d.' % (self.subnet, self.rid)
		self.port_count = port_count
		self.forbidden_ports = []
		self.ip_offset = ip_offset

		self.ports = [port for port in range(1, port_count+1) if port not in self.forbidden_ports]

	def disable_ports(self, ports):
		self.forbidden_ports = ports
		self.ports = [port for port in range(1, self.port_count+1) if port not in self.forbidden_ports]

	def dump_host_definitions(self):
		host_def = []
		for port in self.ports:
			ip = port + self.ip_offset
			hostname = 'SW%dPORT%d' % (self.rid, port)
			if ip <= 255:
				ip = self._ip_prefix + str(ip)
				t = 1 #Refer to TP-Link documentation about DHCP Option 82 TLV format
				v = ("%d.%d" % (self.rid, port))
				l = len(v)
				v_iter = iter(v.encode('utf-8').hex())
				#Inserts ':' after every 2nd character, works for hex representation
				#since custom circuit-id is a string and valid characters are bigger than 9 in hex
				cid = "%s:%s:%s" % (hex(t)[2:], hex(l)[2:], ':'.join(i+j for i,j in zip(v_iter, v_iter)))
				host_def.append( _format_string % (hostname, cid, ip))
		return host_def

	def ip_list(self):
		return [self._ip_prefix + str(port + self.ip_offset) for port in self.ports if (port + self.ip_offset) <= 255]