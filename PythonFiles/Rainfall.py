from BasicImports import *

def Rainfall(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData):
	# 3 is precip

	# Calculate monthly totals of liquid precip
	# Years is the year data for the month records
	Years = []
	# YearTemp is the temporary record for recording the year
	# each month is located in
	YearTemp = 0
	# Months is the list of months to align with totals
	Months = []
	# MonthlyRainfall is the list of monthly totals
	MonthlyRainfall = []
	# tempRain is the count of rainfall within the month
	tempRain = 0

	# AnnCount is the counting variable for annual totals
	AnnCount = 0
	AnnualSum = []
	AnnualDate = []

	i = RawData[0][-1]
	im = RawData[0][2]
	# print RawData[0]
	for aRow in RawData:

		if aRow[-1]==i:
			if np.isnan(aRow[3]) != True:
				AnnCount = AnnCount+aRow[3]
				if aRow[2] == im:
					# print aRow
					if np.isnan(aRow[3]) != True:
						YearTemp = aRow[0]
						tempRain = tempRain+aRow[3]
				if aRow[2] != im:
					# print aRow
					Months.append(im)
					Years.append(YearTemp)
					MonthlyRainfall.append(tempRain)
					tempRain = 0
					# Variables have been reset. Record the data
					# for the record passing. Var converts row value
					# to int value. Has issues using direct row value.
					var = int(aRow[2])
					im = var
					YearTemp = aRow[0]
					tempRain = tempRain+aRow[3]
		if aRow[-1]!=i:
			Months.append(im)
			Years.append(YearTemp)
			MonthlyRainfall.append(tempRain)
			# Set tempRain back to 0
			tempRain = 0
			AnnualSum.append(AnnCount)
			AnnualDate.append(YearTemp)
			# Set AnnCount back to 0
			AnnCount = 0
			# Variables have been reset. Record the data
			# for the record passing. Var converts row value
			# to int value. Has issues using direct row value.
			var = int(aRow[2])
			im = var
			var = int(aRow[-1])
			i = var
			YearTemp = aRow[0]
			if np.isnan(aRow[3]) != True:
				tempRain = tempRain+aRow[3]
				AnnCount = AnnCount+aRow[3]

	Months.append(im)
	Years.append(YearTemp)
	MonthlyRainfall.append(tempRain)
	AnnualSum.append(AnnCount)
	AnnualDate.append(YearTemp)
	# print len(Months)
	# print len(Years)
	# print len(MonthlyRainfall)
	# print len(AnnualDate)
	# print len(AnnualSum)
	i = 0
	im = 0
	def Xvar(x, y):
		return abs(float(x) - float((y/12)))

	def Yvar(x,y):
		return float(1/(1.83*x))*y

	SeasonalityIndex = []
	MonthVals = []
	for aRow in MonthlyRainfall:
		if im < 12:
			x = aRow
			y = AnnualSum[i]
			# if y != 0 or x != 0:
			Temp = Xvar(x, y)

			MonthVals.append(Temp)
			# if y == 0 or x == 0:
			# 	MonthVals.append(np.nan)
			im = im+1
		# Month count started at 0 so 12 is the 13th variable
		# representing a year change.
		if im==12:
			if i==len(AnnualSum):
				break
			im==0
			y = sum(MonthVals)
			if AnnualSum[i]!=0:
				SI = Yvar(AnnualSum[i], y)
				SeasonalityIndex.append(SI)
			if AnnualSum[i]==0:
				SeasonalityIndex.append(np.nan)
			i = i+1
			# break
	# print SeasonalityIndex
	TotalYears = RawData[-1][-1]
	x = AnnualDate
	x = np.array(x)
	SeasonalityIndex = np.array(SeasonalityIndex)
	mask = ~np.isnan(x) & ~np.isnan(SeasonalityIndex)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.grid(True)
	ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
	    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	    fontweight=None, color='black')
	fig.subplots_adjust(top=0.85)
	ax.set_xlabel(YearLabel)
	ax.set_ylabel('Seasonality Index Over Time')
	ax.set_title('Study Period Seasonality Index(%i Years)' % (TotalYears), fontweight='bold')
	plt.plot(x,SeasonalityIndex,  'ro')
	# slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], SeasonalityIndex[mask])
	# plt.plot(x,intercept+slope*x, 'r')
	# ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	#     (slope, p_value, r_value), verticalalignment='bottom', 
	#     horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	# plt.savefig('%s/Annual_Average_Daily_STD.%s' % (dir, f))
	# StationExports.append(slope)
	# StationExports.append(p_value)
	# StationExports.append(r_value)

	# plt.show()
	plt.close()


	# Total seasonality index
	# Write a df with monthly totals and months
	df = pd.DataFrame({'Rain': MonthlyRainfall, 'Month': Months})
	# Convert to list
	Data = df.values.tolist()

	# Define months
	Jan = []
	Feb = []
	Mar = []
	Apr = []
	May = []
	Jun = []
	Jul = []
	Aug = []
	Sep = []
	Oct = []
	Nov = []
	Dec = []

	for aRow in Data:
		aRow[0] = int(aRow[0])
		if aRow[0]==1:
			Jan.append(aRow[1])
		if aRow[0]==2:
			Feb.append(aRow[1])
		if aRow[0]==3:
			Mar.append(aRow[1])
		if aRow[0]==4:
			Apr.append(aRow[1])
		if aRow[0]==5:
			May.append(aRow[1])
		if aRow[0]==6:
			Jun.append(aRow[1])
		if aRow[0]==7:
			Jul.append(aRow[1])
		if aRow[0]==8:
			Aug.append(aRow[1])
		if aRow[0]==9:
			Sep.append(aRow[1])
		if aRow[0]==10:
			Oct.append(aRow[1])
		if aRow[0]==11:
			Nov.append(aRow[1])
		if aRow[0]==12:
			Dec.append(aRow[1])
	SeasonalityIndex = []
	MonthVals = [sum(Jan)/30, sum(Feb)/30, sum(Mar)/30, sum(Apr)/30, sum(May)/30, 
		sum(Jun)/30, sum(Jul)/30, sum(Aug)/30, sum(Sep)/30, 
		sum(Oct)/30, sum(Nov)/30, sum(Dec)/30]
	im = 1
	# print sum(MonthVals)
	x = sum(MonthVals)
	temp = []
	for aRow in MonthVals:
		tVar = Xvar(aRow, x)
		temp.append(tVar)
	y = sum(temp)
	SI = Yvar(x, y)
	# print SI




	# Calculate total seasonal precip

	df = pd.DataFrame(RawData, columns=['Year', 'Day', 'Month', 'Precip', 'Snow', 'Tmax','Tmin', 'TOBS', 'Year'])
	df = df.drop(columns=['Snow', 'Tmax','Tmin', 'TOBS'])
	allData = df.values.tolist()

	WinterSum = []

	for aRow in allData:
		if aRow[2] == 12 or aRow[2] == 1 or aRow[2] == 2:
			WinterSum.append(aRow[3])

	SpringSum = []

	for aRow in allData:
		if aRow[2] == 3 or aRow[2] == 4 or aRow[2] == 5:
			SpringSum.append(aRow[3])

	SummerSum = []

	for aRow in allData:
		if aRow[2] == 6 or aRow[2] == 7 or aRow[2] == 8:
			SummerSum.append(aRow[3])

	FallSum = []

	for aRow in allData:
		if aRow[2] == 9 or aRow[2] == 10 or aRow[2] == 11:
			FallSum.append(aRow[3])

	WinterSum = np.array(WinterSum)
	WinterSum = np.nansum(WinterSum)

	FallSum = np.array(FallSum)
	FallSum = np.nansum(FallSum)

	SpringSum = np.array(SpringSum)
	SpringSum = np.nansum(SpringSum)

	SummerSum = np.array(SummerSum)
	SummerSum = np.nansum(SummerSum)

	# Data to plot
	labels = 'Winter', 'Spring', 'Summer', 'Fall'
	sizes = [WinterSum, SpringSum, SummerSum, FallSum]
	colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
	explode = (0, 0, 0, 0)  # explode a slice 0 means none
	 
	# Plot
	plt.pie(sizes, explode=explode, labels=labels, colors=colors,
	        autopct='%1.1f%%', shadow=True, startangle=140)
	
	plt.axis('equal')
	plt.title('Seasonal Precipitation Over Study Period (%i Years)' % (TotalYears), fontweight='bold')
	plt.text(.5, 1.12, 'Station: %s' % (StationName), verticalalignment='center', 
	    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	    fontweight=None, color='black')	
	# plt.show()
	plt.close()

	# Annual probabilty 

	df = pd.DataFrame({"Sum Of Rainfall" : AnnualSum, "Date" : AnnualDate})
	df = df.replace(0, np.nan)
	df = df.sort_values(['Sum Of Rainfall'])
	df = df.dropna(how='any')

	Data = df.values.tolist()

	x = []
	for aRow in Data:
		print aRow[0]
		x.append(aRow[-1])

	Bin = collections.Counter(x)
	bins = Bin.keys()
	n = len(Data)
	data = np.array(x)
	STD = np.nanstd(data)
	Av = np.nanmean(data)

	# print np.percentile(data, 99)
	mu, sigma = Av, STD

	# # Create the bins and histogram
	# count, bins, ignored = plt.hist(data, 20, normed=True)

	# # Plot the distribution curve
	# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
	# 	np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
	# plt.show()


	# best fit of data
	(mu, sigma) = norm.fit(data)



	# the histogram of the data
	n, bins, patches = plt.hist(data, len(bins)-1, normed=1, facecolor='green', alpha=0.75, label='Rainfall PDF')
	# add a 'best fit' line
	y = mlab.normpdf(data, mu, sigma)
	l = plt.plot(bins, y, 'r--', linewidth=2, label='Fit')

	#plot
	plt.xlabel('Rainfall')
	plt.ylabel('Probability')
	plt.title('Histogram of Rainfall Events 30 Years\n Average: %i     STD: %i' %(round(mu, 6), round(sigma, 6)))
	plt.legend()
	plt.grid(True)

	plt.show()



    # Recurrence interval for 100 year flood
	# def Rec(Years, Rank):
	# 	return float((Years+1)/Rank)

	# Recurrence = []
	# Years = Data[-1][0]
	# for aRow in Data:
	# 	Var = Rec(Years, aRow[0])
	# 	Recurrence.append(Var)

	# # Assume the data matched a gausian curve
	# y = np.array(y)
	# print np.percentile(y, 99)


	sys.exit()

