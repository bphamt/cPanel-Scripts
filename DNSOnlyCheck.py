#! /usr/bin/python

import commands
import subprocess

# Open file for reading
fileObject = open("/etc/trueuserowners", "r")

# Reseller dict
resellers = {}

# Convert reseller & child info into the reseller dict
for line in fileObject:
    cpanel_owner = (line.split()[0])[:-1]
    reseller_owner = (line.split()[1])
    cpanel_array = []
    if reseller_owner in resellers:
        resellers[reseller_owner].append(cpanel_owner)
    else:
        cpanel_array.append(cpanel_owner)
        resellers[reseller_owner] = cpanel_array

def get_disk_usage(username):
    mb_value = str(
        commands.getstatusoutput("uapi --user=" + str(username) + " Quota get_quota_info|grep -E 'megabytes_used: '"))
    usage = (((mb_value.split()[3]).replace('"', '')).replace("'", "")).strip(")")
    return usage

def get_cpanel_info(username):
    # Get User Plan
    mb_value = str(
        commands.getstatusoutput("uapi --user=" + str(username) + " Variables get_user_information | grep 'plan'"))
    usage = (mb_value.split()[3]).split("'")[0]

    #Get User Email
    user_value = str(
        commands.getstatusoutput("uapi --user=" + str(username) + " Variables get_user_information | grep \"contact_email: \""))
    email = (user_value).split()[3].split("'")[0]

    if usage.find('DNS') > 1:
        print(username + " - " + str(usage) + " - " + str(get_disk_usage(username)) + "MB - " + str(email))

hostname_cmd = 'cat /proc/sys/kernel/hostname'
hostname_result = subprocess.check_output(hostname_cmd, shell=True)
print(str(hostname_result.strip()))

for i in resellers.values():
    for j in range(len(i)):
        get_cpanel_info(i[j])
