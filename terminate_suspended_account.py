#! /usr/bin/python
# Binh Pham - bphamt@gmail.com
# Lists all the suspended account of a cPanel
# Gives the option to terminate all the suspended accounts

# Used for linux command-line manipulation
import os

# Path to suspended user in cPanel
path = "/var/cpanel/suspended/"

# Add user to a list called 'dir_list'
dir_list = os.listdir(path)


def terminate_accounts():
    """
    Terminates cPanel account if user agrees
    @param dir_list: list of suspended users
    """
    for i in dir_list:
        cmd = "/usr/local/cpanel/scripts/removeacct " + str(i) + " --force"
        os.system(cmd)

    print("\n\nThe following accounts have been terminated:")
    for x in dir_list:
        print(" - " + str(x))


if not dir_list:
    print("No suspended account on server")
else:
    print("List of suspended accounts:")
    for i in dir_list:
        print(" - " + str(i))
    input_variable = raw_input("\nDo you want to terminate the above suspended cPanel accounts (Y/N)? ")
    if str(input_variable) == 'Y' or str(input_variable) == 'y':
        terminate_accounts()
    else:
        quit()
