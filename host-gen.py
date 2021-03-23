import os
import pathlib
from swconfig import Switch

SW1 = Switch(0, '172.16', 28, ip_offset=20)
SW1.disable_ports([1,2,23,24,25,26,27,28])

SW2 = Switch(1, '172.16', 18)
SW2.disable_ports([1,17,18])

DHCP = Switch(0, '172.17', 256)

Statics = Switch(0, '172.18', 2)
Statics.disable_ports([1])

host_definitions = SW1.dump_host_definitions() + SW2.dump_host_definitions()

os.chdir(pathlib.Path(__file__).parent.absolute())
with open('./dhcpd.opt82', 'w+') as file:
	for host in host_definitions:
		file.write(host)

with open('./hosts', 'w+') as file:
	for host in SW1.ip_list() + SW2.ip_list() + Statics.ip_list():
		file.write(host + '\n')

with open('./hosts-dhcp', 'w+') as file:
	for host in SW1.ip_list() + SW2.ip_list() + DHCP.ip_list() + Statics.ip_list():
		file.write(host + '\n')