import datetime

from fetcher import get_cloudspaces, get_vms

def list_cloudspaces(user, wide=False):
    cs = get_cloudspaces(user.vco, user.customer, user.jwt)
    cloudspaces = cs['result']

    if wide: 
        print(f"{'NAME':<40} {'ID':<40} {'LOCATION':<20} {'STATUS':<12} {'MODE':<10} {'CREATED':<20}")
        for cs in cloudspaces:
            created = datetime.datetime.fromtimestamp(cs['creation_time'], tz=datetime.UTC).strftime('%Y-%m-%d')
            print(f"{cs['name']:<40} {cs['cloudspace_id']:<40} {cs['location']:<20} {cs['status']:<12} {cs['cloudspace_mode']:<10} {created:<20}")
    else:

        print(f"{'NAME':<60} {'ID':<30} {'LOCATION':<20} {'STATUS':<12}")
        for cs in cloudspaces:
            created = datetime.datetime.fromtimestamp(cs['creation_time'], tz=datetime.UTC).strftime('%Y-%m-%d')
            print(f"{cs['name']:<60} {cs['cloudspace_id']:<30} {cs['location']:<20} {cs['status']:<12}")




def list_vms(user, args):
    vms = get_vms(user.vco, user.customer, user.jwt, args.cloudspace_id)['result']
    print(f"{'NAME':<60} {'ID':<12} {'STATUS':<12} {'CREATED':<12}")
    if vms:
        for vm in vms: 
            created = datetime.datetime.fromtimestamp(vm['creation_time'], tz=datetime.UTC).strftime('%Y-%m-%d')
            print(f"{vm['name']:<60} {vm['vm_id']:<12} {vm['status']:<12} {created:<12}")
