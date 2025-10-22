#!/bin/python3
import argparse

from config import load_token, save_token, load_user
from lister import list_cloudspaces, list_vms
from dataclasses import dataclass

@dataclass
class User:
    jwt = load_token()
    vco, customer = load_user()

def create_parser():

    parser = argparse.ArgumentParser(prog="ws", description="Manage whitesky resources")
    subparsers = parser.add_subparsers(dest="command")

    # === TOKEN ===
    token_parser = subparsers.add_parser("token", help="Set JWT token")
    token_parser.add_argument("token", help="JWT token")
    token_parser.set_defaults(func=save_token)

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
    user = User()

    parser = create_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(user, args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
