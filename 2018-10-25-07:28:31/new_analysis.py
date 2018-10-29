import os
from os import listdir
from os.path import isfile, join
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
	print_results = True

	filenames = get_filenames()
	titles = get_titles(filenames)

	df = create_dataframe(filenames, titles, print_results)

	titles = list(df)
	units = ['Force (g-9.8m/s^2)', 'Force (g-9.8m/s^2)', 'Force (g-9.8m/s^2)', 'Blood Volume per Pulse (mL)', 'EDA Units', 'Heart Rate (bpm', 'Temperature (degrees C']
	sample_rates = [32, 32, 32, 64, 4, 64, 4]

	plot_data(df, titles, units, print_results)

def plot_data(df, titles, units, sample_rates, print_results=False):
	df = df.reset_index()
	
	#fig, axes = plt.subplots(nrows=len(list(df)[1:]), ncols=1)
	plt.figure(figsize=(19,12))

	for i in range(1,len(list(df)[1:])+1):
		plt.subplot(len(list(df)[1:]),1,i)
		plt.scatter(
			x=df['index'],
			y=df.iloc[:,i],
			s=0.1
		)
		plt.title(titles[i-1])
		plt.xlabel('Sample Number n')
		#plt.ylabel(units[i-1])

	plt.suptitle('Scott: A Growing Boy and His Growing Signals')
	plt.subplots_adjust(hspace=2)

	plt.show()

def create_dataframe(filenames, titles, print_results=False):
	appended_data = []

	print filenames

	for f in range(0,len(filenames)):
		if os.stat(filenames[f]).st_size is not 0:
			data = pd.read_csv(
				filenames[f],
				error_bad_lines=False
			)
			appended_data.append(data)

	df = pd.concat(appended_data, axis=1)
	return df

def get_filenames():
	filenames = [f for f in listdir('.') if isfile(join('.', f))]

	if 'analysis.py' in filenames and 'info.txt' in filenames:
		filenames.remove('analysis.py')
		filenames.remove('info.txt')

	return filenames

def get_titles(filenames):
	files = [i.strip('.csv') for i in filenames]

	if 'new_analysis.py' in files and 'info.txt' in files:
		files.remove('new_analysis.py')
		files.remove('info.txt')
		filenames.remove('new_analysis.py')
		filenames.remove('info.txt')

	return files

if __name__ == '__main__':
	main()