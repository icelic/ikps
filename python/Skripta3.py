#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dohvaćanje vanjskih funkcija
from openstack_api_utils import get_auth_token
import json
import requests

# gets auth token from authenticate.py
auth_token = get_auth_token()

headers = {'X-Auth-Token': auth_token}

r = requests.get("http://10.30.1.2:5000/v3/auth/catalog", headers=headers)
results_json = r.json()
for catalog_entry in results_json["catalog"]:
    if catalog_entry["name"] == "neutron":
        for endpoint in catalog_entry["endpoints"]:
            if endpoint["interface"] == "public":
                neutron_endpoint = endpoint["url"]

#print neutron_endpoint

data = {
    "network": {"name": "StudentNet"}
}

headers={
    'X-Auth-Token': auth_token,
    "Content-Type": "application/json"
}

r = requests.post(neutron_endpoint + "/v2.0/networks", headers=headers, data=json.dumps(data))
#print(r.status_code, r.reason)
#print r.json()
results_json = r.json()

net_dict = results_json['network']
network_id = net_dict['id']
print('Network %s created' % network_id)
#print json.dumps(results_json, indent=4)
#net_dict = results_json['network']
#network_id = results_json['id']
#print('Network %s created' % network_id)




#creating subnets

data = {
     "subnet":{"name":"StudentSubnet","cidr":"120.1.2.0/24","ip_version":4,
           "network_id":network_id}
}

headers={
    'X-Auth-Token': auth_token,
    "Content-Type": "application/json"
}

r = requests.post(neutron_endpoint + "/v2.0/subnets", headers=headers, data=json.dumps(data))
#print(r.status_code, r.reason)
#print r.json()
results_json = r.json()
subnet_dict = results_json['subnet']
subnet_name = subnet_dict['name']
print('Subnet %s created' % subnet_name)

