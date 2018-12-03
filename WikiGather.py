########################
######            ######
#####  WIKI GATHER #####
######            ######
########################

# Gather wikipedia raw dataset and reformat them into .csv datasets

import sys
import csv
import statistics
import re
import os
import urllib.request
import gzip
from urllib.request import urlopen
import datetime

global labelflag
labelflag = 0

#Directory where the original DS´s are located
path = r''

#Directory where there CSV file will be written, csv name not included
csvdir = r''

#Enconding function to resolve encoding issues(may not be needed, depends on the workstation)
def enconding():
	if sys.stdout.encoding != 'cp850':
  		sys.stdout = codecs.getwriter('cp850')(sys.stdout.buffer, 'strict')
	if sys.stderr.encoding != 'cp850':
  		sys.stderr = codecs.getwriter('cp850')(sys.stderr.buffer, 'strict')

#generate list of the dataset names stored online
def get_URL():
	urls= []
	openUrls = [] 
	defURL = 'https://dumps.wikimedia.org/other/pagecounts-raw/2016/2016-0'
	for i in range(1):
		i +=1
		openUrls.append(defURL + str(i) +"/")
	for i in range(len(openUrls)):
		urlpath =urlopen(openUrls[i])
		string = urlpath.read().decode('utf-8')
		pattern = re.compile('<a href="(.+?)z"') 								
		filelist = pattern.findall(string)
		for line in filelist:
			urls.append(openUrls[i]+line+"z")
	return urls		

#create a Dataset with 9 columns from the original DS,contains all languages 
def create_ds():
	global dictNumID
	dictNumID = {}
	global dictWebsize
	dictWebsize = {}
	global dictRequest
	dictRequest = {}
	global ds 
	ds = []
	for incrementer in range(11):
		ds.append([])

	for filename in os.listdir(path):
		print(filename)
		fdata= open(path+filename,encoding="ascii", errors="surrogateescape")	
		for line in fdata:
			addToDS(line)
		calculateALL()
		writeCSV()
		clearData()
		fdata.close()

#create a Dataset with 8 columns from the original contains just the defined language for 24 hours	
def create_ds_lang(desiredLang):
	counter = 0
	global dictNumID
	dictNumID = {}
	global dictWebsize
	dictWebsize = {}
	global dictRequest
	dictRequest = {}

#increment or create new register for each new line read
def add_to_ds(n):
	global tmplist1
	global tmplist2
	global dictNumID
	global dictWebsize
	global dictRequest
	
	tmplist1 = []
	tmplist2 = []
	line = n
	splitedline =line.split()
	linesize = len(splitedline)
	languageRaw = splitedline[0]
	language = languageRaw.split('.',1)[0]    										#saves just the language identifier, i.e. "en","pt",etc...
	websize = float(re.sub('[^0-9]','', splitedline[linesize-1]))					#remove the non numeric values from the webpage size field			
	requestNum = float(re.sub('[^0-9]','',splitedline[linesize-2]))					#Create a number of request field in int type
	load = requestNum * websize														#Calculate the total load of the generate by the webpage
	if language in ds[0]:
		ind = ds[0].index(language)	 												#find the index of the existing language
		ds[1][ind] = ds[1][ind] + requestNum										#increment the sum of the request number
		ds[2][ind] = ds[2][ind] + websize											#increment the sum of the webpage size
		ds[9][ind] = ds[9][ind]+ load												#increment the sum of the load
		ds[10][ind] = ds[10][ind]  + 1												#increment the occurance counter
		tmplist1 = dictRequest.get(language)
		tmplist1.append(requestNum)
		tmplist2 = dictWebsize.get(language)
		tmplist2.append(websize)
		dictRequest[language] = tmplist1	
		dictWebsize[language] = tmplist2
	else:
		ds[0].append(language)
		ds[1].append(requestNum)												
		ds[2].append(websize)														
		ds[9].append(load)
		ds[10].append(1)
		dictRequest[language] =  []
		dictWebsize[language] =  []
		tmplist1 = dictRequest.get(language)
		tmplist1.append(requestNum)
		tmplist2 = dictWebsize.get(language)
		tmplist2.append(websize)
		numeID = ds[0].index(language)
		keyValue = dictNumID.get(language,"empty")	
		if keyValue == "empty":
			dictNumID[language] = numeID
				
#Write create DS out in CSV format		
def write_CSV():
	global labelflag
	global dictNumID
	
	with open(csvdir+'final.csv', 'a') as csvfile:
		label = ['language','sum_requests','sum_size','avg_requests','avg_size','Sample_stdev_requests','Sample_stdev_size','Population_stdev_requests','Population_stdev_size','total_Load','language_occur','Numeric_ID']
		writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=label)	
		if labelflag == 0:
			writer.writeheader()
			labelflag = 1
		for i in range(len(ds[0])):
			writer.writerow({'language':ds[0][i],'sum_requests':ds[1][i],'sum_size':ds[2][i],'avg_requests':ds[3][i],'avg_size':ds[4][i],'Sample_stdev_requests':ds[5][i],'Sample_stdev_size':ds[6][i],'Population_stdev_requests':ds[7][i],'Population_stdev_size':ds[8][i],'total_Load':ds[9][i],'language_occur':ds[10][i],'Numeric_ID':dictNumID.get(ds[0][i])})
		csvfile.close()

#calculates the average,standard deviaton for request and webpage size
def calculate_all():
	languageNumber = len(ds[0])	
	
	#Average Manual
	for x in range(languageNumber):
		languageName = ds[0][x]
		ds[3].insert(x,statistics.mean(dictRequest.get(languageName)))
		ds[4].insert(x,statistics.mean(dictWebsize.get(languageName)))
		
	#Sample Standard Deviation
	for y in range(languageNumber):
		languageName2 = ds[0][y]
		if len(dictRequest.get(languageName2)) <2:
			print("A")
			print(len(dictRequest.get(languageName2)))
			ds[5].insert(y,0)
			ds[6].insert(y,0)
		else:
			print(len(dictRequest.get(languageName2)))
			print(languageName2)
			ds[5].insert(y,statistics.stdev(dictRequest.get(languageName2)))
			ds[6].insert(y,statistics.stdev(dictWebsize.get(languageName2)))

	#Population Standard Deviation
	for w in range(languageNumber):
		languageName3 = ds[0][w]
		if len(dictRequest.get(languageName3)) <2:
			print("A")
			print(len(dictRequest.get(languageName3)))
			ds[7].insert(w,0)
			ds[8].insert(w,0)
		else:
			print(len(dictRequest.get(languageName3)))
			print(languageName3)
			ds[7].insert(w,statistics.pstdev(dictRequest.get(languageName3)))
			ds[8].insert(w,statistics.pstdev(dictWebsize.get(languageName3)))

#clear all variables to be reused on the next step
def clearData():
	global tmplist1
	global tmplist2
	global ds
	global dictRequest
	global dictWebsize

	del tmplist1[:]
	del tmplist2[:]
	del ds[:]
	dictRequest.clear()
	dictWebsize.clear()
	dictWebsize = {}
	dictRequest = {}
	ds = []
	for incrementer in range(11):
		ds.append([])

########################################################################## 4 hours functions ######################################################################################

#create a Dataset with 41 columns from the original DS(40 input att and 1 output att),contains just the defined language	
def create_ds_4h(desiredLang):
	counter = 0
	global dictNumID
	dictNumID = {}
	global dictWebsize
	dictWebsize = {}
	global dictRequest
	dictRequest = {}
	global ds 
	ds = []
	for incrementer in range(10):
		ds.append([])
	global finalDS
	finalDS = []
	tempurls = []
	urls = []

	tempurls = getURL()	#get all urls, used to download all files
	print(len(tempurls))
	urls = tempurls[:93]
	print(len(urls))
	start2 =  datetime.datetime.now() 
	for url in urls:
		start = datetime.datetime.now() 
		print("start download")
		file_name, headers = urllib.request.urlretrieve(url)
		print("start zip")
		with gzip.open(file_name, 'rb') as f:	
			print("unz")
			for line in f:
				if(len(line.decode('ascii',errors="surrogateescape"))<10):    #if the line that was read has not content jumps to the next line
					continue
				addToDS4h(line.decode('ascii',errors="surrogateescape"),desiredLang)
			finalDS.append([])
			if ds[0] == []:											
				finalDS[counter].append(0)
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
				finalDS[counter].append(0)	
			else:
				calculateALL4h(desiredLang)
				finalDS[counter].insert(0,ds[0][0])
				finalDS[counter].insert(1,ds[1][0])
				finalDS[counter].insert(2,ds[2][0])
				finalDS[counter].insert(3,ds[3][0])
				finalDS[counter].insert(4,ds[4][0])
				finalDS[counter].insert(5,ds[5][0])	
				finalDS[counter].insert(6,ds[6][0])
				finalDS[counter].insert(7,ds[7][0])
				finalDS[counter].insert(8,ds[8][0])		
				finalDS[counter].insert(9,ds[9][0])
			clearData()
			print(counter)
			counter += 1
		urllib.request.urlcleanup()
		print(datetime.datetime.now() - start)
	writeCSV4h()
	print(datetime.datetime.now() - start2)

#write csv with 41 columns
def write_CSV_4h():
	global labelflag
	global dictNumID
	global finalDS
	global labelflag

	with open(csvdir+'final4h1.csv', 'a') as csvfile:
		label = ['sum_requests1','sum_size1','avg_requests1','avg_size1','Sample_stdev_requests1','Sample_stdev_size1','Population_stdev_requests1','Population_stdev_size1','total_Load1','language_occur1','sum_requests2','sum_size2','avg_requests2','avg_size2','Sample_stdev_requests2','Sample_stdev_size2','Population_stdev_requests2','Population_stdev_size2','total_Load2','language_occur2','sum_requests3','sum_size3','avg_requests3','avg_size3','Sample_stdev_requests3','Sample_stdev_size3','Population_stdev_requests3','Population_stdev_size3','total_Load3','language_occur3','sum_requests4','sum_size4','avg_requests4','avg_size4','Sample_stdev_requests4','Sample_stdev_size4','Population_stdev_requests4','Population_stdev_size4','total_Load4','language_occur4','target_load']
		writer = csv.DictWriter(csvfile, lineterminator='\n', fieldnames=label)	
		print("write CSV")
		print(labelflag)
		if labelflag != 1:
			writer.writeheader()
			labelflag = 1
			print("enter")
		for i in range(len(finalDS)-4):
			print(len(finalDS))
			print(i+5)
			if i+5 < len(finalDS):
				target = str(finalDS[i+4][8])
			else:
				target = '?'
			print(target)
			writer.writerow({'sum_requests1':finalDS[i][0],'sum_size1':finalDS[i][1],'avg_requests1':finalDS[i][2],'avg_size1':finalDS[i][3],'Sample_stdev_requests1':finalDS[i][4],'Sample_stdev_size1':finalDS[i][5],'Population_stdev_requests1':finalDS[i][6],'Population_stdev_size1':finalDS[i][7],'total_Load1':finalDS[i][8],'language_occur1':finalDS[i][9],'sum_requests2':finalDS[i+1][0],'sum_size2':finalDS[i+1][1],'avg_requests2':finalDS[i+1][2],'avg_size2':finalDS[i+1][3],'Sample_stdev_requests2':finalDS[i+1][4],'Sample_stdev_size2':finalDS[i+1][5],'Population_stdev_requests2':finalDS[i+1][6],'Population_stdev_size2':finalDS[i+1][7],'total_Load2':finalDS[i+1][8],'language_occur2':finalDS[i+1][9],'sum_requests3':finalDS[i+2][0],'sum_size3':finalDS[i+2][1],'avg_requests3':finalDS[i+2][2],'avg_size3':finalDS[i+2][3],'Sample_stdev_requests3':finalDS[i+2][4],'Sample_stdev_size3':finalDS[i+2][5],'Population_stdev_requests3':finalDS[i+2][6],'Population_stdev_size3':finalDS[i+2][7],'total_Load3':finalDS[i+2][8],'language_occur3':finalDS[i+2][9],'sum_requests4':finalDS[i+3][0],'sum_size4':finalDS[i+3][1],'avg_requests4':finalDS[i+3][2],'avg_size4':finalDS[i+3][3],'Sample_stdev_requests4':finalDS[i+3][4],'Sample_stdev_size4':finalDS[i+3][5],'Population_stdev_requests4':finalDS[i+3][6],'Population_stdev_size4':finalDS[i+3][7],'total_Load4':finalDS[i+3][8],'language_occur4':finalDS[i+3][9],'target_load': target})
		csvfile.close()
	print("finish!")

#increment or create new register for each new line read
def add_to_ds_4h(rawline,lan):
	global tmplist1
	global tmplist2
	global dictWebsize
	global dictRequest

	tmplist1 = []
	tmplist2 = []
	line = rawline

	splitedline =line.split()
	linesize = len(splitedline)
	languageRaw = splitedline[0]
	language = languageRaw.split('.',1)[0]    										#saves just the language identifier, i.e. "en","pt",etc...
	if lan != language:
		return 1
	websize = float(re.sub('[^0-9]','', splitedline[linesize-1]))					#remove the non numeric values from the webpage size field			
	requestNum = float(re.sub('[^0-9]','',splitedline[linesize-2]))					#Create a number of request field in int type
	load = requestNum * websize														#Calculate the total load of the generate by the webpage
	if ds[0] != []:
		ds[0][0] = ds[0][0] + requestNum											#increment the sum of the request number
		ds[1][0] = ds[1][0] + websize												#increment the sum of the webpage size
		ds[8][0] = ds[8][0]+ load													#increment the sum of the load
		ds[9][0] = ds[9][0]  + 1													#increment the occurance counter
		tmplist1 = dictRequest.get(language)
		tmplist1.append(requestNum)
		tmplist2 = dictWebsize.get(language)
		tmplist2.append(websize)
		dictRequest[language] = tmplist1	
		dictWebsize[language] = tmplist2
	else:
		ds[0].append(requestNum)
		ds[1].append(websize)												
		ds[8].append(load)														
		ds[9].append(1)
		dictRequest[language] =  []
		dictWebsize[language] =  []
		tmplist1 = dictRequest.get(language)
		tmplist1.append(requestNum)
		tmplist2 = dictWebsize.get(language)
		tmplist2.append(websize)
			
#calculates the average,standard deviaton for request and webpage size
def calculate_all_4h(desiredLang):
	#Average
		if 'empty' == dictRequest.get(desiredLang,'empty'):
			ds[2].append(0)
			ds[3].append(0)
		else:
			ds[2].insert(0,statistics.mean(dictRequest.get(desiredLang)))
			ds[3].insert(0,statistics.mean(dictWebsize.get(desiredLang)))
		
	#Sample Standard Deviation
		if 'empty' == dictRequest.get(desiredLang,'empty'):
			ds[4].append(0)
			ds[5].append(0)
		elif len(dictRequest.get(desiredLang)) <2:
			ds[4].insert(0,0)
			ds[5].insert(0,0)
		else:
			ds[4].insert(0,statistics.stdev(dictRequest.get(desiredLang)))
			ds[5].insert(0,statistics.stdev(dictWebsize.get(desiredLang)))

	#Population Standard Deviation
		if 'empty' == dictRequest.get(desiredLang,'empty'):
			ds[6].append(0)
			ds[7].append(0)
		elif len(dictRequest.get(desiredLang)) <2:
			ds[6].insert(0,0)
			ds[7].insert(0,0)
		else:
			ds[6].insert(0,statistics.pstdev(dictRequest.get(desiredLang)))
			ds[7].insert(0,statistics.pstdev(dictWebsize.get(desiredLang)))

