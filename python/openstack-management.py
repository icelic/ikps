import requests
import json
from openstack_api_utils import get_auth_token, get_endpoint
import time

MENU_OPTIONS = [
    "Korisnici",
    "Instance",
    "Kontinuirano pracenje",
    "Statistika",
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

STATISTICS_SUBMENU_OPTIONS = [
    "Statistika za sve projekte",
    "Statistika za odredjen projekt",
    "Natrag"
]

auth_token = get_auth_token()
headers = {'X-Auth-Token': auth_token}

nova_endpoint = get_endpoint("nova", auth_token)


def list_instances(filter):
    if filter == 'all':
        instance_count = 0
        r = requests.get(nova_endpoint + "/servers", headers=headers)
        json_data = r.json()
        print("\n----------------------------------------------------------------------")
        print("Sve instance")
        print("----------------------------------------------------------------------")
        for server in json_data["servers"]:
            instance_count += 1
            print(server["name"])
        print("----------------------------------------------------------------------")
        print "Broj svih instanci je: " + str(instance_count)
        print("----------------------------------------------------------------------")
    elif filter == 'active' or filter == 'error' or filter == 'build':
        instance_count = 0
        r = requests.get(nova_endpoint + "/servers?status=" + filter, headers=headers)
        json_data = r.json()
        print("\n----------------------------------------------------------------------")
        print("Instance sa statusom " + filter)
        print("----------------------------------------------------------------------")
        for server in json_data["servers"]:
            instance_count += 1
            print(server["name"])
        print("----------------------------------------------------------------------")
        print "Broj instanci sa statusom " + filter + " je: " + str(instance_count)
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
        print repr(user["id"]).ljust(30) + repr(user["name"]).rjust(90)
    print("----------------------------------------------------------------------\n")


def print_statistics():
    r = requests.get(nova_endpoint + "/os-simple-tenant-usage", headers=headers)
    json_data = r.json()
    for tenant in json_data["tenant_usages"]:
        print("\n----------------------------------------------------------------------")
        print("Statistika za projekt: " + tenant["tenant_id"])
        print("----------------------------------------------------------------------")
        for key, value in tenant.iteritems():
            if(key != "tenant_id"):
                print key + ": " + str(value)
        print("----------------------------------------------------------------------")


def servers_changed(old_servers, new_servers):
    result = set(old_servers) ^ set(new_servers)
    if not result:
        return False
    else:
        return True


server_ids = []
server_names = []
server_user_ids = []
selected_menu_option = 2000

r = requests.get(nova_endpoint + "/servers/detail", headers=headers)
json_data = r.json()
for server in json_data["servers"]:
    server_ids.append(server["id"])
    server_names.append(server["name"])
    server_user_ids.append(server["user_id"])
servers_count = len(server_ids)

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
        print("Za prekid ove funkcije pritisnite tipke 'Ctrl' + 'C'")
        try:
            while True:
                for i in range(30):
                    new_server_ids = []
                    new_server_names = []
                    new_server_user_ids = []
                    r = requests.get(nova_endpoint + "/servers/detail", headers=headers)
                    json_data = r.json()
                    for server in json_data["servers"]:
                        new_server_ids.append(server["id"])
                        new_server_names.append(server["name"])
                        new_server_user_ids.append(server["user_id"])
                    servers_count = len(new_server_ids)
                    if servers_changed(server_ids, new_server_ids):
                        if len(server_ids) > len(new_server_ids):
                            print("Pobrisana je instanca: ")
                            for item in list(set(server_ids) ^ set(new_server_ids)):
                                item_index = server_ids.index(item)
                                r = requests.get("http://10.30.1.2:5000/v3/users/" + server_user_ids[item_index], headers=headers)
                                results_json = r.json()
                                user = results_json["user"]
                                print "    - instanca: " + server_names[item_index] + " od korisnika: " + user["name"]
                        elif len(server_ids) < len(new_server_ids):
                            print("Dodana je instanca: ")
                            for item in list(set(server_ids) ^ set(new_server_ids)):
                                item_index = new_server_ids.index(item)
                                r = requests.get("http://10.30.1.2:5000/v3/users/" + new_server_user_ids[item_index], headers=headers)
                                results_json = r.json()
                                user = results_json["user"]
                                print "    - instanca: " + new_server_names[item_index] + " od korisnika: " + user["name"]
                        server_ids = new_server_ids
                        server_names = new_server_names
                        server_user_ids = new_server_user_ids
                    time.sleep(3)
        except KeyboardInterrupt:
            pass
    elif selected_menu_option == '4':
        print_statistics()
