from ncclient import manager
import sys

devices = [{"HOST":"192.168.200.81", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxe" },
           {"HOST":"192.168.200.82", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxr"}]

for device in devices:
    with manager.connect (host = device["HOST"], 
                          username=device["USER"], password = device["PASSWORD"], device_params = { "name": device["PLATFORM"]},
                          hostkey_verify=False) as m:
        c = m.get_config(source='running').data_xml
        with open("%s.xml" % device["HOST"], 'w') as f:
            f.write(c)
    
        # print all NETCONF capabilities
        print(f'***Here are the Remote Devices %s Capabilities***', device["HOST"])
        with open("%s capa.txt" % device["HOST"], 'w') as f:
                f.write("\n")
        for capability in m.server_capabilities:            
            with open("%s capa.txt" % device["HOST"], 'a') as f:
                f.write(capability + "\n")




