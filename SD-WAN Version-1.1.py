from netmiko import ConnectHandler, ssh_exception
import re
import getpass

def ssh_connect(device, output):
    try:
        device = {
            "host" : input("Enter Device IP Address: "),
            "username" : input("Username: "),
            "password" : getpass.getpass("Password: "),
            "device_type" : "cisco_ios",
            "fast_cli" : True    
        }
        with ConnectHandler(**device) as device_connect:
            device_connect.enable()
        

    except(ssh_exception.NetMikoAuthenticationException,ssh_exception.NetmikoTimeoutException,ssh_exception.AuthenticationException):
        print("Authentication Failed")

        

    
    

    

