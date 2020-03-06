#!/bin/python3.6
import socket, pwd, grp, os, csv

devinfo = {}
userlist = []
grouplist = []

for p in pwd.getpwall():
    userlist.append(p[0])

devinfo["hostname"] = {socket.getfqdn()}
devinfo["IPv4 Private"] = {socket.gethostbyname(socket.gethostname())}
devinfo["Users"] = [userlist]
if os.path.isfile("/bin/ansible"):
    devinfo["Ansible"] = ["Present"]

csv_file = "output.csv"

with open(csv_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    for key, value in devinfo.items():
        writer.writerow([key, value])


# print(list(devinfo.items()))
# print(devinfo['Users'])
