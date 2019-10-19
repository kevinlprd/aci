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

# Enter data for BD
tenant = input('Enter Tenant Name:')
bd_Name = input('Enter BD Name:')
arp_Flood = input('Enter ARP Flood mode: "true" or "false":')
mac_Flood = input('Enter MAC Flood mode: "flood" or "proxy":')
unkMcast_Flood = input('Enter unknown Multicast Flood mode: "flood" or "opt-flood":')
vrf_Name = input('Enter VRF Name:')
sub_IP = input('Enter Subnet IP or "none" for L2 only:')

if sub_IP != 'none':

	sub_Scope = input('Enter Subnet Scope: "private" or "public":')

	jsondata = '''
	{
	  	"fvBD": {
			"attributes": {
			"arpFlood": "%s",
			"ipLearning": "yes",
			"limitIpLearnToSubnets": "no",
			"mac": "00:22:BD:F8:19:FF",
			"mcastAllow": "no",
			"multiDstPktAct": "bd-flood",
			"name": "%s",
			"type": "regular",
			"unicastRoute": "yes",
			"unkMacUcastAct": "%s",
			"unkMcastAct": "%s",
			"vmac": "not-applicable"
		},
			"children": [
				{
					"fvRsCtx": {
						"attributes": {
							"tnFvCtxName": "%s"
						}
					}
				},
		    	{
			    	"fvSubnet": {
				    	"attributes": {
					    	"ip": "%s",
					    	"preferred": "no",
					    	"scope": "%s",
					    	"virtual": "no"
						}
					}
		  		}
			]
	  	}
	}
	''' % (arp_Flood, bd_Name, mac_Flood, unkMcast_Flood, vrf_Name, sub_IP, sub_Scope)
else:
	jsondata = '''
	{
	  	"fvBD": {
			"attributes": {
			"arpFlood": "%s",
			"ipLearning": "yes",
			"limitIpLearnToSubnets": "no",
			"mac": "00:22:BD:F8:19:FF",
			"mcastAllow": "no",
			"multiDstPktAct": "bd-flood",
			"name": "%s",
			"type": "regular",
			"unicastRoute": "yes",
			"unkMacUcastAct": "%s",
			"unkMcastAct": "%s",
			"vmac": "not-applicable"
		},
			"children": [
				{
					"fvRsCtx": {
						"attributes": {
							"tnFvCtxName": "%s"
						}
					}
				},
			]
	  	}
	}
	''' % (arp_Flood, bd_Name, mac_Flood, unkMcast_Flood, vrf_Name)

r = s.post('https://{0}/api/node/mo/uni/tn-{1}/BD-{2}.json'.format(apic,tenant,bd_Name), cookies=cookies, data=jsondata, verify=False)
print (jsondata)
print(r.status_code)
 