#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dohvaćanje vanjskih funkcija
from openstack_api_utils import get_auth_token, get_endpoint
import json
import requests

# gets auth token from authenticate.py
auth_token = get_auth_token()

headers = {'X-Auth-Token': auth_token}

glance_endpoint = get_endpoint("glance", auth_token)

image_name = raw_input("\nEnter new image name: ")
image_path = raw_input("\nEnter image file location: ")

data = {
    "container_format": "bare",
    "disk_format": "qcow2",
    "name": image_name
}

headers={
    'X-Auth-Token': auth_token,
    "Content-Type": "application/json"
}

r = requests.post(glance_endpoint + "/v2/images", headers=headers, data=json.dumps(data))
print "Creating image..."

results_json = r.json()
image_id = results_json["id"]

data = open(image_path, 'rb').read()

headers={
    'X-Auth-Token': auth_token,
    "Content-Type": "application/octet-stream"
}

r = requests.put(glance_endpoint + "/v2/images/" + image_id + "/file", headers=headers, data=data)
print "Image Created!"

