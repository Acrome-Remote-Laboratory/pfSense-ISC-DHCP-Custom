#!/bin/bash
cp ./dhcpd.opt82 /var/dhcpd/etc/dhcpd.opt82
cp ./dhcpdoverride.sh /usr/local/etc/rc.d/dhcpdoverride.sh
chmod +x /usr/local/etc/rc.d/dhcpdoverride.sh
