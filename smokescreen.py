from smokescreen_utilities import *


def turnReturnsIntoValues(monthly_returns_timing):
	x = 100.0
	b = len(monthly_returns_timing)
	monthly_values_timing = []
	m11 = []
	m12 = []

	for i in range(b):
		monthly_values_timing.append([x, monthly_returns_timing[i][1]] )
		m11.append(x)
		m12.append(monthly_returns_timing[i][1])
		x *= monthly_returns_timing[i][0]

	return monthly_values_timing, m11, m12



def strategy1(myfile, moving_ave_list):

	m = len(myfile)
	mm = len(moving_ave_list)
	n = 0
	months = 0
	returns = []
	closes = []
	monthly_returns_timing = []
	monthly_returns_index = []
	
	Cash = True
	Equity = False

	for i in range(m):
	
		close, close_dt, close_month = getMAInfo(myfile, i)
		
		#print(close_dt)
		#print(moving_ave_list[n][1])
		
		if n < mm:
			if close_dt == moving_ave_list[n][1]:
			
				closes.append((round(close,2), close_dt))
			
				if moving_ave_list[n][0] > 0.0:
				
					if close > moving_ave_list[n][0]:
						
						if Cash:
							
							r = 1 + getInterestRate(close_dt)
							returns.append([r**((float)(months)/12.0), close_dt])
							A = close
							monthly_returns_timing.append([r**(1.0/12.0), close_dt])
						
						else:
						
							monthly_returns_timing.append([close/lastA, close_dt])
							

						Equity = True
						Cash = False
				
					else:
					
						if Equity:
						
							returns.append([close/A, close_dt])
							months = 0
							monthly_returns_timing.append([close/lastA, close_dt])

						else:
						
							r = 1 + getInterestRate(close_dt)
							months += 1
							monthly_returns_timing.append([r**(1.0/12.0), close_dt])
						
						
						Cash = True
						Equity = False
									
				else:
					months += 1
					lastA = close
				
				monthly_returns_index.append([close/lastA, close_dt])
				lastA = close
				n += 1
		else:
			break
			

	t = len(returns)

	retval = 1.0
	for j in range(t):
		retval *= returns[j][0]
		#print(retval, '\t', returns[j][1])

	# print(closes)

	return retval, closes, returns, monthly_returns_index, monthly_returns_timing








def calculateMovingAverage(myfile):

	m = len(myfile)
	avelist = []
	moving_ave_list = []
	
	last_close, last_close_dt, last_time = getMAInfo(myfile, 0)

	for i in range(1, m):
	
		this_close, this_close_dt, this_time = getMAInfo(myfile, i)

		# print(this_time)

		if this_time != last_time:
			# print("updating")
			moving_ave_list, avelist = updateMovingAverage(moving_ave_list, avelist, last_close, last_close_dt, num_periods)
			last_time = this_time
			last_close = this_close
			last_close_dt = this_close_dt
		else:
			last_close = this_close

	return moving_ave_list, avelist
			


def findDrawdownsPD(myfile, uninteresting_limit):

	m = len(myfile)
	ddlist = []

	maxclose, maxclose_date, maxindex = myfile.iloc[0]['Close'], myfile.iloc[0]['Date'], 0
	minclose, minclose_date, minindex = myfile.iloc[0]['Close'], myfile.iloc[0]['Date'], 0
	maxdd = 0.0
	looking = False

	for i in range(1, m):

		if myfile.iloc[i]['Close'] > maxclose:
			
			if looking:
			
				dd = (maxclose - minclose)/maxclose
				
				if dd > maxdd:
					maxdd, maxdd_start_date, maxdd_end_date = dd, maxclose_date, minclose_date
					
				if dd > uninteresting_limit:
				
					ddlist.append((dd, maxclose_date, minclose_date))
					print(str(dd) + " " + str(maxclose_date) + " " +  str(minclose_date))
					df = myfile[maxindex:minindex+1]
					#df.plot(x='Date', y='Close')
					#plt.show()
				
			minclose, minclose_date = myfile.iloc[i]['Close'], myfile.iloc[i]['Date']
			
			maxclose, maxclose_date, maxindex = myfile.iloc[i]['Close'], myfile.iloc[i]['Date'], i
			
			looking = False
		
		else:
		
			looking = True
			
			if myfile.iloc[i]['Close'] <= minclose:
				minclose, minclose_date, minindex = myfile.iloc[i]['Close'], myfile.iloc[i]['Date'], i


#	print(" The maximimum drawdown was " + str(round(maxdd*100.0, 3)) + "%, the period for this drawdown started on " + str(maxdd_start_date) + " and ended on " + str(maxdd_end_date) )
#	print(maxdd_start_date)
#	print(maxdd_end_date)

	return ddlist, (round(maxdd*100.0, 3), maxdd_start_date, maxdd_end_date)




def findDrawdowns(myfile, uninteresting_limit):

	m = len(myfile)
	ddlist = []

	maxclose, maxclose_date, maxindex = myfile[0][0], myfile[0][1], 0
	minclose, minclose_date, minindex = myfile[0][0], myfile[0][1], 0
	maxdd = 0.0
	looking = False

	for i in range(1, m):

		if myfile[i][0] > maxclose:
			
			if looking:
			
				dd = (maxclose - minclose)/maxclose
				
				if dd > maxdd:
					maxdd, maxdd_start_date, maxdd_end_date = dd, maxclose_date, minclose_date
					
				if dd > uninteresting_limit:
				
					ddlist.append((dd, maxclose_date, minclose_date))
					print(str(dd) + " " + str(maxclose_date) + " " +  str(minclose_date))
					# df = myfile[maxindex:minindex+1]
					# df.plot(x='Date', y='Close')
					#plt.show()
				
			minclose, minclose_date, minindex = myfile[i][0], myfile[i][1], i
			maxclose, maxclose_date, maxindex = myfile[i][0], myfile[i][1], i
			
			looking = False
		
		else:
		
			looking = True
			
			if myfile[i][0] <= minclose:
				minclose, minclose_date, minindex = myfile[i][0], myfile[i][1], i

	return ddlist, (round(maxdd*100.0, 3), maxdd_start_date, maxdd_end_date)



def takeFirst(elem):
	return elem[0]



# myfile = pd.read_csv("s_p_12301927.csv", sep='\t', header=0)
# myfile = pd.read_csv("s_p_12301927.csv", sep=',', header=0)
# myfile = pd.read_csv("s_p_12311929.csv", sep=',', header=0)
myfile = pd.read_csv("s_p_12291989.csv", sep=',', header=0)

ddlist, ddtriple = findDrawdownsPD(myfile, .1)

moving_ave_list, avelist = calculateMovingAverage(myfile)

# print(moving_ave_list, "\t", avelist, "\t", len(moving_ave_list))

overall_return, closes, returns, monthly_returns_index, monthly_returns_timing = strategy1(myfile, moving_ave_list)

print(overall_return, "\t", len(closes))

print(closes[len(closes)-1][0]/closes[0][0])

listResults(moving_ave_list, closes)

returns.sort(key=takeFirst)

# print(returns)

# print(monthly_returns_index, "\t", len(monthly_returns_index))
# print(monthly_returns_timing, "\t", len(monthly_returns_timing))

ttl = 0.0
b = len(monthly_returns_index)

for i in range(10, b):
	ttl += monthly_returns_index[i][0]

mu_index_returns = ttl / len(monthly_returns_index)
# print(mu_index_returns)

ttl = 0.0

for i in range(10, len(monthly_returns_index)):
	ttl += (monthly_returns_index[i][0] - mu_index_returns)**2


ttl /= (len(monthly_returns_index) - 10)
ttl0 = pow(ttl, .5)



ttl = 0.0
b = len(monthly_returns_timing)

for i in range(b):
	ttl += monthly_returns_timing[i][0]


mu_timing_returns = ttl / len(monthly_returns_timing)
# print(mu_timing_returns)

ttl = 0.0

for i in range( len(monthly_returns_timing)):
	ttl += (monthly_returns_timing[i][0] - mu_timing_returns)**2

ttl /= len(monthly_returns_timing)
ttl1 = pow(ttl, .5)

print(ttl0, '\t', ttl1)


monthly_values_timing, mm, mm1 = turnReturnsIntoValues(monthly_returns_timing)
monthly_values_index, nn, nn1 = turnReturnsIntoValues(monthly_returns_index)



# print(monthly_values_timing)

ddlist1, ddtriple1 = findDrawdowns(monthly_values_timing, .1)



# plt.plot(x,y, 'C2o', markersize=4)

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1,1,1)


plt.title('30 Years - SMA Market Timing Model versus S&P')
plt.plot(mm1[6::12], np.array(mm[6::12]),'b-', label='Timing Model')
plt.plot(nn1[16::12], np.array(nn[16::12]),'r-', label='S&P')
legend = ax.legend(loc='upper center', shadow=True, fontsize='large')
# ax.set_xlabel('')
ax.set_ylabel('Portfolio Size USD (x $1,000 )')

plt.show()
