import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import numpy as np

# print(myfile)
# print(myfile.keys())
# print(myfile[['Date','Close'][1]])
# print(myfile[1:25])

# print(myfile.describe())

num_periods = 10
#ave_commission_rates = [(1930, .01), (1940, .01), (1950, .01), (1960, .012), (1970, .012), (1980, .008), (1990, .004), (2000, .002), (2010, .002)]
ave_commission_rates = [(70, .012), (80, .008), (90, .004), (00, .002), (10, .002)]
ave_interest_rates = [(70, .075), (80, .12), (90, .06), (00, .025), (10, .01)]

mpl.rc('xtick', labelsize=5)
mpl.rc('ytick', labelsize=5)


def listResults(moving_ave_list, closes):
	
	
	ofile = open("lookie.csv", "w")
	
	m = len(closes)
		
	s = "Date, " + "MA, " + "Close\n"
	ofile.write(s)
	
	for i in range(m):
		s =  closes[i][1] + ", " + str(moving_ave_list[i][0]) + ", " + str(closes[i][0]) + "\n"
		ofile.write(s)
	
	ofile.close()
	
	return


def mean(thelist, freq):

	avel = 0.0
	for i in range(freq):
		avel += thelist[i]
	avel /= float(freq)

	return avel



def updateMovingAverageList(avelist, newclose, freq):
	
	if len(avelist) < freq:
		avelist.append(newclose)
		mu = 0.0
	else:
		for i in range(freq-1):
			avelist[i] = avelist[i+1]
		avelist[freq-1] = newclose
		mu = mean(avelist, freq)

	return avelist, mu



def updateMovingAverage(moving_ave_list, avelist, newclose, new_close_dt, freq):

	avelist, mu = updateMovingAverageList(avelist, newclose, freq)
	moving_ave_list.append((round(mu,2), new_close_dt))

	return moving_ave_list, avelist



def getInterestRate(close_dt):
	close_year = getYear(close_dt)
	irate = 0.0
	for xtuple in ave_interest_rates:
		# print(close_year, "\t", xtuple[0], "\t")
		if (close_year - close_year%10) == xtuple[0]:
			irate = xtuple[1]
			break
	
	return irate



def getMonth(close_dt):
	date_object = datetime.strptime(close_dt, "%m/%d/%y")
	close_month = int(date_object.strftime("%m"))
	
	return close_month



def getYear(close_dt):
	date_object = datetime.strptime(close_dt, "%m/%d/%y")
	close_year = int(date_object.strftime("%y"))
	
	return close_year



def getMAInfo(myfile, i):
	close = myfile.iloc[i]['Close']
	close_dt = myfile.iloc[i]['Date']
	close_month = getMonth(close_dt)

	return close, close_dt, close_month
