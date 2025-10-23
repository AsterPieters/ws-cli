#!/bin/python3
import argparse

from config import Config, create_config, set_customer
from lister import list_cloudspaces, list_vms

def create_parser():

    parser = argparse.ArgumentParser(prog="ws", description="Manage whitesky resources")
    subparsers = parser.add_subparsers(dest="command")

    # === CONFIG ===
    config_parser = subparsers.add_parser("config", help="Manage config")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    set_token_parser = config_subparsers.add_parser("set_token", help="Set token")
    set_token_parser.add_argument("token", help="JWT token")
    set_token_parser.set_defaults(func=create_config)

    set_customer_parser = config_subparsers.add_parser("set_customer", help="Set customer")
    set_customer_parser.add_argument("customer", help="Customer name")
    set_customer_parser.set_defaults(func=set_customer)

    # === LIST ===
    list_parser = subparsers.add_parser("list", help="List resources")
    list_subparsers = list_parser.add_subparsers(dest="list_command")

    cloudspaces_parser = list_subparsers.add_parser("cloudspaces", help="List cloudspaces")
    cloudspaces_parser.set_defaults(func=list_cloudspaces)

    vms_parser = list_subparsers.add_parser("vms", help="List virtual machines")
    vms_parser.add_argument("cloudspace_id", help="Cloudspace name")
    vms_parser.set_defaults(func=list_vms)

    return parser

def main():

    parser = create_parser()
    args = parser.parse_args()

    if args.command == "config" and args.config_command == "set_token":
        create_config(args.token)
        return
    
    config = Config()

    if hasattr(args, "func"):
        args.func(config, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
