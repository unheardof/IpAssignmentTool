HACKTAVIST_IP_FILE = 'hacktavist_ip_blocks.txt'
APT_IP_FILE = 'apt_ip_blocks.txt'
INFRASTRUCTURE_IP_FILE = 'infrastructure_ip_blocks.txt'

HACKTAVIST_IP_TYPE = 'hacktavist'
APT_IP_TYPE = 'apt'
INFRASTRUCTURE_IP_TYPE = 'infrastructure'

hacktavist_ip_list = []

# 30.181.0.0 / 30.210.255.255
[ hacktavist_ip_list.append("30.%d.0.0/16" % x) for x in range(181, 210 + 1) ]

# 40.31.0.0 / 40.40.255.255
[ hacktavist_ip_list.append("40.%d.0.0/16" % x) for x in range(31, 40 + 1) ]
    
# 50.181.0.0 / 50.210.255.255
[ hacktavist_ip_list.append("50.%d.0.0/16" % x) for x in range(181, 210 + 1) ]
        
# 60.31.0.0 / 60.60.255.255
[ hacktavist_ip_list.append("60.%d.0.0/16" % x) for x in range(31, 60 + 1) ]

apt_ip_list = []
    
# 20.31.0.0 / 20.60.255.255
[ apt_ip_list.append("20.%d.0.0/16" % x) for x in range(31, 60 + 1) ]
                
# 30.211.0.0 / 30.240.255.255
[ apt_ip_list.append("30.%d.0.0/16" % x) for x in range(211, 240 + 1) ]
                    
# 40.0.0.0 / 40.30.255.255
[ apt_ip_list.append("40.%d.0.0/16" % x) for x in range(0, 30 + 1) ]
                        
# 50.211.0.0 / 50.240.255.255
[ apt_ip_list.append("50.%d.0.0/16" % x) for x in range(211, 240 + 1) ]

infrastructure_ip_list = []
    
# 60.0.0.0 / 60.30.255.255
[ infrastructure_ip_list.append("60.%d.0.0/16" % x) for x in range(0, 30 + 1) ]
                                
# 20.0.0.0 / 20.30.255.255
[ infrastructure_ip_list.append("20.%d.0.0/16" % x) for x in range(0, 30 + 1) ]

with open(HACKTAVIST_IP_FILE, 'w') as f:
    f.write('\n'.join(hacktavist_ip_list))

with open(APT_IP_FILE, 'w') as f:
    f.write('\n'.join(apt_ip_list))

with open(INFRASTRUCTURE_IP_FILE, 'w') as f:
    f.write('\n'.join(infrastructure_ip_list))
