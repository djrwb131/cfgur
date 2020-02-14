# const_cmdmodes.py
#
# The command mode information is spread across the whole document.
# The table in chapter 1 was missing 6 of them.
# It's easier just to create these manually, rather than write a parser
# for it.
#

from command import CommandMode

user_desc           = \
"Contains a limited set of commands to view basic system information."
user_mode           = CommandMode("", "User EXEC", user_desc)

enable_desc         = \
"Allows you to issue any EXEC command, enter the VLAN mode, or enter the Global Configuration mode."        
enable_mode         = CommandMode("enable", "Privileged EXEC", enable_desc)

configure_desc      = \
"Groups general setup commands and permits you to make modifications to the running configuration."
configure_mode      = CommandMode("configure", "Global Config", configure_desc)

vlan_database_desc  = \
"Groups all the VLAN commands."
vlan_database_mode  = CommandMode("vlan database", "VLAN Config", vlan_database_desc)

interface_desc      = \
"Manages the operation of an interface and provides access to the router interface configuration \
commands. Use this mode to set up a physical port for a specific logical connection operation."
interface_mode      = CommandMode( ("interface","interface loopback","interface tunnel"),"Interface Config", interface_desc)

line_console_desc   = \
"Contains commands to configure USB and RS-232 console settings."
line_console_mode   = CommandMode( "line console", "Line Config (console)", line_console_desc)

line_ssh_desc       = \
"Contains commands to configure inbound SSH settings."
line_ssh_mode       = CommandMode( "line ssh", "Line Config (ssh)", line_ssh_desc)

line_telnet_desc       = \
"Contains commands to configure inbound telnet settings."
line_telnet_mode    = CommandMode( "line telnet", "Line Config (telnet)", line_telnet_desc)

policymap_desc      = \
"Contains the QoS Policy-Map configuration commands."                
policymap_mode      = CommandMode( "policy-map", "Policy-Map Config", policymap_desc)

policy_class_desc   = \
"Consists of class creation, deletion, and matching commands. The class match \
commands specify Layer 2, Layer 3, and general match criteria. "
policy_class_mode   = CommandMode( "class", "Policy-Class-Map Config", policy_class_desc)

classmap_desc       = \
"Contains the QoS class map configuration commands for IPv4."
classmap_mode       = CommandMode( "class-map", "Class-Map Config", classmap_desc)
ipv6_classmap_desc  = \
"Contains the QoS class map configuration commands for IPv6."
ipv6_classmap_mode  = CommandMode( "class-map ipv6", "IPv6-Class-Map Config", ipv6_classmap_desc)
mac_accesslist_desc = \
"Allows you to create a MAC Access-List and to enter the mode containing MAC \
Access-List configuration commands."
mac_accesslist_mode = CommandMode( "mac access-list extended", "Mac-Access-List Config", mac_accesslist_desc)

tacacs_server_desc  = \
"Contains commands to configure properties for the TACACS servers."
tacacs_server_mode  = CommandMode( "tacacs-server host", "TACACS Config", tacacs_server_desc)

dhcp_pool_desc      = \
"Contains the DHCP server IP address pool configuration commands."
dhcp_pool_mode      = CommandMode( "ip dhcp pool", "DHCP Pool Config", dhcp_pool_desc)

arp_accesslist_desc = \
"Contains commands to add ARP ACL rules in an ARP Access List."
arp_accesslist_mode = CommandMode( "arp access-list", "ARP Access-List Config", arp_accesslist_desc)

# These modes are not listed in chapter 1
vlan_desc           = \
"Contains commands to configure private and RSPAN VLANs."
vlan_mode           = CommandMode("vlan", "Private VLAN Config", vlan_desc)

time_range_desc     = \
"Contains commands for time-range based ACL rules."
time_range_mode     = CommandMode("time-range", "Time-Range Config", time_range_desc)

ipv4_acl_desc       = \
"Contains commands for configuring extended (named) IP ACLs."
ipv4_acl_mode       = CommandMode("ip access-list", "IPv4-Access-List Config", ipv4_acl_desc)

ipv6_acl_desc       = \
"Contains commands for configuring IPv6 ACLs."
ipv6_acl_mode       = CommandMode("ipv6 access-list", "IPv6-Access-List Config", ipv4_acl_desc)

aaa_ias_desc        = \
"Contains configuration options for users in the IAS database."
aaa_ias_mode        = CommandMode("aaa ias-username", "AAA IAS User Config", aaa_ias_desc)

mailserver_desc     = \
"Contains configuration commands for SMTP mailserver (email alerts)."
mailserver_mode     = CommandMode("mail-server", "Mail Server Config", mailserver_desc)
