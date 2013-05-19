#!/usr/bin/python 
import re
import fileinput

file_name= '/var/www/UE-environment/updatengine-server/updatengine/settings.py'
url = raw_input('Enter IP address or DNS name of your server:')
newurl = r"PROJECT_URL = 'http://" + url + ":1979'"
for line in fileinput.input(file_name, inplace=1):
	print re.sub(r"PROJECT_URL = 'http\://.*\:1979'", newurl, line)
