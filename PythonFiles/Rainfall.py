from BasicImports import *

def Rainfall(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData):
	# Format: RAWDATA [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
	# Format: STANDARDSNOW [Annual Snowfall, Snow Days, Daily Ave, Start D, End D, Season Length]
	# 3 is precip

	dir = 'Output/'+StationName+'/Rainfall'
	if not os.path.exists(dir):
		os.makedirs('Output/'+StationName+'/Rainfall')
	else:
		shutil.rmtree(dir)
		os.makedirs(dir)

	Output = 'Output/'+StationName+'/Rainfall/'

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
			if aRow[2]!=im:
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
	ax.set_title('Total Annual Rainfall')
	ax.set_xlabel('Year')
	ax.set_ylabel('Total Rainfall (mm)')
	# ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
	ax.set_yticks([0.9], minor=True)
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/Annual_Rainfall.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)


	###################################### Running mean Annual Rainfall 3
	# Format: RAWDATA [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
	# Format: STANDARDSNOW [Annual Snowfall, Snow Days, Daily Ave, Start D, End D, Season Length]

	# This section will calculate the SI based upon 3 year averages to smooth out the
	# data. As expressed in pg 182 Terrestrial Hydrometerology W. James Shuttleworth
	# as a running means SI.

	# Define the index values (years) and place them into the data records
	RainMod = []
	i = 0
	for aItem in AnnualRainfall:
		RainMod.append([aItem, i])
		i = i+1

	# Define the lenght of the data set
	Lenght =  len(RainMod)
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Rainfall Total (mm)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('3 Year Rainfall Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Rainfall (mm)')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/3_YearAve_Annual_Rainfall.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)

	###################################### Running mean Annual Rainfall 6
	# Define the index values (years) and place them into the data records
	RainMod = []
	i = 0
	for aItem in AnnualRainfall:
		RainMod.append([aItem, i])
		i = i+1

	# Define the lenght of the data set
	Lenght =  len(RainMod)
	# print Lenght
	# print SIdMod
	# sys.exit()

	# Define the window size for the mean, add 1 to start at 1
	Window = 6
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Rainfall Total (mm)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('5 Year Rainfall Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Rainfall (mm)')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/5_YearAve_Annual_Rainfall.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)

###################################### Running mean Annual Rainfall 10
	# Define the window size for the mean, add 1 to start at 1
	Window = 10
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Rainfall Total (mm)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('9 Year Rainfall Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Rainfall (mm)')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/9_YearAve_Annual_Rainfall.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)


	################################ Rainfall Extremes

   #*********************************Extreme Events CDF******************************

	# Write a snowfall *VALUE* only list.
	x = []
	for aRow in BaseData:
		if aRow[3]!=0.0 and np.isnan(aRow[3]) != True:
			x.append(aRow[3])
	# Count the frequency of variables and
	# identify all variables in the set.
	counter=collections.Counter(x)
	# The rv_discrete function requires unique values.
	# This provides the values to fulfill the arguments.
	F = copy.deepcopy(counter.values())
	Fsum = sum(F)
	Frequency = []
	for aRow in F:
		x = float(aRow)
		temp = x/Fsum
		Frequency.append(temp)

	# Sum of Frequency is now 1. This is required for the rv_discrete function.
	# This discrete function provides a start and end value for the CDF.
	# This ensures that the highest value in a dataset is given the value of
	# 1. Meaning %100 of the records are below the highest recorded amount. 

	Variables = copy.deepcopy(counter.keys())

	CDF = scipy.stats.rv_discrete(values=(Variables, Frequency))
	CDF = CDF.cdf(Variables)
	# x is snowfall amount
	x = sorted(Variables)
	# y is CDF values for each variable
	y = sorted(CDF)

	## This section is the reverse emperical
	## y2 is the reverse emperical line.
	# y2 = []
	# for aRow in y:
	#     V = 1 - aRow
	#     y2.append(V)
	#     V = 0

	fig, ax = plt.subplots(1, 1)
	ax.grid(True)
	#SE is pre-defined variable representing CDF limit
	ax.text(-0.01, 0.93, '%s' % ('0.98'), verticalalignment='top', 
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
	ax.set_yticks([0.98], minor=True)
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	plt.savefig('%s/CDF_Rainfall.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	# sys.exit()
	#****************************Identify rainfall minimum CDF***********

	# ExtremeEventsCDF is a list of extreme events per year.
	ExtremeEventsCDF = []
	# i is the index counting the location of the first sig record in y.
	# y is given in the function above as CDF values (y-axis) for the graph.
	i = 0
	#SE is pre-defined variable representing CDF limit
	for aRow in y:
		if aRow < 0.98:
			i = i+1
		if aRow >= 0.98:
			ExtremeEventsCDF.append(aRow)
	#******************Identify Extreme Rainfall Events********************

	# ExtremeEventsRF is a list of Rain values meeting the CDF threshold.
	ExtremeEventsRF = []
	ExtremeEventsRF = copy.deepcopy(x[i::])
	# ValueMinS is the snowfall value which represents the percentile of SE.
	# SE is defined at the start of the program.
	ValueMinS = copy.deepcopy(ExtremeEventsRF[0])
	#****************************Count extreme events per year

	#ExtremeEventsPerYearCDF is list for counting extreme events per year.
	# They are defined as greater than or equal to ValueMinS.
	ExtremeEventsPerYearCDF = []
	# Counting variable for events per year.
	numbevents = 0
	# Index for guiding study year
	i = 0
	# Count of records passed to be used in breaking the loop at last record.
	records = 0
	# Write a list of Study years
	StudyYearList = []
	Temp = []
	for aRow in BaseData:
		Temp.append(aRow[0])
	StudyYearList = collections.Counter(Temp).keys()

	for aRow in BaseData:
		records = records+1
		if aRow[0]==StudyYearList[i]:
			if aRow[3] >= ValueMinS and np.isnan(aRow[3]) != True:
				numbevents = numbevents+1
		if aRow[0]!=StudyYearList[i]:
			if aRow[0]==StudyYearList[i+1]:
				ExtremeEventsPerYearCDF.append(numbevents)
				numbevents = 0
				i = i+1
				if aRow[-5] >= ValueMinS:
					numbevents = numbevents+1
		if records == len(BaseData):
			ExtremeEventsPerYearCDF.append(numbevents)
			numbevents = 0
			i = i+1
			if aRow[3] >= ValueMinS:
				numbevents = numbevents+1

	x = np.array(StudyYearList)
	# Annual extreme precipitation events
	EED = []
	for aItem in ExtremeEventsPerYearCDF:
		EED.append(aItem)
	ExtremeEventsPerYearCDF = np.array(ExtremeEventsPerYearCDF)
	mask = ~np.isnan(x) & ~np.isnan(ExtremeEventsPerYearCDF)

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.grid(True)
	ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
		horizontalalignment='center', transform=ax.transAxes, fontsize=12,
		fontweight=None, color='black')
	fig.subplots_adjust(top=0.85)
	ax.set_xlabel(YearLabel)
	ax.set_ylabel('Days of Extreme Events (CDF>=%s)' % ('0.98'))
	ax.set_title('Extreme Rainfall Events Per Year', fontweight='bold')
	plt.plot(x,ExtremeEventsPerYearCDF,  '-')
	slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],ExtremeEventsPerYearCDF[mask])
	plt.plot(x,intercept+slope*x, 'r')
	ax.text(0.95, 0.008, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' 
		% (slope, p_value, r_value), verticalalignment='bottom', 
		horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/Annual_Extreme_Events.%s' % (dir, f), dpi=None, 
		facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
		format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
		frameon=None)
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)
	# plt.show()
	plt.close()



	###################################### Running mean Annual Rainfall EE 3
	# Define the index values (years) and place them into the data records
	RainMod = []
	i = 0
	for aItem in EED:
		RainMod.append([aItem, i])
		i = i+1

	# Define the lenght of the data set
	Lenght =  len(RainMod)
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Extreme Events (CDF>=0.98)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('3 Year Extreme Events Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Evetns')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/3_YearAve_ExtremeEvetns.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)

###################################### Running mean Annual Rainfall EE 5
	# Define the window size for the mean, add 1 to start at 1
	Window = 6
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Extreme Events (CDF>=0.98)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('5 Year Extreme Events Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Evetns')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/5_YearAve_ExtremeEvetns.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)
###################################### Running mean Annual Rainfall EE 9
	# Define the window size for the mean, add 1 to start at 1
	Window = 10
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
	RainAve = []
	# print CenterV
	# # Define a list of indexes for the analysis to go off of

	for aItem in RainMod:
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
				for Mod in RainMod:
					if Mod[-1]==Index:
						WT = WT+Mod[0]
			RainAve.append(WT/Size)
			WT = 0

	EndMod = int(Size/2)
	for x in range(BaseData[0][0]+EndMod, BaseData[-1][0]-EndMod):
		Years.append(x)

	# print RainAve

	fig, ax = plt.subplots(1, 1)
	Years = np.array(Years)
	S = np.array(RainAve)
	mask = ~np.isnan(Years) & ~np.isnan(S)
	ax.grid(True)
	ax.plot(Years, S, label='Extreme Events (CDF>=0.98)')
	# ax.plot(x, y2, label='Reversed emp.')
	ax.legend(loc='upper right')
	ax.set_title('9 Year Extreme Events Averages')
	ax.set_xlabel('Central Year')
	ax.set_ylabel('Evetns')
	# ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
	ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
	slope, intercept, r_value, p_value, std_err = stats.linregress(Years[mask], S[mask])
	plt.plot(Years,intercept+slope*Years, 'r')
	ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
	    (slope, p_value, r_value), verticalalignment='bottom', 
	    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
	plt.savefig('%s/9_YearAve_ExtremeEvetns.%s' % (Output, f), 
		dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
		papertype=None, format=None, transparent=False, bbox_inches=None, 
		pad_inches=0.1, frameon=None)
	# plt.show()
	plt.close()
	StationExports.append(slope)
	StationExports.append(p_value)
	StationExports.append(r_value)
	