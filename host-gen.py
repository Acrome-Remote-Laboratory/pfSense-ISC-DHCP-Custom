from pprint import pprint as print

import os
import pathlib

os.chdir(pathlib.Path(__file__).parent.absolute())

def create_host_definition(switch_id, port_name, ip):
	host_def = """
	host port%d  {
		host-identifier option agent.circuit-id "%d.%d";
		fixed-address %s;
	}""" % (port_name, switch_id, port_name, ip)
	return host_def

device_port_range = (3,22)
total_port_count = 28
ip_offset = 20
ip_subnet = '172.0.0.'

ip_addresses = [ip_subnet+"%d" % (i+1) for i in range(ip_offset, ip_offset + total_port_count)]
port_ip_map = ["Port %2d -- IP: %s" % (i+1, ip_addresses[i]) for i in range(total_port_count)]
host_definitions = [create_host_definition(0, i+1, ip_addresses[i]) for i in range(total_port_count)]


with open('./dhcpd.opt82', 'w') as file:
	file.write('')

with open('./dhcpd.opt82', 'a') as file:
	for host in host_definitions[device_port_range[0]-1:device_port_range[1]]:
		file.write(host)
