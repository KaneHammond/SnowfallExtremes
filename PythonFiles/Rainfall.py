from BasicImports import *

def Rainfall(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData):
	# Format: RAWDATA [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
	# Format: STANDARDSNOW [Annual Snowfall, Snow Days, Daily Ave, Start D, End D, Season Length]
	# 3 is precip

	##################################### DATA PREP

	# This section will extract all precipitation data, including snowfall. The
	# snowfall data will be converted to SWE using a standard 1/10 estimate.
	# The annual totals and monthly data will be extracted. Supporting data such
	# as corresponding year and month will also be recorded for reference.
	# Annual assessments are based upon the Year signifier on the end of each record,
	# see the master file to reference what month the 'year' will start. For example,
	# if using a hydro year, the first month will be 10 for October.

	# Filter the data, remove temp information. Leave: [Year, DD, MM, Precip, Snow, Hydro Year]
	SelectData = []
	SY = BaseData[0][0]
	i = 1
	for aItem in BaseData:
		T1 = aItem[0:5]
		if T1[0]!= SY:
			SY = T1[0]
			i = i+1
		T1.append(i)
		SelectData.append(T1)

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

	# Define the starting year (i) and the starting month (im) in the data
	i = SelectData[0][-1]
	im = SelectData[0][2]
	# print SelectData[0]
	# Parse the data for calculations
	for aRow in SelectData:
		# If the row is equal to our year/counting index, check for rain data
		if aRow[-1]==i:
			if np.isnan(aRow[3]) != True:
				# This will record all rain data for the year (annual totals)
				AnnCount = AnnCount+aRow[3]
				if aRow[2] == im:
					# If a variable is equal to the month of interest, collect the 
					# rain data for that record
					if np.isnan(aRow[3]) != True:
						# Verify it is not nan
						# Record the year
						YearTemp = aRow[-1]
						# Record the rain data
						tempRain = tempRain+aRow[3]
				if aRow[2] != im:
					# Modify the month if it has changed
					# Record the month
					Months.append(im)
					# Record the year for that month
					Years.append(YearTemp)
					# Record the total rain for that month
					MonthlyRainfall.append(tempRain)
					tempRain = 0
					# Variables have been reset. Record the data
					# for the record passing. Var converts row value
					# to int value. Has issues using direct row value.
					var = int(aRow[2])
					im = var
					# Define our variables of interest from the passed data record
					YearTemp = aRow[-1]
					if np.isnan(aRow[3]) != True:
						# Verify it is not nan
						# Record the year
						YearTemp = aRow[-1]
						# Record the rain data
						tempRain = tempRain+aRow[3]
		if aRow[-1]!=i:
			# If our year has changed, we need to now extract data
			# as well as change the variables for the next loop

			# Add the previous month to our set
			Months.append(im)
			# Add year
			Years.append(YearTemp)
			# Add our monthly rain total
			MonthlyRainfall.append(tempRain)
			# Set tempRain back to 0
			tempRain = 0
			# A new year has started so we now add the annual total to a list
			AnnualSum.append(AnnCount)
			# This will be our list of years relating to the annual totals
			AnnualDate.append(YearTemp)
			# Set AnnCount back to 0
			AnnCount = 0
			# Variables have been reset. Record the data
			# for the record passing. Var converts row value
			# to int value. Has issues using string item vs int item.
			# Define month
			var = int(aRow[2])
			im = var
			# Define year
			var = int(aRow[-1])
			i = var
			YearTemp = aRow[-1]
			# Begin adding monthly data to set
			if np.isnan(aRow[3]) != True:
				# Verify it is not nan
				# Record the year
				YearTemp = aRow[-1]
				# Record the rain data
				tempRain = tempRain+aRow[3]
			# tempRain has been reset, so incase it has accumulated snowfall or
			# rain within this passing record, tempRain will only contain data for
			# this single record.
			AnnCount = AnnCount+tempRain

	# Final loop break, append all data from last loop
	Months.append(im)
	Years.append(YearTemp)
	MonthlyRainfall.append(tempRain)
	AnnualSum.append(AnnCount)
	AnnualDate.append(YearTemp)


	################################### Parsed by year

	# yearly precip per month
	YPM = []
	Temp = []
	i = 0
	for aItem in MonthlyRainfall:
		if i < 12:
			Temp.append(aItem)
			i = i+1
		if i == 12:
			YPM.append(Temp)
			Temp = []
			i = 0

	####################################### Rainfall Extremes

	# Calculate Rainfall cdf

	# Def to automate the calculation more easily
	def CDF(Data, x, y):
		counter=collections.Counter(Data)
		# The rv_discrete function requires unique values.
		# This provides the values to fulfill the arguments.
		F = copy.deepcopy(counter.values())
		Fsum = sum(F)
		Frequency = []
		for aRow in F:
			z = float(aRow)
			temp = z/Fsum
			Frequency.append(temp)
		# Sum of Frequency is now 1. This is required for the rv_discrete function.
		# This discrete function provides a start and end value for the CDF.
		# This ensures that the highest value in a dataset is given the value of
		# 1. Meaning %100 of the records are below the highest recorded amount. 

		Variables = copy.deepcopy(counter.keys())

		CDF = scipy.stats.rv_discrete(values=(Variables, Frequency))
		CDF = CDF.cdf(Variables)
		# x is snowfall amount
		TempX = sorted(Variables)
		# y is CDF values for each variable
		TempY = sorted(CDF)
		for aItem in TempX:
			x.append(aItem)
		for aItem in TempY:
			y.append(aItem)


	# Calculate overall CDF of rainfall
	RainOnlyD = []
	for aRow in BaseData:
		RainOnlyD.append(aRow[3])

	x = []
	y = []
	CDF(RainOnlyD, x, y)

	fig, ax = plt.subplots(1, 1)
	ax.grid(True)
	#SE is pre-defined variable representing CDF limit
	ax.text(-0.01, 0.93, '%s' % ('90'), verticalalignment='top', 
		horizontalalignment='right', transform=ax.transAxes, fontsize=9,
		fontweight='bold', color='r')
	ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
		horizontalalignment='center', transform=ax.transAxes, fontsize=12,
		fontweight=None, color='black')
	ax.plot(x, y, label='CDF')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='right')
	ax.set_title('Cumulative Distrbution of Rainfall')
	ax.set_xlabel('Daily Rainfall (mm)')
	ax.set_ylabel('CDF Value')
	# ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
	ax.set_yticks([0.9], minor=True)
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	# plt.savefig('%s/CDF_Snowfall.%s' % (dir, f), 
		# dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		# papertype=None, format=None, transparent=False, bbox_inches=None, 
		# pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()


	# Calculate CDF for spring summer and fall

	Spring = []
	Summer = []
	Fall = []

	Seasons = [Spring, Summer, Fall]
	SeasonsStr = ['Spring', 'Summer', 'Fall']

	for aRow in YPM:
		Temp = aRow[2]+aRow[3]+aRow[4]
		Spring.append(Temp)
		Temp = aRow[5]+aRow[6]+aRow[7]
		Summer.append(Temp)
		Temp = aRow[8]+aRow[9]+aRow[10]
		Fall.append(Temp)

	CDFlim = []

	i = 0
	while i<len(Seasons):
		x = []
		y = []
		CDF(Seasons[i], x, y)

		# Extract cdf limit
		z = 0
		Temp = []
		for aItem in y:
			if aItem >= 0.9:
				Temp = [aItem, x[z]]
				CDFlim.append(Temp)
				break
			z = z+1

		fig, ax = plt.subplots(1, 1)
		ax.grid(True)
		#SE is pre-defined variable representing CDF limit
		ax.text(-0.01, 0.93, '%s' % ('90'), verticalalignment='top', 
			horizontalalignment='right', transform=ax.transAxes, fontsize=9,
			fontweight='bold', color='r')
		ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
			horizontalalignment='center', transform=ax.transAxes, fontsize=12,
			fontweight=None, color='black')
		ax.plot(x, y, label='CDF')
		# ax.plot(x, y2, label='Reversed emp.')
		ax.legend(loc='right')
		ax.set_title('Cumulative Distrbution of Rainfall %s' % SeasonsStr[i])
		ax.set_xlabel('Seasonal Rainfall (mm)')
		ax.set_ylabel('CDF Value')
		# ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
		ax.set_yticks([0.9], minor=True)
		# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
		ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
		# plt.savefig('%s/CDF_Snowfall.%s' % (dir, f), 
			# dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
			# papertype=None, format=None, transparent=False, bbox_inches=None, 
			# pad_inches=0.1, frameon=None)
		# plt.show()
		plt.close()
		i = i+1

	# Determine frequency of CDF extreme precipitaion seasons
	# index to determine year

	Years = []
	for x in xrange(int(BaseData[0][0]), int(BaseData[-1][0])+1):
		Years.append(int(x))

	# i = 0
	# SPR_EE = []
	# for aItem in Spring:
	# 	if aItem >= CDFlim[0][-1]:
	# 		SPR_EE.append(Years[i])
	# 	i = i+1

	i = 0

	while i < len(Seasons):
		fig, ax = plt.subplots(1, 1)
		Years = np.array(Years)
		S = np.array(Seasons[i])
		mask = ~np.isnan(Years) & ~np.isnan(S)
		ax.grid(True)
		ax.plot(Years, S, label='Rainfall Total (mm)')
		# ax.plot(x, y2, label='Reversed emp.')
		ax.legend(loc='upper right')
		ax.set_title('Seasonal Rainfall %s' % SeasonsStr[i])
		ax.set_xlabel('Year')
		ax.set_ylabel('Rainfall (mm)')
		# ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
		ax.set_yticks([0.9], minor=True)
		# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
		ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
		slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
		plt.plot(Years,intercept+slope*Years, 'r')
		ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
		    (slope, p_value, r_value), verticalalignment='bottom', 
		    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
		# plt.savefig('%s/CDF_Snowfall.%s' % (dir, f), 
			# dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
			# papertype=None, format=None, transparent=False, bbox_inches=None, 
			# pad_inches=0.1, frameon=None)
		# plt.show()
		plt.close()
		i = i+1

	##################################### Annual Rainfall Totals

	AnnualRainfall = []
	for aItem in YPM:
		AnnualRainfall.append(sum(aItem))

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(AnnualRainfall)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Rainfall Total (mm)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('Annual Rainfall')
	ax.set_xlabel('Year')
	ax.set_ylabel('Rainfall (mm)')
	# ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
	ax.set_yticks([0.9], minor=True)
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	# plt.savefig('%s/CDF_Snowfall.%s' % (dir, f), 
		# dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		# papertype=None, format=None, transparent=False, bbox_inches=None, 
		# pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)
