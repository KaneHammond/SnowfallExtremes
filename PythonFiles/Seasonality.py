from BasicImports import *

def Seasonality(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData, EE, StandardSnow):

	dir = 'Output/'+StationName+'/Seasonality'
	if not os.path.exists(dir):
		os.makedirs('Output/'+StationName+'/Seasonality')
	else:
		shutil.rmtree(dir)
		os.makedirs(dir)

	Output = 'Output/'+StationName+'/Seasonality/'

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

	# Filter the data, remove temp information. 
	# Leave: [Year, DD, MM, Precip, Snow, Index]
	# We use BaseData to allow for full analysis of seasons here.
	# RawData is clipped special for snowfall/winter analysis.
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
			if np.isnan(aRow[4]) != True:
				# This will include SWE
				# Estimate a 1/10 ratio of snow water equivalent
				AnnCount = AnnCount+(aRow[4]/10)
				if aRow[2] == im:
					# If a variable is equal to the month of interest, collect the 
					# rain data for that record
					if np.isnan(aRow[3]) != True:
						# Verify it is not nan
						# Record the year
						YearTemp = aRow[-1]
						# Record the rain data
						tempRain = tempRain+aRow[3]
					if np.isnan(aRow[4]) != True:
						# This will include SWE
						# Estimate a 1/10 ratio of snow water equivalent
						tempRain = tempRain+(aRow[4]/10)
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
					if np.isnan(aRow[4]) != True:
						# This will include SWE
						# Estimate a 1/10 ratio of snow water equivalent
						tempRain = tempRain+(aRow[4]/10)
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
			if np.isnan(aRow[4]) != True:
				# This will include SWE
				# Estimate a 1/10 ratio of snow water equivalent
				tempRain = tempRain+(aRow[4]/10)
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

	############################################# Seasonality Index (Annual)
	i = 0
	im = 0
	# Define defs for our SI calculation pg 179 Terrestrial Hydrometerology W. James Shuttleworth

	# Returns absolute value for half of equation
	def Xvar(x, y):
		return abs(float(x) - float((y/12)))

	# Other half of equation
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

	TotalYears = SelectData[-1][-1]
	x = AnnualDate
	x = np.array(x)
	# Put the SI data in a list for EE comparison
	SId = []
	for aItem in SeasonalityIndex:
		SId.append(aItem)

	print len(SId)
	sys.exit()

	# Plot our seasonality index

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
	ax.set_ylabel('Seasonality Index')
	ax.set_title('Study Period Seasonality Index(%i Years)' % (TotalYears), fontweight='bold')
	plt.plot(x,SeasonalityIndex,  'ro')
	slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], SeasonalityIndex[mask])
	plt.plot(x,intercept+slope*x, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%sSeasonality_Index.%s' % (Output, f))
	# StationExports.append(slope)
	# StationExports.append(p_value)
	# StationExports.append(r_value)

	# plt.show()
	plt.close()

	############################################# Seasonality Index (Entire period)

	# This requires data from the initial annual SI assessment. Therefore, it must 
	# come before the running mean SI>

	# Write a df with monthly totals and months
	df = pd.DataFrame({'Rain': MonthlyRainfall, 'Month': Months})
	# Convert to list, this will put the data side by side
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
		# Filter through months
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

	# Provide average precipitation per month, by taking the total for that month
	# over the entire period, then divide it by total years of analysis
	MonthVals = [sum(Jan)/TotalYears, sum(Feb)/TotalYears, sum(Mar)/TotalYears, sum(Apr)/TotalYears, sum(May)/TotalYears, 
		sum(Jun)/TotalYears, sum(Jul)/TotalYears, sum(Aug)/TotalYears, sum(Sep)/TotalYears, 
		sum(Oct)/TotalYears, sum(Nov)/TotalYears, sum(Dec)/TotalYears]
	im = 1

	# x will be the average total precip, based upon the estimated average monthly values
	x = sum(MonthVals)
	# Calculate total SI using equation from above
	temp = []
	for aRow in MonthVals:
		tVar = Xvar(aRow, x)
		temp.append(tVar)
	y = sum(temp)
	# This SI will represent total period SI
	SI = Yvar(x, y)


	#################################### Calculate total seasonal precip
	# Include SWE by 1/10 of snowfall value
	# Format: [Year, DD, MM, Precip, Snow, Hydro Year]
	df = pd.DataFrame(SelectData, columns=['Year', 'Day', 'Month', 'Precip', 'Snow', 'YearMod'])
	allData = df.values.tolist()

	WinterSum = []

	for aRow in allData:
		if aRow[2] == 12 or aRow[2] == 1 or aRow[2] == 2:
			if np.isnan(aRow[3]) != True:
				# Verify it is not nan, append rain to winter rain
				WinterSum.append(aRow[3])
			if np.isnan(aRow[4]) != True:
				# This will include SWE to winter precip total
				# Estimate a 1/10 ratio of snow water equivalent
				WinterSum.append(aRow[4]/10)

	SpringSum = []

	for aRow in allData:
		if aRow[2] == 3 or aRow[2] == 4 or aRow[2] == 5:
			if np.isnan(aRow[3]) != True:
				# Verify it is not nan, append rain to winter rain
				SpringSum.append(aRow[3])
			if np.isnan(aRow[4]) != True:
				# This will include SWE to winter precip total
				# Estimate a 1/10 ratio of snow water equivalent
				SpringSum.append(aRow[4]/10)

	SummerSum = []

	for aRow in allData:
		if aRow[2] == 6 or aRow[2] == 7 or aRow[2] == 8:
			if np.isnan(aRow[3]) != True:
				# Verify it is not nan, append rain to winter rain
				SummerSum.append(aRow[3])
			if np.isnan(aRow[4]) != True:
				# This will include SWE to winter precip total
				# Estimate a 1/10 ratio of snow water equivalent
				SummerSum.append(aRow[4]/10)

	FallSum = []

	for aRow in allData:
		if aRow[2] == 9 or aRow[2] == 10 or aRow[2] == 11:
			if np.isnan(aRow[3]) != True:
				# Verify it is not nan, append rain to winter rain
				FallSum.append(aRow[3])
			if np.isnan(aRow[4]) != True:
				# This will include SWE to winter precip total
				# Estimate a 1/10 ratio of snow water equivalent
				FallSum.append(aRow[4]/10)

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
	plt.savefig('%sSeasonal_Precip.%s' % (Output, f))
	# plt.show()
	plt.close()
	# sys.exit()

	##################################### Plot seasonal precip by year

	# Monthly values
	# Format: [Year, DD, MM, Precip, Snow, Hydro Year]

	# January not appending correctly 

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

	Months = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
	MonthsV = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
	MonthStr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	i = 0
	Y = allData[0][0]

	while i < len(Months):
		Temp = []
		for aRow in allData:
			if int(aRow[0])==int(Y):
				if int(aRow[2])==MonthsV[i]:
					if np.isnan(aRow[3]) != True:
						# Verify it is not nan, append rain to winter rain
						Temp.append(aRow[3])	
					if np.isnan(aRow[4]) != True:
						# This will include SWE to winter precip total
						# Estimate a 1/10 ratio of snow water equivalent
						Temp.append(aRow[4]/10)

			if int(aRow[0])!= int(Y):
				Y = Y+1
				Months[i].append(Temp)
				Temp = []

				if int(aRow[2])==MonthsV[i]:
					if np.isnan(aRow[3]) != True:
						# Verify it is not nan, append rain to winter rain
						Temp.append(aRow[3])	
					if np.isnan(aRow[4]) != True:
						# This will include SWE to winter precip total
						# Estimate a 1/10 ratio of snow water equivalent
						Temp.append(aRow[4]/10)

			if aRow==allData[-1]:
				Y = allData[0][0]
				Months[i].append(Temp)
		i = i+1

	MTP = []
	Temp = []
	for aList in Months:
		for aMList in aList:
			Temp.append(sum(aMList))
		MTP.append(Temp)
		Temp = []

	# Loop graph the data for monthly precipitaion totals of time
	Years = []
	for x in xrange(int(allData[0][0]), int(allData[-1][0])+1):
		Years.append(x)

	i = 0
	while i<len(MTP):
		MonthlyPrecip = np.array(MTP[i])
		xi = np.array(Years)
		mask = ~np.isnan(xi) & ~np.isnan(MonthlyPrecip)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.grid(True)
		ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
		    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
		    fontweight=None, color='black')
		fig.subplots_adjust(top=0.85)
		ax.set_xlabel('Year')
		ax.set_ylabel('Monthly Precipitation (mm)')
		ax.set_title('%s Total Precipitation by Year' % (MonthStr[i]), fontweight='bold')
		plt.plot(xi,MonthlyPrecip,  '-')
		slope, intercept, r_value, p_value, std_err = stats.linregress(xi[mask], MonthlyPrecip[mask])
		plt.plot(xi,intercept+slope*xi, 'r')
		ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
		    (slope, p_value, r_value), verticalalignment='bottom', 
		    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
		# plt.show()
		plt.savefig('%sMonthly_Precipitation_%s.%s' % (Output, MonthStr[i], f))
		plt.close()
		i = i+1


	############################### Plot seasonal precipitation over time

	# Due to months for winter season, this section is plotted seprately.
	# It requires the months of December, January, and Feburary.

	WinterSums = []
	i = 0
	while i < int(allData[-1][-1])-1:
		# Using december from the "year" before. 
		DecMod = i-1
		if DecMod>=0:
			WinterSum = MTP[-1][DecMod]+MTP[0][i]+MTP[1][i]
		if DecMod<0:
			WinterSum = np.nan
		WinterSums.append(WinterSum)
		i = i+1

	Years = []
	for x in xrange(int(allData[0][0]), int(allData[-1][0])):
		Years.append(x)

	Precip = np.array(WinterSums)
	xi = np.array(Years)
	mask = ~np.isnan(xi) & ~np.isnan(Precip)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.grid(True)
	ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
	    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	    fontweight=None, color='black')
	fig.subplots_adjust(top=0.85)
	ax.set_xlabel('Year')
	ax.set_ylabel('Seasonal Precipitation Total (mm)')
	ax.set_title('Total Precipitation by Season (Winter_Sums)', fontweight='bold')
	plt.plot(xi,Precip,  '-')
	slope, intercept, r_value, p_value, std_err = stats.linregress(xi[mask], Precip[mask])
	plt.plot(xi,intercept+slope*xi, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%sWinter_Sums_Precipitation.%s' % (Output, f))
	# plt.show()
	plt.close()

	# Spring Summer and Fall graphing

	SpringSums = []
	i = 0
	while i < int(allData[-1][-1]):
		SpringSum = MTP[2][i]+MTP[3][i]+MTP[4][i]
		SpringSums.append(SpringSum)
		i = i+1

	SummerSums = []
	i = 0
	while i < int(allData[-1][-1]):
		SummerSum = MTP[5][i]+MTP[6][i]+MTP[7][i]
		SummerSums.append(SummerSum)
		i = i+1

	FallSums = []
	i = 0
	while i < int(allData[-1][-1]):
		FallSum = MTP[8][i]+MTP[9][i]+MTP[10][i]
		FallSums.append(FallSum)
		i = i+1

	# Central seasons (the ones that don't pass into new year)
	CS = [SpringSums, SummerSums, FallSums]
	CSstr = ['Spring_Sums', 'Summer_Sums', 'Fall_Sums']

	Years = []
	for x in xrange(int(allData[0][0]), int(allData[-1][0])+1):
		Years.append(x)

	i = 0
	while i < len(CS):
		Precip = np.array(CS[i])
		xi = np.array(Years)
		mask = ~np.isnan(xi) & ~np.isnan(Precip)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.grid(True)
		ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
		    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
		    fontweight=None, color='black')
		fig.subplots_adjust(top=0.85)
		ax.set_xlabel('Year')
		ax.set_ylabel('Seasonl Precipitation Total (mm)')
		ax.set_title('Total Precipitation by Season (%s)' % (CSstr[i]), fontweight='bold')
		plt.plot(xi,Precip,  '-')
		slope, intercept, r_value, p_value, std_err = stats.linregress(xi[mask], Precip[mask])
		plt.plot(xi,intercept+slope*xi, 'r')
		ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
		    (slope, p_value, r_value), verticalalignment='bottom', 
		    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
		plt.savefig('%s%s_Precipitation.%s' % (Output, CSstr[i], f))
		# plt.show()
		plt.close()
		i = i+1


	###################################### Running mean SI
	# Format: RAWDATA [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
	# Format: STANDARDSNOW [Annual Snowfall, Snow Days, Daily Ave, Start D, End D, Season Length]

	# This section will calculate the SI based upon 3 year averages to smooth out the
	# data. As expressed in pg 182 Terrestrial Hydrometerology W. James Shuttleworth
	# as a running means SI.

	# Define the index values (years) and place them into the data records
	SIdMod = []
	i = 0
	for aItem in SId:
		SIdMod.append([aItem, i])
		i = i+1

	# Define the lenght of the data set
	Lenght =  len(SIdMod)
	# print Lenght
	# print SIdMod
	# sys.exit()

	# Define the window size for the mean, add 1 to start at 1
	Window = 4
	# Define a temporary average value
	WT = 0
	# Define size of actual window, will be odd number
	Size = Window-1
	# # Define max limit for the analysis, the max index to run to
	MaxV = (Lenght)-((Size-1)/2)
	# Define the minimum value to start the analysis
	MinV = ((Size-1)/2)
	# Define center value of window
	ModVars = []
	for c in range(1, Window):
		ModVars.append(c)
	CenterV = np.median(ModVars)
	# Define years centered at each average
	Years = []
	# Define averages for SI
	SIave = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in SIdMod:
		if aItem[-1]>MinV and aItem[-1]<MaxV:
			# Write the indexes for all neighboring data for average calc
			TempI = []
			for z in range(1, Window):
				# This value will represent the modifying variables
				IndexByz = int(z-CenterV)
				# The index on the list item will modified to write a list of 
				# index values equal to its neighboring data sets
				TempI.append(IndexByz+aItem[-1])
			# Filter by each index value selected
			for Index in TempI:
				for Mod in SIdMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			SIave.append(WT/Size)
			WT = 0

	# Define central years for each average
	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# Plot our average seasonality index

	SeasonalityIndex = np.array(SIave)
	xi = np.array(Years)
	mask = ~np.isnan(xi) & ~np.isnan(SeasonalityIndex)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.grid(True)
	ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
	    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	    fontweight=None, color='black')
	fig.subplots_adjust(top=0.85)
	ax.set_xlabel(YearLabel)
	ax.set_ylabel('Seasonality Index')
	ax.set_title('Mean Seasonality Index(%i Year Average)' % (Size), fontweight='bold')
	plt.plot(xi,SeasonalityIndex,  '-')
	slope, intercept, r_value, p_value, std_err = stats.linregress(xi[mask], SeasonalityIndex[mask])
	plt.plot(xi,intercept+slope*xi, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s%s_Year_Mean_SI.%s' % (Output, str(Size), f))
	# plt.show()
	plt.close()



















	# Belongs in sep module

	# ###################################### Running mean EE

	# # Define the lenght of the data set
	# Lenght =  len(EE)
	# # print Lenght
	# # print SIdMod
	# # sys.exit()

	# # Define the window size for the mean, add 1 to start at 1
	# Window = 4
	# # Define a temporary average value
	# WT = 0
	# # Define size of actual window, will be odd number
	# Size = Window-1
	# # # Define max limit for the analysis, the max index to run to
	# MaxV = (Lenght)-((Size-1)/2)
	# # Define the minimum value to start the analysis
	# MinV = ((Size-1)/2)
	# # Define center value of window
	# ModVars = []
	# for c in range(1, Window):
	# 	ModVars.append(c)
	# CenterV = np.median(ModVars)
	# # Define years centered at each average
	# Years = []
	# # Define averages for SI
	# EEave = []
	# # print CenterV
	# # # Define a list of indexes for the analysis to go off of

	# for aItem in EE:
	# 	if aItem[0]>MinV and aItem[0]<MaxV:
	# 		# Write the indexes for all neighboring data for average calc
	# 		TempI = []
	# 		for z in range(1, Window):
	# 			# This value will represent the modifying variables
	# 			IndexByz = int(z-CenterV)
	# 			# The index on the list item will modified to write a list of 
	# 			# index values equal to its neighboring data sets
	# 			TempI.append(IndexByz+aItem[0])
	# 		# Filter by each index value selected
	# 		for Index in TempI:
	# 			for Mod in EE:
	# 				if Mod[0]==Index:
	# 					WT = WT+Mod[-1]
	# 		Years.append(aItem[0])
	# 		EEave.append(WT/Size)
	# 		# if WT!=0:
	# 		# 	EEave.append(WT/Size)
	# 		# if WT==0:
	# 		# 	EEave.append(0)
	# 		WT = 0

	# # Plot our average seasonality index

	# EEmod = np.array(EEave)
	# x = np.array(Years)
	# mask = ~np.isnan(x) & ~np.isnan(EEmod)
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.grid(True)
	# ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
	#     horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	#     fontweight=None, color='black')
	# fig.subplots_adjust(top=0.85)
	# ax.set_xlabel(YearLabel)
	# ax.set_ylabel('Extreme Snowfall Events')
	# ax.set_title('Mean Extreme Snowfall Events (%i Year Average)' % (Size), fontweight='bold')
	# plt.plot(x,EEmod,  'ro')
	# # slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], SeasonalityIndex[mask])
	# # plt.plot(x,intercept+slope*x, 'r')
	# # ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	# #     (slope, p_value, r_value), verticalalignment='bottom', 
	# #     horizontalalignment='right', transform=ax.transAxes, fontsize=8)

	# # plt.show()
	# plt.close()

	# ############################### Plot SI with EE

	# EEmod = np.array(EEave)
	# x = np.array(Years)
	# mask = ~np.isnan(x) & ~np.isnan(EEmod)
	# fig, ax1 = plt.subplots()
	# # ax1 = fig.add_subplot(111)
	# ax1.grid(True)
	# ax1.text(.5, 1.15, 'Station: %s' % (StationName), verticalalignment='center', 
	#     horizontalalignment='center', transform=ax.transAxes, fontsize=12,
	#     fontweight=None, color='black')
	# # fig.subplots_adjust(top=0.85)
	# ax1.set_xlabel(YearLabel)
	# ax1.set_ylabel('Extreme Snowfall Events (Averaged)')
	# ax1.set_title('SE Events and SI Values (%i Year Average)' % (Size), fontweight='bold')
	# ax1.plot(x,EEmod,  linestyle= '-', color = 'blue')
	# ax1.tick_params(axis='y', labelcolor='blue')

	# ax2 = ax1.twinx()
	# ax2.set_ylabel('Seasonality Index (Averaged)')
	# ax2.tick_params(axis='y', labelcolor='black')

	# ax2.plot(xi,SeasonalityIndex,  linestyle= '-', color = 'black')

	# # slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], SeasonalityIndex[mask])
	# # plt.plot(x,intercept+slope*x, 'r')
	# # ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	# #     (slope, p_value, r_value), verticalalignment='bottom', 
	# #     horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	# plt.savefig('%s%s_Year_Mean_SI_SnowfallEE.%s' % (Output, str(Size), f))
	# plt.show()
	# # plt.close()

	# # Format: RAWDATA [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
	# # Format: STANDARDSNOW [Annual Snowfall, Snow Days, Daily Ave, Start D, End D, Season Length]


	################################### Annual probabilty 

	#################### SHUT OFF NOT SURE IF NEEDED

	# AnnualSum as previously written above is the annual totals
	# AnnualDate are the years associated with data

	# df = pd.DataFrame({"Sum Of Rainfall" : AnnualSum, "Date" : AnnualDate})
	# df = df.replace(0, np.nan)
	# df = df.sort_values(['Sum Of Rainfall'])
	# df = df.dropna(how='any')

	# Data = df.values.tolist()

	# x = []
	# for aRow in Data:
	# 	x.append(aRow[-1])

	# Bin = collections.Counter(x)
	# bins = Bin.keys()
	# n = len(Data)
	# data = np.array(x)
	# STD = np.nanstd(data)
	# Av = np.nanmean(data)

	# # print np.percentile(data, 99)
	# mu, sigma = Av, STD

	# # # Create the bins and histogram
	# # count, bins, ignored = plt.hist(data, 20, normed=True)

	# # # Plot the distribution curve
	# # plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
	# # 	np.exp( - (bins - mu)**2 / (2 * sigma**2) ),       linewidth=3, color='y')
	# # plt.show()


	# # best fit of data
	# (mu, sigma) = norm.fit(data)



	# # the histogram of the data
	# n, bins, patches = plt.hist(data, len(bins)-1, normed=1, facecolor='green', alpha=0.75, label='Rainfall PDF')
	# # add a 'best fit' line
	# y = mlab.normpdf(data, mu, sigma)
	# l = plt.plot(bins, y, 'r--', linewidth=2, label='Fit')

	# #plot
	# plt.xlabel('Rainfall')
	# plt.ylabel('Probability')
	# plt.title('Histogram of Rainfall Events 30 Years\n Average: %i     STD: %i' %(round(mu, 6), round(sigma, 6)))
	# plt.legend()
	# plt.grid(True)

	# plt.show()



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

