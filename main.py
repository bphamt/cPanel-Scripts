#! /usr/bin/python
# Binh Pham - bphamt@gmail.com
# Lists all the child account of a cPanel owner
# Gives the total limit of all the child account under the owner account (also including the owner)
# Gives the total disk space usage of all the child account under the cPanel owner account (including the owner)

import commands

# Open file for reading
fileObject = open("/etc/trueuserowners", "r")

# Reseller dict
resellers = {}

for line in fileObject:
    cpanel_owner = (line.split()[0])[:-1]
    reseller_owner = (line.split()[1])
    cpanel_array = []
    if reseller_owner in resellers:
        resellers[reseller_owner].append(cpanel_owner)
    else:
        cpanel_array.append(cpanel_owner)
        resellers[reseller_owner] = cpanel_array


def get_total_usage(owner):
    total_disk_usage = 0
    total_limit = 0
    for x in resellers[owner]:
        mb_value = str(commands.getstatusoutput("uapi --user=" + str(x) + " Quota get_quota_info|grep -E 'megabytes_used: '"))
        usage = (((mb_value.split()[3]).replace('"', '')).replace("'", "")).strip(")")
        total_disk_usage += float(usage)
        limit_value = str(commands.getstatusoutput("uapi --user=" + str(x) + " Quota get_quota_info | grep -w 'megabyte_limit:'"))
        limit_usage = (((limit_value.split()[3]).replace('"', '')).replace("'", "")).strip(")")
        total_limit += float(limit_usage)

    if str(total_limit) == "0.0":
        print("Total limit of all the cPanel account: Unlimited")
    else:
        print("Total limit of all the cPanel account: " + str(total_limit) + "MB")
    print("Total usage of all the cPanel account of the reseller: " + str(total_disk_usage) + "MB")

for key in resellers:
    print("Reseller Owner: " + key)
    print(" - Child account: " + str(resellers[key]))
    get_total_usage(key)
    print("\n")