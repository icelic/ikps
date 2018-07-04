import requests
import json
from openstack_api_utils import get_auth_token, get_endpoint
import time

MENU_OPTIONS = [
    "Korisnici",
    "Instance",
    "Kontinuirano pracenje",
    "Kraj rada"
]

USER_SUBMENU_OPTIONS = [
    "Ispis svih korisnika",
    "Natrag"
]

INSTANCE_SUBMENU_OPTIONS = [
    "Ispis svih instanci",
    "Ispis svih aktivnih instanci",
    "Ispis svih instanci s greskom",
    "Ispis svih instanci koje se kreiraju",
    "Ispis svih instanci za nekog korisnika",
    "Natrag"
]

auth_token = get_auth_token()
headers = {'X-Auth-Token': auth_token}

nova_endpoint = get_endpoint("nova", auth_token)


def list_instances(filter):
    if filter == 'all':
        r = requests.get(nova_endpoint + "/servers", headers=headers)
        json_data = r.json()
        print("\n----------------------------------------------------------------------")
        print("Sve instance")
        print("----------------------------------------------------------------------")
        for server in json_data["servers"]:
            print(server["name"])
        print("----------------------------------------------------------------------")
    elif filter == 'active' or filter == 'error' or filter == 'build':
        r = requests.get(nova_endpoint + "/servers?status=" + filter, headers=headers)
        json_data = r.json()
        print("\n----------------------------------------------------------------------")
        print("Servers with status " + filter)
        print("----------------------------------------------------------------------")
        for server in json_data["servers"]:
            print(server["name"])
        print("----------------------------------------------------------------------")
    else:
        print("Netocan argument: " + filter + ".\nArgument mora biti: 'all', 'active', 'error' ili 'build'")


def list_instances_for_user(user_id):
    if filter == 'all':
        r = requests.get(nova_endpoint + "/servers", headers=headers)
        json_data = r.json()
        print("\n----------------------------------------------------------------------")
        print("Sve instance za korisnika: " + user_id)
        print("----------------------------------------------------------------------")
        for server in json_data["servers"]:
            print(server["name"])
        print("----------------------------------------------------------------------")
    else:
        print("Netocan argument: " + filter + ".\nArgument mora biti: all, active, error, build ili user id")


def list_users():
    r = requests.get("http://10.30.1.2:5000/v3/users", headers=headers)
    results_json = r.json()
    print("\n----------------------------------------------------------------------")
    print("Korisnici")
    print("----------------------------------------------------------------------")
    for user in results_json["users"]:
        print repr(user["id"]).ljust(30) + repr(user["name"]).rjust(40)
    print("----------------------------------------------------------------------\n")


def servers_changed(old_servers, new_servers):
    result = set(old_servers) ^ set(new_servers)
    if not result:
        return False
    else:
        return True 


servers = []
selected_menu_option = 2000

r = requests.get(nova_endpoint + "/servers", headers=headers)
json_data = r.json()
for server in json_data["servers"]:
    servers.append(server["name"])
servers_count = len(servers)

while(selected_menu_option != str(len(MENU_OPTIONS))):
    print("IZBORNIK:")
    for i, option in enumerate(MENU_OPTIONS):
        print("%d. %s" % (i+1, option))
    selected_menu_option = raw_input('Unesite broj zeljene opcije: ')

    if selected_menu_option == '1':
        selected_submenu_option = 2000
        while(selected_submenu_option != str(len(USER_SUBMENU_OPTIONS))):
            print("KORISNICI:")
            for i, option in enumerate(USER_SUBMENU_OPTIONS):
                print("%d. %s" % (i+1, option))

            selected_submenu_option = raw_input('Unesite broj zeljene opcije: ')
            if selected_submenu_option == '1':
                list_users()

    elif selected_menu_option == '2':
        selected_submenu_option = 2000
        while(selected_submenu_option != str(len(INSTANCE_SUBMENU_OPTIONS))):
            print("INSTANCE :")
            for i, option in enumerate(INSTANCE_SUBMENU_OPTIONS):
                print("%d. %s" % (i+1, option))
            selected_submenu_option = raw_input('Unesite broj zeljene opcije: ')
            if selected_submenu_option == '1':
                list_instances("all")
            elif selected_submenu_option == '2':
                list_instances("active")
            elif selected_submenu_option == '3':
                list_instances("error")
            elif selected_submenu_option == '4':
                list_instances("build")
            elif selected_submenu_option == '5':
                user_id = input("Unesite id korisnika: ")
                list_instances(user_id)
    elif selected_menu_option == '3':
        user_input = 'a'
        while user_input != 'q':
            for i in range(10):
                new_servers = []
                r = requests.get(nova_endpoint + "/servers", headers=headers)
                json_data = r.json()
                for server in json_data["servers"]:
                    new_servers.append(server["name"])
                servers_count = len(servers)
                if servers_changed(servers, new_servers):
                    print "Server added or removed"
                    servers = new_servers
                time.sleep(30)
                user_input = raw_input("Za povratak na izbornik odaberite 'q', a za nastavak 'c': ")
                if user_input == 'q':
                    break
