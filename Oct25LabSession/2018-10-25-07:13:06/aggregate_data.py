import os
import pytz
import time
import json
from datetime import datetime
import shutil
import distutils
from distutils import dir_util
from os import listdir
from os.path import isfile, join
import subprocess
import numpy as npd
import pandas as pd
import matplotlib.pyplot as plt

def main():
	user_choice = raw_input('Would you like to \n1 - Analyze one user session\n2 - Analyze all user sessions(Inadvisable; Results in many figures)\n3 - Analyze user sessions in a date range?\n\n=> ')
	print "\n"

	if user_choice == '1':
		analysis_session = raw_input('Please provide the folder name for the session that you would like to analyze: ')
		single_session(analysis_session, 0, 1)
		plt.show()
	elif user_choice == '2':
		all_sessions()
		#plt.show()
	elif user_choice == '3': 
		date_range()
		#plt.show()

def single_session(analysis_session, iteration, total):
	
	filenames = get_filenames(analysis_session)
	titles = get_titles(filenames)

	df = create_dataframe(filenames, titles)

	units = ['Force (g-9.8m/s^2)', 'Force (g-9.8m/s^2)', 'Force (g-9.8m/s^2)', 'Blood Volume per Pulse (mL)', 'EDA Units', 'Heart Rate (bpm', 'Temperature (degrees C']
	sample_rates = [32, 32, 32, 64, 4, 64, 4]

	json_list = get_json(analysis_session)
	information_report(df, iteration, json_list)

	plt = plot_data(df, titles, units, sample_rates, iteration, analysis_session, total)

def all_sessions():

	dir_names = next(os.walk('.'))[1]

	for dir_name in range(0,len(dir_names)-1):
		if '201' not in dir_names[dir_name]:
			dir_names.remove(dir_names[dir_name])

	for i in range(0,len(dir_names)):
		print "\nAnalyzing session starting on: {}".format(dir_names[i])
		single_session(dir_names[i],i,len(dir_names))

def date_range():

	dir_names = next(os.walk('.'))[1]

	for dir_name in range(0,len(dir_names)-1):
		if '201' not in dir_names[dir_name]:
			dir_names.remove(dir_names[dir_name])

	print "Possible sessions for range: \n"
	for i in range(0, len(dir_names)):
		print dir_names[i]
	print "\n"

	date_range = raw_input('Enter the range of dates (to the minute and second) between which you would like to retrieve data separated by a space\n\nFormat = 2018-09-20-08:03:06 2018-09-25-08:04:24\n\n=> ')

	date_range = date_range.split(' ')

	start_date = format_to_unix(date_range[0])
	end_date = format_to_unix(date_range[1])

	filtered_sessions = [dir_names[i] for i in range(0,len(dir_names)) if format_to_unix(dir_names[i]) >= start_date]
	filtered_sessions = [dir_names[i] for i in range(0,len(filtered_sessions)) if format_to_unix(dir_names[i]) <= end_date]

	print "\nCreating report from the {} sessions supplied in your indicated range: \n".format(len(filtered_sessions))
	for i in range(0,len(filtered_sessions)):
		print filtered_sessions[i], "\n"

	for i in range(0,len(filtered_sessions)):
		single_session(filtered_sessions[i],i,len(filtered_sessions))

	create_dataset = raw_input('Would you like to create a data subset from the date range presented?: (y or n)\n=> ')

	if create_dataset == 'y':
		print("\n")
		create_set(filtered_sessions)
	else:
		return

def information_report(df, iteration, json_list):

	# Duration of session
	# Max value for each health metric
	# Start date of session 
	# End date of session

	start_date = datetime.utcfromtimestamp(int(json_list['start_time'])).strftime('%Y-%m-%d-%H:%M:%S')
	duration = float(json_list['duration']) / 3600.0

	print "\nThe duration of session {} was {:.2f} hours".format(iteration+1, duration)

def get_json(session_name):

	data = open(os.getcwd()+'/'+session_name+'/'+'json_info.json', 'r').read()
	json_list = json.loads(data)

	return json_list

def create_set(sessions):

	dataset_name = raw_input('What would you like to name your dataset: ')
	
	dataset_dir = os.path.join(os.getcwd(), dataset_name)
	os.makedirs(dataset_dir)

	for i in range(0,len(sessions)):
		session_dir = os.path.join(os.getcwd(), sessions[i])
		#shutil.copytree(session_dir, dataset_dir+sessions[i])
		distutils.dir_util.copy_tree(session_dir, dataset_dir+'/'+sessions[i])

	copyfile('new_analysis.py', dataset_dir+'/new_analysis.py')
	copyfile('aggregate_data.py', dataset_dir+'/aggregate_data.py')
	copyfile('mike_script.m', dataset_dir+'/mike_script.m')
	copyfile('bvp_analysis.m', my_dir+'/bvp_analysis.m')

def format_to_unix(date):

	date_list = date.split('-')
	date_list[3] = date_list[3].split(':')

	unix_time = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(date_list[3][0]), int(date_list[1])).strftime('%s')

	return unix_time

def plot_data(df, titles, units, sample_rates, iteration, analysis_session, total):
	df = df.reset_index()

	list(df)[1] = 'Accelerometer' + list(df)[1]
	list(df)[2] = 'Accelerometer' + list(df)[2]
	list(df)[3] = 'Accelerometer' + list(df)[3]
	
	plt.figure(iteration, figsize=(10,10))

	for i in range(1,len(list(df)[1:])+1):
		plt.subplot(len(list(df)[1:]),1,i)
		plt.scatter(
			x=df['index'],
			y=df.iloc[:,i],
			s=0.1
		)
		plt.title(list(df)[i])
		plt.xlabel('Sample Number n')
		#plt.ylabel(units[i-1])

	plt.suptitle('Session Occuring at: '+analysis_session)
	plt.subplots_adjust(hspace=2)

	numer = float(iteration+1)
	denom = float(total)

	print 'Plotting Sequence {0:.{1}f}% Complete'.format((numer / denom) * 100, 2)

def create_dataframe(filenames, titles):
	appended_data = []

	for f in range(0,len(filenames)):
		if os.stat(filenames[f]).st_size is not 0:
			data = pd.read_csv(
				filenames[f]
			)
			appended_data.append(data)

	df = pd.concat(appended_data, axis=1)
	return df

def get_filenames(analysis_session):
	filenames = [analysis_session + '/' + f for f in listdir(analysis_session + '/') if isfile(join(analysis_session, f))]

	if analysis_session+'/new_analysis.py' in filenames or analysis_session+'/info.txt' in filenames:
		filenames.remove(analysis_session + '/new_analysis.py')
		filenames.remove(analysis_session + '/info.txt')
		filenames.remove(analysis_session + '/json_info.json')

	return filenames

def get_titles(filenames):
	files = [i.strip('.csv') for i in filenames]
	files = [i.split('/',1)[1] for i in files]

	if 'new_analysis.py' in files and 'info.txt' in files:
		files.remove('new_analysis.py')
		files.remove('info.txt')
		filenames.remove('new_analysis.py')
		filenames.remove('info.txt')

	return files

if __name__ == '__main__':
	main()