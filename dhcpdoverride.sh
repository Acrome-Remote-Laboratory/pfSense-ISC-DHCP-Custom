#!/bin/bash
killall -3 dhcpd
cat /var/dhcpd/etc/dhcpd.opt82 >> /var/dhcpd/etc/dhcpd.conf
/usr/local/sbin/dhcpd -user dhcpd -group _dhcp -chroot /var/dhcpd -cf /etc/dhcpd.conf -pf /var/run/dhcpd.pid em1 em2
