#! /opt/alt/python27/bin/python2.7

import commands
import csv

# Open file for reading
fileObject = open("/etc/trueuserowners", "r")

# Reseller list
resellers = {}

shared_accounts = []
shared_accounts_username = []
shared_accounts_domain = []
shared_accounts_emailaddress = []

reseller_accounts = []
reseller_accounts_username = []
reseller_accounts_domain = []
reseller_accounts_emailaddress = []
reseller_accounts_plan = []

dns_accounts = []

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

def grab_user_info(owner):
    username = owner
    domain_cmd = str(commands.getstatusoutput("uapi --user=" + str(owner) + " Variables get_user_information | grep 'domain: '"))
    domain = domain_cmd.split()[3].split("'")[0]
    email_cmd = str(commands.getstatusoutput("uapi --user=" + str(username) + " Variables get_user_information | grep \"contact_email: \""))
    emailaddress = email_cmd.split()[3].split("'")[0]
    plan_cmd = str(commands.getstatusoutput("uapi --user=" + str(username) + " Variables get_user_information | grep \"plan: \""))
    plan = plan_cmd.split()[3].split("'")[0]

    return username, domain, emailaddress, plan

# Check if account is a reseller. Reseller > 1 cPanel account
def check_if_reseller(owner, child, index):
    global shared_accounts_domain
    global shared_accounts_emailaddress
    global reseller_accounts_domain
    global reseller_accounts_emailaddress

    if owner == "root":
        for y in range(index + 1):
            if 'DNS' in str((grab_user_info(child[y])[3])):
                dns_accounts.append(child[y])
            else:
                shared_accounts.append(child[y])
                shared_accounts_domain.append(grab_user_info(child[y])[1])
                shared_accounts_emailaddress.append(grab_user_info(child[y])[2])
    elif len(child) < 2:
        if 'DNS' in str(grab_user_info(owner)[3]):
            dns_accounts.append(owner)
        else:
            shared_accounts.append(owner)
            shared_accounts_domain.append(grab_user_info(owner)[1])
            shared_accounts_emailaddress.append(grab_user_info(owner)[2])
    else:
        reseller_accounts.append(owner)
        reseller_accounts_domain.append(grab_user_info(owner)[1])
        reseller_accounts_emailaddress.append(grab_user_info(owner)[2])


for key in resellers:
    check_if_reseller(key, resellers[key], len(resellers[key]) - 1)

print("shared_accounts = " + str(shared_accounts))
print("shared_accounts_domain = " + str(shared_accounts_domain))
print("shared_accounts_emailaddress = " + str(shared_accounts_emailaddress))

print("")

print("reseller_accounts = " + str(reseller_accounts))
print("reseller_accounts_domain = " + str(reseller_accounts_domain))
print("reseller_accounts_emailaddress = " + str(reseller_accounts_emailaddress))

print("")

print("dns_account = " + str(dns_accounts))
