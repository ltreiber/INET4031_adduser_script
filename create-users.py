#!/usr/bin/python3
import os
import re
import sys

def main():
	for line in sys.stdin:
		#This checks for the # symbol in the text which means we should ignore it
		match = (re.match("#", line, re.IGNORECASE))
		#This line splits the the text recieved when it hits :
		fields = line.strip().split(':')
		#If we see a # or if there are too many fields, this jumps us to the next line in the file.
		if(match or len(fields) != 5):
			continue
		username = fields[0]
		password = fields[1]
		gecos = "%s %s,,," % (fields[3],fields[2])
		#This line cuts/splits the fourth field if there is a comma. This allows us to put a user in multiple groups
		groups = fields[4].split(',')
		print("==> Creating accound for %s..." % (username))
		cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
		print(cmd)
		os.system(cmd)
		print("==> Setting the password for %s..." % (username))
		cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password,username)
		print(cmd)
		os.system(cmd)
		#This for loop is iterating through the different groups that the user are assigned to.
		#If there is more than one, we need to run the command multiple times with the differen group
		for group in groups:
			if group != '-':
				print("==> Assigning %s to the %s group..." % (username,group))
				cmd = "/usr/sbin/adduser %s %s" % (username, group)
				print(cmd)
				os.system(cmd)
if __name__ == '__main__':
	main()
