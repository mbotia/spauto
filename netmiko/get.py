from netmiko import ConnectHandler

devices = [{
    "device_type": "cisco_xr",
    "ip": "192.168.200.82",
    "username": "cisco",
    "password": "cisco",
    "port": "22",
}, {
    "device_type": "cisco_xe",
    "ip": "192.168.200.81",
    "username": "cisco",
    "password": "cisco",
    "port": "22",
}]

for device in devices:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show version")
    output2 = net_connect.send_command("show ip interface brief", use_textfsm=True)
    net_connect.disconnect()
    result = output.find('uptime is')
    begin = int(result)
    end = begin + 38
    print(device['ip'] + " => " + output[int(begin):int(end)])

    print ("\n", output2)