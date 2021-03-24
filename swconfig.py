_format_string = """ host %s  {
	host-identifier option agent.circuit-id "%d.%d";
	fixed-address %s;
}"""

class Switch:
	def __init__(self, cid, subnet, port_count, ip_offset=0):
		self.cid = cid
		self.subnet = subnet
		self._ip_prefix = '%s.%d.' % (self.subnet, self.cid)
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
			hostname = 'SW%dPORT%d' % (self.cid, port)
			if ip <= 255:
				ip = self._ip_prefix + str(ip)
				host_def.append( _format_string % (hostname, self.cid, port, ip))
		return host_def

	def ip_list(self):
		return [self._ip_prefix + str(port + self.ip_offset) for port in self.ports if (port + self.ip_offset) <= 255]