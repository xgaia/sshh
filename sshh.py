import argparse
import os
import subprocess
import sys
import yaml

import pathlib

def yes_no_question(question=None, default="y"):

    possible_answers = "[Y/n]" if default == "y" else "[y/N]"
    if question:
        answer = input("{} {} ".format(question, possible_answers))
    else:
        answer = input("{} ".format(possible_answers))

    if not answer:
        answer = default

    if answer.lower() in ["y", "yes", "o", "oui"]:
        return True
    return False

def pprint_header():
    print(
        "Name           Group                    ssh                               "
        " Port"
    )
    print(
        "-------------------------------------------------------------------------------"
    )


def pprint_server(name, group, user, address, port):
    full = user + "@" + address
    space_1 = " " * (15 - len(name))
    space_2 = " " * (25 - len(group))
    space_3 = " " * (35 - len(full))
    space_4 = " " * (20 - len(address))

    print(name + space_1 + group + space_2 + user + "@" + address + space_3 + str(port))
    # print("{} ({}): {}@{}:{}".format(name, group, user, address, port))


home = os.path.expanduser("~")

parser = argparse.ArgumentParser(description='Easy manage your ssh servers')
parser.add_argument(
    '-f',
    '--file',
    help='Path to the yaml servers file',
    default='{}/.config/sshh/servers.yaml'.format(home),
)

subparsers = parser.add_subparsers(dest='subcommand')

# List
parser_list = subparsers.add_parser('list')
parser_list.add_argument('group', help='List server of group', nargs="?")

# Groups
parser_list = subparsers.add_parser('groups')

# Connect
parser_connect = subparsers.add_parser('ssh')
parser_connect.add_argument('--user', help='Connect with another user')
parser_connect.add_argument('server', help='The server to connect')

# Add
parser_add = subparsers.add_parser('add')
parser_add.add_argument('server', help='The server to add (user@host:port)')
parser_add.add_argument('name', help='The server\'s name to add')
parser_add.add_argument('-g', '--group', help='Server group', required=True)

# Add
parser_add = subparsers.add_parser('remove')
parser_add.add_argument('server', help='The server name to remove')
parser_add.add_argument('-f', '--force', help='Force remove', action=argparse.BooleanOptionalAction)

# parser.add_argument('--feature', action=argparse.BooleanOptionalAction)

# Edit
parser_edit = subparsers.add_parser('edit')

args = parser.parse_args()

# init config file
if not os.path.isfile(args.file):
    path = pathlib.Path(os.path.dirname(args.file))
    os.makedirs(os.path.dirname(args.file), exist_ok=True)
    with open(args.file, "w+") as f:
        f.write("servers:\n")

a_yaml_file = open(args.file)
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
servers = parsed_yaml_file["servers"]

# Display error message if config file is empty
if not servers:
    if args.subcommand != "add":
        print("Add a server first")
        parser_add.print_help()
        sys.exit(1)

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
    # FIXME: sort once
    sorted_list_tmp = sorted(servers, key=lambda k: k['name'])
    sorted_list = sorted(sorted_list_tmp, key=lambda k: k['group'])
    pprint_header()
    for server in sorted_list:
        if args.group:
            if len(args.group.split("/")) == 1:
                requested_group = args.group
                server_groups = server["group"].split("/")
                if requested_group in server_groups:
                    pprint_server(
                        server["name"],
                        server["group"],
                        server["user"],
                        server["address"],
                        server["port"],
                    )

            else:
                requested_groups = args.group.split("/")
                server_groups = server["group"].split("/")
                lrg = len(requested_groups)
                if requested_groups == server_groups[0:lrg]:
                    pprint_server(
                        server["name"],
                        server["group"],
                        server["user"],
                        server["address"],
                        server["port"],
                    )
        else:
            pprint_server(
                server["name"],
                server["group"],
                server["user"],
                server["address"],
                server["port"],
            )

# Connect to server
if args.subcommand == 'ssh':
    for server in servers:
        if server["name"] == args.server:
            user = args.user if args.user else server["user"]
            cmd = "ssh -p {} {}@{}".format(server["port"], user, server["address"])
            # print(cmd)
            retcode = subprocess.call(cmd, shell=True)

# Add a server
if args.subcommand == "add":
    # create object
    obj = {
        "name": args.name,
        "user": args.server.split("@")[0],
        "address": args.server.split("@")[1].split(":")[0],
        "port": args.server.split("@")[1].split(":")[1]
        if len(args.server.split("@")[1].split(":")) == 2
        else 22,
        "group": args.group,
    }
    # Write it to yaml file
    if parsed_yaml_file["servers"] is None:
        parsed_yaml_file["servers"] = []
    parsed_yaml_file["servers"].append(obj)
    with open(args.file, "w+") as file:
        yaml.dump(parsed_yaml_file, file)

# remove a server
if args.subcommand == "remove":

    if not args.force:
        # print("Remove {}? [Y/n]".format(args.server))
        if not yes_no_question("Remove {}?".format(args.server)):
            exit(0)

    new_servers = []
    for server in servers:
        if server["name"] != args.server:
            new_servers.append(server)
        else:
            print("{} removed !".format(args.server))

    yaml_dict = {"servers": new_servers}

    with open(args.file, "w+") as file:
        yaml.dump(yaml_dict, file)


# Edit servers
if args.subcommand == "edit":
    editor = os.environ.get('EDITOR')
    cmd = "{} {}".format(editor, args.file)
    retcode = subprocess.call(cmd, shell=True)
