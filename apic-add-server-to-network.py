# Import the 'sys', 'json' and 'requests' and 'getpass' python modules
import sys
import json
import requests
import getpass
import urllib3
# From the 'urllib3' module import the insecure warning message
from urllib3.exceptions import InsecureRequestWarning
# Disable the insecure warning message
urllib3.disable_warnings(InsecureRequestWarning)
# Store data as variables for the apic, username and password
# Ask the user for APIC username
username = input('What is Login Username:')
# username = 'admin'
# Ask the user for APIC password. Getpass hides the password you type in
password = getpass.getpass('What is Login Password:')
# password = 'BMGFS3cr3t'
# Ask the user for their APIC IP address and store it in the variable'apic'
apic = input('What is the IP of your assigned APIC:')
# apic = '10.10.200.186'
# Print the variables defined above
# The "\n" character is used to delineate a new line, making output easier to read.
# print("\n"+apic+"\n"+username+"\n"+password)

# Using what we have now gathered from the variables, populate our standard auth
# JSON file, using variables
auth = {'aaaUser': {'attributes': {'name': username, 'pwd': password } }
}

# Create a 'requests' session, and store that session object as variable's'
s = requests.Session()
# print(s)

# Send an HTTPS POST to authenticate using the session that we just created and
# stored as variable 's', and send the 'auth' variable which is our JSON auth
# data
# Using the variable 's' with a '.' and another word is simply calling a object/
# method in a class from the requests python module, but as an extension of an
# already-created session
r = s.post('https://{0}/api/mo/aaaLogin.json'.format(apic),
data=json.dumps(auth), verify=False)
print(r)

# The variable 'r' now is packed with a lot of good information
# Find out what the HTTP Status is, and pack that info in the variable 'status'
status = r.status_code
print(status)
cookies = r.cookies

# Enter data for port
leaf_name = input('Enter Leaf Name:')
mod_start = input('Enter fromCard No.:')
mod_end = input('Enter toCard No.:')
port_start = input('Enter fromPort No.:')
port_end = input('Enter toPort No.:')
port_name = input('Enter the Port Name:')
port_type = input('Please choose the Port Type: accportgrp or accbundle:')
pol_group = input('Please choose the Port Policy:')

# Enter data for EPG
tenant = input('Enter Tenant Name:')
ap_name = input('Enter Application Profile Name: PRD or DEV:')
epg_name = input('Enter EPG Name:')
#leaf_name = input('Enter LEAF Switch No.:')
port_no = input('Enter Port No.(i.e. eth1/48):')
encap_vlan = input('Enter EnCap VLAN No.:')
mode = input('Enter Port Mode(for Trunk, use "regular"; for Access, use "native"):')

jsondata = '''
{
    "infraHPortS": {
        "attributes": {
            "name": "%s",
            "dn": "uni/infra/accportprof-%s/hports-%s-typ-range",
            "status": "",
            "type": "range"
        },
        "children": [
            {
                "infraRsAccBaseGrp": {
                    "attributes": {
                        "fexId": "101",
                        "rn": "rsaccBaseGrp",
                        "tDn": "uni/infra/funcprof/%s-%s",
                        "status": "created,modified"
                    }
                }
            },
            {
                "infraPortBlk": {
                    "attributes": {
                        "fromCard": "%s",
                        "toCard": "%s",
                        "fromPort": "%s",
                        "toPort": "%s",
                        "name": "block2",
                        "rn": "portblk-block2",
                        "descr": "%s"
                        "status": "created,modified"
                    }
                }
            }
        ]
    }
}
''' % (port_name, leaf_name, port_name, port_type, pol_group, mod_start, mod_end, port_start, port_end, port_name)
r = s.post('https://{0}/api/mo/uni/infra/accportprof-{1}/hports-{2}-typ-range.json'.format(apic,leaf_name,port_name), cookies=cookies, data=jsondata, verify=False)
print (jsondata)
print(r.status_code)
if r.status_code = 200:
    jsondata = '''
    {
      "fvRsPathAtt": {
        "attributes": {
          "encap": "vlan-%s",
          "mode": "%s",
          "status": "created",
          "tDn": "topology/pod-1/paths-%s/pathep-[%s]"
        },
        "children":[]
      }
    }
    ''' % (encap_vlan, mode, leaf_name, port_no)
    r = s.post('https://{0}/api/mo/uni/tn-{1}/ap-{2}/epg-{3}.json'.format(apic,tenant,ap_name,epg_name), cookies=cookies, data=jsondata, verify=False)
    print (jsondata)
    print(r.status_code)
else:
    print('Port config error')
    exit()
