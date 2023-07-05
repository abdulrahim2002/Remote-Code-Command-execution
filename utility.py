import psutil
from urllib.parse import urlparse
import os

def getpath():
    '''get path of current directory'''
    return os.path.dirname(os.path.abspath(__file__))

def printUI():
    print('\nThis is telnet implementation.\n'
          'You can execute commands remotely.\n')
    print("\n")
    
# get a list of all commands available on the system
def getCommands():
    '''get a list of all commands available on the system'''
    return os.popen("help").read().split("\n")
    
'''server functions'''
# returns ip address assigned by router
def get_ip_address():
    addrs = psutil.net_if_addrs()
    if "Wi-Fi" in addrs:
        wifi_info = addrs["Wi-Fi"]
        for info in wifi_info:
            if info.family == 2: # 2 is the address family for IPv4
                return info.address
    return None
