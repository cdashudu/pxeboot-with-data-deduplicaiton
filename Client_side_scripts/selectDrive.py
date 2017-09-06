import sys
import os
import getpass
from subprocess import call

users={"yvora":"yvora", "cddashud":"cddashud", "vwfreeh":"vwfreeh"}

status = ""

def displayMenu():
    status = raw_input("Are you a registered user? y/n? Press q to quit: ")  
    if status == "y":
        oldUser()
    elif status == "n":
        print("Contact admin to create a get your persistent storage")
    elif status == "q":
    	print("Exiting.....!")
    	sys.exit(0)


def oldUser():
    login = raw_input("Enter login name: ")
    passw = getpass.getpass('Password:')

   
	# check if user exists and login matches password
    if login in users and users[login] == passw: 
        print ("\nLogin successful!\n")
        print("Mounting your persistent storage at /mnt \n")
        print("Use cd /mnt to go to your remote storage")
	os.system("ssh -t -o \"StrictHostKeyChecking no\" -i /home/chandu/scripts/id_rsa yash@192.168.0.26 /home/yash/scripts/reconstruct.sh {0}".format(login))
        os.system("mount -t nfs -o proto=tcp,port=2049 192.168.0.26:/pxeusers/'{0}' /mnt".format(login))
        sys.exit(0)
    else:
        print "\nUser doesn't exist or wrong password!\n"

while True:            
    displayMenu()


'''
mount -t nfs -o proto=tcp,port=2049 192.168.0.26:/login /mnt
'''
