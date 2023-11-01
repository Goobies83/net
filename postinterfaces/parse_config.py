from ciscoconfparse import CiscoConfParse
from interfaces_in_netbox import *

device_name = "R1"
file1 = open('C:\\temp\\conf\\192.168.0.22.cfg', 'r')
config = file1.readlines()

def get_interfaces_and_description(config, device_name):
    #load config
    intf_obj_sh_list = []
    
    parse = CiscoConfParse(config, syntax='ios')
    # extract the interface name and description
    # first, we get all interface commands from the configuration
    # Choose the first interface (parent) object
    ##################################################
    # Define ans collect list of disabled interfaces #
    ##################################################
    for intf_obj_sh in parse.find_objects_w_child('^interface', '^\s+shutdown'):
        print(intf_obj_sh.text)
        intf_obj_sh_list.append(intf_obj_sh.text)
       
    for intf_obj in parse.find_objects('^interface'):
        ######################
        #  Define interfaces #
        ######################
        name_of_interface = str(intf_obj.text)
        print(name_of_interface)

        #####################
        # Define IP address #
        #####################
        ipaddress = intf_obj.re_match_iter_typed(r'ip\saddress\s(\d+\.\d+\.\d+\.\d+)\s', result_type=str, group=1, default='')
        print(ipaddress)
                
        ######################
        # Define description #
        ######################
        description = intf_obj.re_match_iter_typed(r'description\s(\w+.*)', result_type=str, group=1, default='')
        print(description)
        ########################################
        # Define if port in access and it vlan #
        ########################################
        vlanacess = intf_obj.re_match_iter_typed(r'^\sswitchport\saccess\svlan\s(\d+.*)', result_type=int, untyped_default=True, default='')
        vlantrunk = intf_obj.re_match_iter_typed(
            r'\s+switchport\strunk\sallowed\svlan\s(add\s)?(.*)$',  untyped_default=True, default='')
        if vlanacess:
            print("Access mode")
            print(vlanacess)
            interface_mode = "access"
        elif vlantrunk:
           print("Trunk mode")
           print(vlantrunk)
           interface_mode = "tagged-all"
        else:
            interface_mode = "access"

        ############################
        # Define type of interface #
        ############################100gbase-x-qsfp28
        if "Hundred" in name_of_interface:
            type_of_interface = "100gbase-x-qsfp28"
        elif "Forty" in name_of_interface:
            type_of_interface = "40gbase-x-qsfpp"
        elif "Twe" in name_of_interface:
            type_of_interface = "25gbase-x-sfp28"
        elif "Ten" in name_of_interface:
            type_of_interface = "10gbase-x-sfpp"
        elif "Giga" in name_of_interface:
            type_of_interface = "1000base-t"
        elif "Fast" in name_of_interface:
            type_of_interface = "100base-tx"
        elif "Port" in name_of_interface:
            type_of_interface = "lag"
        else:
            type_of_interface = "virtual"
        print(type_of_interface)
         
        ##############################
        # Define disabled interfaces #
        ##############################
        if name_of_interface in intf_obj_sh_list:
            print("Interface Disabled")
            is_enabled_interface = "False"
        else:
            print("Interface Enabled")
            is_enabled_interface = "True"
        
        ###########################
        # Run script              #
        ########################### 
        
        try:
            update_interfaces(device_name, name_of_interface, description, type_of_interface, is_enabled_interface, interface_mode)
            find_ip_and_assign(device_name,name_of_interface, ipaddress)
        except AttributeError:
            post_interfaces(device_name, name_of_interface, description,
                           type_of_interface, is_enabled_interface, interface_mode)
            find_ip_and_assign(device_name,name_of_interface, ipaddress)

if __name__ == "__main__":
    get_interfaces_and_description(config, device_name)