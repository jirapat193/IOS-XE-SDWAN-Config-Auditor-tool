from netmiko import ConnectHandler, ssh_exception
import re
import getpass
import signal
import sys

def sigint_handler(signal, frame):
    print ('Keyboard interrupt')
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

print("\nIOS-XE SD-WAN Onbording Configuration Auditor Tool\n")

device = {
        "host" : input("Enter Device IP Address: "),
        "username" : input("Username: "),
        "password" : getpass.getpass("Password: "),
        "device_type" : "cisco_ios",
        "fast_cli" : True    
    }

def device_audit():
    try:
        with ConnectHandler(**device) as device_connect:
            print("Auditing configuration..\n")
            device_connect.enable()

        # checking sdwan tunnel interface configration
            tunnel_config = device_connect.send_command("sh run | incl interface Tunnel")
            sdwan_tunnel_config = device_connect.send_command("sh sdwan run | incl tunnel-interface")

            match_reg_tunnel_intf = re.search(r"interface\sTunnel\d", tunnel_config)
            match_sdwan_tunnel_intf = re.search(r"tunnel\-interface", sdwan_tunnel_config)
    
            print("Tunnel interface configuration checking...")
            if match_reg_tunnel_intf:
                print("Tunnel interface check passed\n")
            else:
                print("Tunnel interface configuration not found\n")

            print("SD-WAN Tunnel interface configuration checking..")
            if match_sdwan_tunnel_intf:
                print("SD-WAN Tunnel interface check passed\n")
            else:
                print("SD-WAN Tunnel interface configuration not found\n")

        # checking default route configuration
            route_config = device_connect.send_command("sh run | sec ip route")
            match_route = re.search(r"ip\sroute\s\d", route_config)
            print ("Default route configuration checking..")

            if match_route:
                print("Default route check passed\n")
            else:
                print("No default route configured\n")

        # checking ip name-server (dns server) confiuration
            dns_config = device_connect.send_command("sh run | sec ip name-server")
            match_dns = re.search(r"ip\sname-server\s\d", dns_config)
            print("DNS configuration checking..")

            if match_dns:
                print("DNS check passed\n")
            else:
                print("No ip name-server configured\n")

        # checking system-ip configuration
            system_ip_config = device_connect.send_command("sh sdwan run | incl system-ip")
            match_system_ip = re.search(r"system\-ip\s\s\s\s\s\s\s\s\s\s\s\s\s\d", system_ip_config)
            print("System ip checking..")

            if match_system_ip:
                print("System ip check passed\n")
            else:
                print("System ip configuration not found\n")

        # checking vBond configuration
            vbond_config = device_connect.send_command("sh sdwan run | incl vbond")
            match_vbond = re.search(r"vbond\s\d", vbond_config)
            print("vBond configuration checking..")    

            if match_vbond:
                print("vBond check passed\n")
            else:
                print("vBond configuration not found\n")

        # checking organization name configuration
            organization_name_config = device_connect.send_command("sh sdwan run | incl organization-name")
            match_sp_organization_name = re.search(r"^\ssp", organization_name_config)
            match_organization_name = re.search(r"\n\s\w\w\w", organization_name_config, re.MULTILINE)
            print("SP-Organization name configuration checking..")
   
            if match_sp_organization_name:
                print("SP-Organization-name check passed\n")
            else:
                print("SP-Organization-name configuration not found\n")

            print("Organization name configuration checking..")
            if match_organization_name:
                print("Organization-name check passed\n")
            else:
                print("Organization-name configuration not found\n")
    
        # checking site-id configuration
            site_id_config = device_connect.send_command("sh sdwan run | incl site-id")
            match_site_id = re.search(r"site\-id",site_id_config)
            print("Site-id configuration checking..")

            if match_site_id:
                print("Site-id configuration check passed\n")
            else:
                print("Site-id configuration not found\n")

            print ("Configuration Audit Succeeded\n")
    except(ssh_exception.NetMikoAuthenticationException, ssh_exception.NetMikoTimeoutException, ssh_exception.AuthenticationException):
        print("Device connecting failed please try again.\n")


def main():
    device_audit()


if __name__ == '__main__':
    main()
   
    