import sys
import logging
from ncclient import manager
from lxml import etree
from difflib import context_diff


def pretty_print(retval):
    print(etree.tostring(retval.data, pretty_print=True))

def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)

if __name__ == '__main__':


    log = logging.getLogger(__name__)


    host="192.168.200.81"

    filter = '''
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <Loopback>
            <name>101</name>
          </Loopback>
          <GigabitEthernet>
          </GigabitEthernet>
        </interface>
      </native>
    '''


    config = '''<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <Loopback>
            <name>101</name>
            <ip>
                <address>
                <primary>
                    <address>2.2.2.2</address>
                    <mask>255.255.255.255</mask>
                </primary>
                </address>
            </ip>
            <description>hello</description>
        </Loopback>
        </interface>
    </native>
    </config>
    '''

    config_ospf = '''<config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <router>
          <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
            <id>1</id>
            <network>
              <ip>2.2.2.2</ip>
              <mask>0.0.0.0</mask>
              <area>0</area>
            </network>
          </ospf>
        </router>
      </native>
    </config>
    '''

    with manager.connect(host=host, port=830, username="cisco", password = "cisco", hostkey_verify=False, device_params={'name':'iosxe'}) as m: 
        c = m.get_config(source='running').data_xml
        with open("%s.xml" % host, 'w') as f:
            f.write(c)
        
        running_before = m.get_config(source='running', filter=('xpath', '/native')).data

        m.edit_config(target='candidate', config=config)
        m.commit()

        m.edit_config(target='candidate', config=config_ospf)
        m.commit()
        
        running_after = m.get_config(source='running', filter=('subtree', filter)).data
        candidate_after = m.get_config(source='candidate', filter=('xpath', '/native')).data
        
        running_before_xml = etree.tostring(running_before, pretty_print=True)
        running_after_xml = etree.tostring(running_after, pretty_print=True)
        candidate_after_xml = etree.tostring(candidate_after, pretty_print=True)

        #
        # remember to skip the first few lines that have timestamps & stuff that may differ
        #

        print(running_after_xml.decode())

        #print('\n'.join(context_diff(running_after_xml.decode().splitlines(),
        #                            candidate_after_xml.decode().splitlines())))





