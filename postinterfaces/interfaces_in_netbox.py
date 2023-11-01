import requests
import json
import pynetbox


#pip install pynetbox
NETBOX = 'http://192.168.0.160'
nb = pynetbox.api(NETBOX, token='88a5fdbd9305b1c27b1bd6080b6d8c8da209e9b3')
#post interface to netbox

NB_URL = "http://192.168.0.160"
API_TOKEN = "88a5fdbd9305b1c27b1bd6080b6d8c8da209e9b3"
HEADERS = {'Authorization': f'Token {API_TOKEN}',
           'Content-Type': 'application/json', 'Accept': 'application/json'}


#Get device id from device name
def request_devices(device_name):
    request_url = f"{NB_URL}/api/dcim/devices/?name={device_name}"
    devices = requests.get(request_url, headers=HEADERS)
    result = devices.json()
    id = result["results"][0]["id"]
    return id

def request_interface_id(device_name,interface_name):
    device_id = request_devices(device_name)
    interface = nb.dcim.interfaces.get(device_id=device_id, name=interface_name)
    print(interface)
    return interface

def post_interfaces(device_name, name_of_interface, description, type_of_interface, is_enabled_interface, interface_mode):
    id = request_devices(device_name)
    request_url = f"{NB_URL}/api/dcim/interfaces/?device={device_name}"
    interface_parameters = {
        "device": id,
        "name": name_of_interface,
        "description": description,
        "type": type_of_interface,
        "enabled": is_enabled_interface,
        "mode": interface_mode
    }
    new_interface = requests.post(
        request_url, headers=HEADERS, json=interface_parameters, verify=False)
    print(new_interface.json())

def update_interfaces(device_name, name_of_interface, description, type_of_interface, is_enabled_interface, interface_mode):
    name_of_interface = name_of_interface.rstrip('\n')
    interface = request_interface_id(device_name,name_of_interface)
    id = request_devices(device_name)
    interface_parameters = {
        "device": id,
        "name": name_of_interface,
        "description": description,
        "type": type_of_interface,
        "enabled": is_enabled_interface,
        "mode": interface_mode
    }

    interface.update(interface_parameters)

def find_ip_and_assign(device_name,interface_name, ipaddress):
    print(ipaddress+"!!!!!!!!!!!!")
    interface_id = request_interface_id(device_name, interface_name)
    device_id = request_devices(device_name)
    request_url = f"{NB_URL}/api/ipam/ip-addresses/?q={ipaddress}/"
    ipaddress1 = requests.get(request_url, headers=HEADERS)
    netboxip = ipaddress1.json()
    print(netboxip)
    print(ipaddress)
    #If ip address absent in Netbox, so create
    if netboxip['count'] == 0:
        print(repr(ipaddress))
        interface_id = request_interface_id(device_name, interface_name)
        new_ip = nb.ipam.ip_addresses.create(address=ipaddress,status="active",interface=interface_id)
        print(new_ip)
        
    #if ip address exists in netbox
    else:
        interface_id = request_interface_id(device_name, interface_name)
        url = netboxip['results'][0]['url']
        ipaddress = ipaddress.rstrip('\n')
        update = {
                "address": ipaddress,
                "dns_name": device_name,
                "assigned_object_id": interface_id,
                "assigned_object_type": "dcim.interface"
            }
        change = requests.patch(url, headers=HEADERS,
                                data=json.dumps(update), verify=False)
        print(change)


