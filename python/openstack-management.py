import requests
import json
from openstack_api_utils import get_auth_token, get_endpoint
import sys

auth_token = get_auth_token()
headers = {'X-Auth-Token': auth_token}

endpoint = get_endpoint("nova", auth_token)

print endpoint

r = requests.get("http://10.30.1.2:5000/environments", headers=headers)
print(r.status_code, r.reason)
json_data = r.json()