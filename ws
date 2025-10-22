#!/bin/python3
import argparse

from config import load_token, save_token, load_user
from lister import list_cloudspaces, list_vms
from dataclasses import dataclass

@dataclass
class User:
    jwt = load_token()
    vco, customer = load_user()

if __name__=="__main__":
   
    user = User()

    parser = argparse.ArgumentParser(prog="ws", description="Manage whitesky resources")
    subparsers = parser.add_subparsers(dest="command")
    
    # Token
    token_parser = subparsers.add_parser("token", help="Set JWT token")
    token_parser.add_argument("token", default=None, help="JWT token")

    # List
    list_parser = subparsers.add_parser("list", help="list resources")
    list_subparsers = list_parser.add_subparsers(dest="list_command")

    # Describe
    describe_parser = subparsers.add_parser("describe", help="describe resource")
    describe_subparsers = describe_parser.add_subparsers(dest="describe_command")

    # List cloudspaces
    list_subparsers.add_parser("cloudspaces", help="list cloudspaces")

    # List vms
    vms_parser = list_subparsers.add_parser("vms", help="list virtual machines")
    vms_parser.add_argument("cloudspace", default=None, help="cloudspace")

    # Describe cloudspace



    args = parser.parse_args()

    if args.command == "list":
        if args.list_command == "cloudspaces":
            list_cloudspaces(user)
        elif args.list_command == "vms":
            list_vms(user, args.cloudspace)
        else:
            list_parser.print_help()
    
    elif args.command == "describe":
        if args.list_command == "cloudspace":
            describe_cloudspace(user, args.cloudspace)


    elif args.command == "token":
        save_token(args.token)
    
    else:
        parser.print_help()   
