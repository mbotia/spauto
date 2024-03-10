from ncclient import manager

devices = [{"HOST":"192.168.200.81", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxe"},
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
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface operation="delete">
      <name>{name}</name>
    </interface>
  </interfaces>
</config>""".format(**loopback_interface),
"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg">
    <interface-configuration xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
      <active>act</active>
      <interface-name>{name}</interface-name>
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

networkadd_ospf_template = ["""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <router>
      <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
        <ospf>
          <process-id>
            <id>1</id>
            <network>
              <ip>10.0.0.120</ip>
              <wildcard>0.0.0.0</wildcard>
              <area>0</area>
            </network>
          </process-id>
        </ospf>
      </router-ospf>
    </router>
  </native>
</config>
""","""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
   <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-ospf-cfg">
   <processes>
    <process>
     <process-name>1</process-name>
     <default-vrf>
      <area-addresses>
       <area-area-id>
        <area-id>0</area-id>
        <running/>
        <name-scopes>
         <name-scope>
          <interface-name>Loopback120</interface-name>
          <running/>
          <passive>true</passive>
         </name-scope>
        </name-scopes>
       </area-area-id>
      </area-addresses>
     </default-vrf>
     <start/>
    </process>
   </processes>
  </ospf>
</config>
"""]

add_static_template = ["""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <ip>
        <route>
          <ip-route-interface-forwarding-list>
            <prefix>120.0.0.0</prefix>
            <mask>255.255.255.0</mask>
            <fwd-list>
              <fwd>192.168.200.1</fwd>
            </fwd-list>
          </ip-route-interface-forwarding-list>
        </route>
      </ip>
    </native>
</config>
""","""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <router-static xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ip-static-cfg">
   <default-vrf>
    <address-family>
     <vrfipv4>
      <vrf-unicast>
       <vrf-prefixes>
        <vrf-prefix>
         <prefix>120.0.0.0</prefix>
         <prefix-length>24</prefix-length>
         <vrf-route>
          <vrf-next-hop-table>
           <vrf-next-hop-next-hop-address>
            <next-hop-address>192.168.200.1</next-hop-address>
           </vrf-next-hop-next-hop-address>
          </vrf-next-hop-table>
         </vrf-route>
        </vrf-prefix>
       </vrf-prefixes>
      </vrf-unicast>
     </vrfipv4>
    </address-family>
   </default-vrf>
  </router-static>
</config>
"""]


# Iterate through each device and perform configuration tasks
for device in devices:
    with manager.connect(host=device["HOST"], username=device["USER"], password=device["PASSWORD"],
                         device_params={"name": device["PLATFORM"]}, hostkey_verify=False, look_for_keys=False) as m:
        if device["PLATFORM"] == "iosxe":
            index = 0
        else:
            index = 1
        try:
            # Delete Loopback Interface
            response = m.edit_config(target="candidate", config=delete_interface_template[index])
            m.commit()
            print(f"Loopback interface {loopback_interface['name']} deleted successfully on {device['HOST']}")

            # Create Loopback Interface
            response = m.edit_config(target="candidate", config=create_interface_template[index])
            m.commit()
            print(f"Loopback interface {loopback_interface['name']} created successfully on {device['HOST']}")

            # Add OSPF Network
            response = m.edit_config(target="candidate", config=networkadd_ospf_template[index])
            m.commit()
            print(f"OSPF network added successfully on {device['HOST']}")

            # Add Static Route
            response = m.edit_config(target="candidate", config=add_static_template[index])
            m.commit()
            print(f"Static route added successfully on {device['HOST']}")
        except:
            continue

