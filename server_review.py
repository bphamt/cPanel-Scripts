#! /usr/bin/python
# Binh Pham - bphamt@gmail.com

import os
import re


def get_os_version():
    os_version = re.findall(r'"([^"]*)"', os.popen('cat /etc/os-release | grep -w "PRETTY_NAME="').read())[0]
    print("\nServer OS Version: ")
    print(" - " + str(os_version))


def get_disk_usage():
    disk_usage = (os.popen('df -h | grep -w "/"').read()).split()
    print("\nDisk Usage:")
    print(" - Disk Size: " + str((disk_usage)[1]))
    print(" - Disk Used: " + str((disk_usage)[2]))
    print(" - Disk Available: " + str((disk_usage)[3]))

    index = 0
    found_index = 0
    for item in disk_usage:
        if "%" in item:
            found_index = index
        index += 1
    print(" - Disk Used Percentage: " + str((disk_usage)[found_index]))


def get_uptime():
    uptime = (os.popen('uptime').read()).split()
    print("Uptime:")
    print(" - " + str(uptime[2]) + " " + str(uptime[3]).rstrip(','))


def get_cpanel_version():
    cpanel_version = (os.popen('/usr/local/cpanel/cpanel -V').read())
    print("\ncPanel Version:")
    print(" - " + str(cpanel_version))


def get_kernel_version():
    kernel_version = (os.popen('uname -r').read())
    print("Kernel Version:")
    print(" - " + str(kernel_version))


def get_inode_usage():
    inode_usage = (os.popen('df -i | grep -w "/"').read()).split()
    index = 0
    found_index = 0
    for item in inode_usage:
        if "%" in item:
            found_index = index
        index += 1
    print("\nInode Usage:")
    print(" - " + str(inode_usage[found_index]))


def get_mysql_version():
    mysql_version = (os.popen('mysql --version').read()).split()
    print("\nMySQL Version:")
    print(" - " + str(mysql_version[4]).rstrip(','))


get_cpanel_version()
get_kernel_version()
get_uptime()
get_disk_usage()
get_inode_usage()
get_mysql_version()