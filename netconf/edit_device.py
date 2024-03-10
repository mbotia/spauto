from ncclient import manager

devices = [{"HOST":"192.168.200.81", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxe" },
           {"HOST":"192.168.200.82", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxr"}]

# Define loopback interface details
loopback_interface = {
    "name": "Loopback120",
    "description": "Loopback Interface",
    "ipv4_address": "10.0.0.120",
    "type": "ianaift:softwareLoopback",
    "status": "true",
    "subnet_mask": "255.255.255.255"
}

# Creatye an XML configuration templare for delete loopback

delete_interface_template = [ """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
        	<name>{name}</name>
        </interface>
    </interfaces>
</config>""".format(**loopback_interface),
"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration xc:operation="delete">
            <interface-name>{name}</interface-name>
            <active>act</active>
        </interface-configuration>
    </interface-configurations>
</config>
""".format(**loopback_interface)]

# Create an XML configuration template for ietf-interfaces
create_interface_template = [ """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
        	<name>{name}</name>
        	<description>{description}</description>
        	<type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                {type}
            </type>
        	<enabled>{status}</enabled>
        	<ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
        		<address>
        			<ip>{ipv4_address}</ip>
        			<netmask>{subnet_mask}</netmask>
        		</address>
        	</ipv4>
        </interface>
    </interfaces>
</config>""".format(**loopback_interface),
"""
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
        <interface-configuration>
            <interface-name>{name}</interface-name>
            <description>{description}</description>
            <active>act</active>
            <interface-virtual/>
            <ipv4-network xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-io-cfg">
                <addresses>
                    <primary>
                        <address>{ipv4_address}</address>
                        <netmask>{subnet_mask}</netmask>
                    </primary>
                </addresses>
            </ipv4-network>
        </interface-configuration>
    </interface-configurations>
</config>
""".format(**loopback_interface)]

for device in devices:
    with manager.connect (host = device["HOST"], username=device["USER"], password = device["PASSWORD"], 
                          device_params = { "name": device["PLATFORM"]},
                          hostkey_verify=False, look_for_keys=False) as m:
        if device["PLATFORM"] == "iosxe":
            index = 0
        else:
            index = 1
        response = m.edit_config(target="candidate", config=delete_interface_template[index])
        m.commit()
        response = m.edit_config(target="candidate", config=create_interface_template[index])
        m.commit()
        print(f"Loopback interface {loopback_interface['name']} created successfully on {device['HOST']}")

