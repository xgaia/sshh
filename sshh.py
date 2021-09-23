import argparse
import os
import subprocess
import yaml

import pathlib

def pprint_header():
    print("Name           Group                    ssh                                Port")
    print("-------------------------------------------------------------------------------")

def pprint_server(name, group, user, address, port):
    full =  user + "@" + address
    space_1 = " " * (15 - len(name))
    space_2 = " " * (25 - len(group))
    space_3 = " " * (35 - len(full))
    space_4 = " " * (20 - len(address))

    print(name + space_1 + group + space_2 + user + "@" + address + space_3 + str(port))
    # print("{} ({}): {}@{}:{}".format(name, group, user, address, port))

home = os.path.expanduser("~")

parser = argparse.ArgumentParser(description='Easy manage your ssh servers')
parser.add_argument('-f', '--file', help='Path to the yaml servers file', default='{}/.config/sshh/servers.yaml'.format(home))

subparsers = parser.add_subparsers(dest='subcommand')

# List
parser_list = subparsers.add_parser('list')
parser_list.add_argument('-g', '--group', help='List server of group')

# Groups
parser_list = subparsers.add_parser('groups')

# Connect
parser_connect = subparsers.add_parser('ssh')
parser_connect.add_argument('--root', action='store_true', help='Connect with root user')
parser_connect.add_argument('server', help='The server to connect')
args = parser.parse_args()

# init config file
if not os.path.isfile(args.file):
    path = pathlib.Path(os.path.dirname(args.file))
    os.makedirs(os.path.dirname(args.file), exist_ok = True)
    with open(args.file, "w+") as f:
        f.write("servers:\n")

a_yaml_file = open(args.file)
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
servers = parsed_yaml_file["servers"]

# Display error message if config file is empty
if not servers:
    print("Please fill {} with somme entries".format(args.file))
    exit(1)

# Display help
if not args.subcommand:
    parser.print_help()

# Display groups
if args.subcommand == 'groups':
    groups = set([server["group"] for server in servers])
    for group in groups:
        print(group)

# List servers
if args.subcommand == 'list':
    pprint_header()
    for server in servers:
        if args.group:
            requested_groups = args.group.split("/")
            server_groups = server["group"].split("/")
            lrg = len(requested_groups)
            if requested_groups == server_groups[0:lrg]:
                pprint_server(server["name"], server["group"], server["user"], server["address"], server["port"])
        else:
            pprint_server(server["name"], server["group"], server["user"], server["address"], server["port"])

# Connect to server
if args.subcommand == 'ssh':
    for server in servers:
        if server["name"] == args.server:
            user = "root" if args.root else server["user"]
            cmd = "ssh -p {} {}@{}".format(server["port"], user, server["address"])
            # print(cmd)
            retcode = subprocess.call(cmd,shell=True)
