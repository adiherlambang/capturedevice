from netmiko import ConnectHandler
import os.path

def connect_device(ip,usr,pas,sec):
    ### Proses Connect ke Device
    device = {
        'device_type': 'cisco_ios'
    }

    device['host'] = ip
    device['username'] = usr
    device['password'] = pas
    device['secret'] = sec

    #Function dari modul netmiko
    connect_device = ConnectHandler(**device)
    connect_device.enable()

    print("connecting to device: "+ip)

    #Mencari Hostname
    req_hostname = connect_device.send_command('show running-config | in hostname')
    split_hostname = req_hostname.split()

    return split_hostname[1]