#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from openstack_api_utils import get_auth_token
import sys

# dohvacanje tokena za autentifikaciju korsnika
auth_token = get_auth_token()
headers = {'X-Auth-Token': auth_token}

# dohvacanje URL-a(endpointa) neutron servisa
r = requests.get("http://10.30.1.2:5000/v3/auth/catalog", headers=headers)
results_json = r.json()

#iteriranje po json datoteci da bi se izvukao URL
for catalog_entry in results_json["catalog"]:
    if catalog_entry["name"] == "neutron":
        for endpoint in catalog_entry["endpoints"]:
            if endpoint["interface"] == "public":
                neutron_endpoint = endpoint["url"]





# trazi unos naziva mreze od korisnika
name = raw_input('\nEnter exact network name: ')





# dohvaca id mreze cije ime je korisnik unio
r = requests.get(neutron_endpoint + "/v2.0/networks?name=" + name + "&fields=id", headers=headers)
print("Finding network...")
print(r.status_code, r.reason)
results_json = r.json()

# provjera ima li rezultata pretrage, ako ih nema rezults_json ce biti prazan (len ce biti nula)
if len(results_json["networks"]) > 0:
	net_dict = results_json['networks'][0]
	network_id = net_dict['id']
	print('Found network %s with id %s' % (name, network_id))
else:
   	sys.exit("Network not found.")

# dohvacanje id-ja javne mreze te id-ja subneta javne mreze
r = requests.get(neutron_endpoint + "/v2.0/networks?name=admin_floating_net", headers=headers)
print(r.status_code, r.reason)
results_json = r.json()

# provjera ima li rezultata pretrage, ako ih nema rezults_json ce biti prazan (len ce biti nula) 
if len(results_json["networks"]) > 0:
	net_dict = results_json['networks'][0]
	public_network_id = net_dict['id']
	public_subnet_id = net_dict['subnets'][0]
	
	print('Found public network with id %s' %  public_network_id)
	print ('Found public subnet id %s' % public_subnet_id)
else:
	sys.exit("Public network not found.")



headers = {
	'X-Auth-Token': auth_token,
	'Content-Type': 'application/json'
}
data = {
	"router": {
		"name": "new_API_router",
		"external_gateway_info": {
            "network_id": public_network_id,
            "enable_snat": "true",
            "external_fixed_ips": [
                {
                    "ip_address": "10.30.2.171",
                    "subnet_id": public_subnet_id
                }
            ]
        },
		"admin_state_up": "true"
	}
}

r = requests.post(neutron_endpoint + "/v2.0/routers", headers=headers, data=json.dumps(data))
print "Creating router..."
print(r.status_code, r.reason)
results_json = r.json()
print json.dumps(results_json, indent=4)
router_id = results_json["router"]["id"]



data = {
		'port': {
			'admin_state_up': True,
			'network_id': network_id,
			'fixed_ips': [{"ip_address": "10.20.0.126"}]
		}
}

r = requests.post(neutron_endpoint + "/v2.0/ports", headers=headers, data=json.dumps(data))
print "Creating port..."
print(r.status_code, r.reason)
results_json = r.json()
if len(results_json["port"]) > 0:
	net_dict = results_json['port']
	port_id = net_dict['id']
	print('Created port %s with id %s' % (name, port_id))

#print json.dumps(results_json, indent=4)






data = {
		"port_id":port_id
}

r = requests.put(neutron_endpoint + "/v2.0/routers/"+router_id+"/add_router_interface", headers=headers, data=json.dumps(data))
print "Adding interface to router ..."
print(r.status_code, r.reason)
results_json = r.json()
print json.dumps(results_json, indent=4)


