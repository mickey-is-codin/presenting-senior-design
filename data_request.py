import os
import json
import getpass
import subprocess
from datetime import datetime
import requests
import zipfile
import StringIO
from shutil import copyfile
from bs4 import BeautifulSoup
from urllib2 import urlopen
from requests.auth import HTTPBasicAuth
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def main():
	
	print_results = False
	folder_date_style = 'Datetime'
	folder_nums = int(subprocess.check_output('find ./* -maxdepth 0 -type d | wc -l', shell=True)) - 1

	base_url = 'https://www.empatica.com/connect/'

	s = start_session(base_url, True)
	parsed = get_json_sessions(s, base_url, False)
	
	num_sessions = len(parsed)
	discrep = num_sessions - folder_nums - 1

	id_list = [parsed[i]['id'] for i in range(0,len(parsed))]
	date_list_utc = [parsed[i]['start_time'] for i in range(0,len(parsed))]
	date_list_datetime = [datetime.utcfromtimestamp(int(parsed[i]['start_time'])).strftime('%Y-%m-%d-%H:%M:%S') for i in range(0,len(parsed))]

	download_data(s, parsed, id_list, base_url+'download.php', discrep, date_list_datetime)

def download_data(s, parsed, id_list, downloads_url, discrep, date_list_datetime):

	for i in range(0,len(id_list[-discrep:])):
		if discrep > 0:
			print "\nFound a new session (",id_list[i],")!"
			print "Downloading ..."
			download_full_url = downloads_url + '?id=' + id_list[i]	
			download = s.get(download_full_url)

			z = zipfile.ZipFile(StringIO.StringIO(download.content))

			timestamp = date_list_datetime[i]
			my_dir = os.path.join(os.getcwd(), timestamp)

			if not os.path.isdir(my_dir):
				os.makedirs(my_dir)
			z.extractall(my_dir)

			with open(my_dir+'/json_info.json', 'w') as outfile:
				json.dump(parsed[i], outfile)

			copyfile('new_analysis.py', my_dir+'/new_analysis.py')
			copyfile('mike_script.m', my_dir+'/mike_script.m')
			copyfile('bvp_analysis.m', my_dir+'/bvp_analysis.m')
			copyfile('aggregate_data.py', my_dir+'/aggregate_data.py')
			print "Download complete to folder",timestamp,"\n"	

	if discrep > 0:
		subprocess.call('bash addHeaders.sh', shell=True)

	if discrep == 0:
		print "No new sessions found to download, you're up to date!"	

def get_json_sessions(s, base_url, print_results=False):
	sessions_response_html = response = s.get(base_url+'connect.php/users/19466/sessions?from=0&to=999999999999')
	sessions_json = sessions_response_html.text
	parsed = json.loads(sessions_json)

	sessions_list = json.dumps(parsed, indent=4, sort_keys=True)

	if print_results:
		print "Dictionary of Found Watch Sessions: \n"
		print sessions_list

	return parsed	

def start_session(base_url, print_results=False):
	
	s = requests.session()
	data = {'username':raw_input('\nWhat is your email: '), 'password':getpass.getpass('What is your password: ')}
	login_response = s.post(base_url+'authenticate.php', data)

	return s

if __name__ == '__main__':
	main()