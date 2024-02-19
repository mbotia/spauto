from ncclient import manager
import sys
import xml.dom.minidom
import xmltodict

# XML filter to issue with the get operation
hostname_filter = ['''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                        <hostname/>
                    </native>
                </filter>
                    ''',
                    '''
                <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                    <host-names xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-shellutil-cfg"/>
                </filter>
                    '''
                    ]
interface_filter = ['''
                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
                    </filter>
                    ''',
                    '''
                    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"/>
                    </filter>
                    ''']

interface_tag = ["name", "interface-name"]
hostname_tag = ["hostname", "host-name"]

devices = [{"HOST":"192.168.200.81", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxe" },
           {"HOST":"192.168.200.82", "USER":"cisco", "PASSWORD":"cisco", "PLATFORM" : "iosxr"}]


for device in devices:
    with manager.connect(host=device["HOST"], port=830,  device_params={"name":device["PLATFORM"]},
                            username=device["USER"], password=device["PASSWORD"], hostkey_verify = False ) as m:
        try:    
            if device["PLATFORM"] == "iosxe":
                index = 0
            else:
                index = 1

            result = m.get_config("running", hostname_filter[index])          
            # Pass the XML result as a string to the parseString function
            xml_doc = xml.dom.minidom.parseString(result.xml)
            #print(xml_doc.toprettyxml())
            hostname = xml_doc.getElementsByTagName(hostname_tag[index])
            print(hostname[0].firstChild.nodeValue)

            result = m.get_config('running', interface_filter[index])
            xml_doc = xml.dom.minidom.parseString(result.xml)
            #print(xml_doc.toprettyxml())
            interfaces = []
            interface_name = xml_doc.getElementsByTagName(interface_tag[index])
            number_int = len(interface_name)
            index = 0
            while index < number_int:
                interfaces.append(interface_name[index].firstChild.nodeValue)
                index += 1

            print(interfaces)

        except:
            print("N/A")
        