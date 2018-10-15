from BasicImports import *

def SnowFallAnalysis(StationName, SnowData, RawData, SE, f, StationExports, Dayx, MonthX):
    dir = 'Output/'+StationName+'/Snowfall'
    if not os.path.exists(dir):
        os.makedirs('Output/'+StationName+'/Snowfall')
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)
    #*****************************************Snow only index****************
    #Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
    # The imported list contains no blank ("") snow records. 
    allData = copy.deepcopy(SnowData)
    #*********************************COUNT SNOWDAYS AND TOTAL****************

    # These values can be used to compare the sum of parsed data
    # this will ensure no records were lost.
    TotalnumbSnowDays = 0
    TotalSnow = 0
    for aRow in allData:
        if aRow[-5] != 0.0 and np.isnan(aRow[-5]) != True:
            TotalnumbSnowDays=TotalnumbSnowDays+1
            TotalSnow = TotalSnow+aRow[-5]

    # print ("The total number of snow days is: %i" %(TotalnumbSnowDays))
    # print ("The total snow for study period is: %i" %(TotalSnow))

    #*************************Annual snowdays (Hydro Year)************************

    # DataCheck: If value is 1, that represents one period with missing records.
    # Values only represent number of times records skip, not the number of 
    # years skipped.

    DataCheck = 0
    # j is the hydro year variable
    j = allData[0][-1]
    # jin is the index for each year to be placed. It will place j in the data set
    # for each record in that year. Then the stats for records per year can be calculated.
    jin = []
    for aRow in allData:
        prevRow = aRow
        jin.append(j)
        if aRow[-1]==j: 
            pass
        if aRow[-1]==j+1:
            j = j+1
        if aRow[-1]>j+1:
            j = aRow[-1]
            DataCheck = 0
    # Function to count snowfall records <0 per year.
    # It lists the hydro year for each record. The total times the hydro
    # year occurs in the dataset (values), is equal to the total snowdays
    # per year. Keys values then provide which years were counted.
    Count = collections.Counter(jin)
    StudyYearList = copy.deepcopy(Count.keys())
    snowDays = copy.deepcopy(Count.values())

    # Check sum to ensure no skipped records
    TotalSDcheck = sum(snowDays)
    if TotalSDcheck-TotalnumbSnowDays!=0:
        temp = TotalSDcheck-TotalnumbSnowDays
        print (" \n******Annual Snowday Miscalculation by a value of %i******\n " % (temp))
    #**********************************Yearly Snow Totals****************
    # Record reset at change of each hydro year. Used to count totals per year.
    TotalAnSnowfall = 0
    # List each annual total will be appended to.
    AnnualSnowFall = []
    # First hdyro year date in snowfall only set
    j = allData[0][-1]
    for aRow in allData:
        if j == aRow[-1]:
            TotalAnSnowfall=TotalAnSnowfall+aRow[-5]
        if aRow[-1]==j+1:
            AnnualSnowFall.append(TotalAnSnowfall)
            j = j+1
            TotalAnSnowfall = 0
            TotalAnSnowfall=aRow[-5]
        if aRow[-1]>j+1:
            j = aRow[-1]
            AnnualSnowFall.append(TotalAnSnowfall)
            TotalAnSnowfall = 0
            TotalAnSnowfall=aRow[-5]        
    AnnualSnowFall.append(TotalAnSnowfall)

    # Check sum to ensure no skipped records
    TotalSFcheck = sum(AnnualSnowFall)
    if TotalSFcheck-TotalSnow!=0:
        temp = TotalSFcheck-TotalSnow
        print (" \n******Annual Snow Totals Miscalculation by a value of %i******\n " % (temp))

    #*********************************#Calculate Daily Averages Per Year*************
    YSFarray=np.array(AnnualSnowFall, dtype=np.float) #Defines an array of AnnualSnowFall data
    SDarray=np.array(snowDays, dtype=np.float) #Defines an array of snowDays data
    DailyAverage=np.array([YSFarray/SDarray], dtype=np.float) #Daily average for a given year

    #*****************************Entire Study Period Standard Deviations*************
    TotalDailyAveS=np.nanmean(DailyAverage, dtype=np.float) #Calculates daily average of entire period.
    StandardDevDA = np.nanstd(DailyAverage, dtype=np.float) #Calcualtes std of total study period daily snowfall averages
    #*****************************Annual Standard Deviation**************************
    # List to append the standard deviation for daily snowfall per year
    AnnualStandardDev = []
    # Temp list to count snow amounts and run
    YearlySnowTemporary = []
    # First hdyro year date in snowfall only set
    i=allData[0][-1]
    # Count the std records equal to 0.
    count = 0
    # TempData is a set for full record data. Used to extract start and end dates.
    TempData = []
    # StartDates is a list containing records for first snowfall in a snow season.
    StartDates = []
    # EndDates is a list for records for final records in a snow season.
    EndDates = []
    # PrevRow is to assist loop function for start and end dates.
    prevRow = []
    # TempVar is a date conversion variable for Start and End Dates.
    TempVar = []

    for aRow in allData:
        if aRow[-1]==i:
            YearlySnowTemporary.append(aRow[-5])
            TempData.append(aRow)
        if aRow==allData[-1]:
            YearlySnowTemporary.append(aRow[-5])
            TempVar = TempData[0][0:3]
            TempVar = str(TempVar)
            TempVar = TempVar.replace(", ", "/")
            TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
            StartDates.append(TempVar)
            TempVar = TempData[-1][0:3]
            TempVar = str(TempVar)
            TempVar = TempVar.replace(", ", "/")
            TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
            EndDates.append(TempVar)
            x = np.nanstd(YearlySnowTemporary, dtype=np.float)
            if x==0:
                count = count+1
            AnnualStandardDev.append(x)
            TempData = []   
        if aRow[-1]!=i:
            x = np.nanstd(YearlySnowTemporary, dtype=np.float)
            if x==0:
                count = count+1
                if len(YearlySnowTemporary)==1:
                    TempVar = prevRow[0:3]
                    TempVar = str(TempVar)
                    TempVar = TempVar.replace(", ", "/")
                    TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                    StartDates.append(TempVar)
                    TempVar = prevRow[0:3]
                    TempVar = str(TempVar)
                    TempVar = TempVar.replace(", ", "/")
                    TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                    EndDates.append(TempVar)
                if len(YearlySnowTemporary)>1:
                    TempVar = TempData[0][0:3]
                    TempVar = str(TempVar)
                    TempVar = TempVar.replace(", ", "/")
                    TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                    StartDates.append(TempVar)
                    TempVar = TempData[-1][0:3]
                    TempVar = str(TempVar)
                    TempVar = TempVar.replace(", ", "/")
                    TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                    EndDates.append(TempVar)
            if x!=0:
                TempVar = TempData[0][0:3]
                TempVar = str(TempVar)
                TempVar = TempVar.replace(", ", "/")
                TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                StartDates.append(TempVar)
                TempVar = TempData[-1][0:3]
                TempVar = str(TempVar)
                TempVar = TempVar.replace(", ", "/")
                TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                EndDates.append(TempVar)       
            AnnualStandardDev.append(x)
            YearlySnowTemporary = []
            x=[]
            i=aRow[-1]
            YearlySnowTemporary.append(aRow[-5])
            TempData = []
            TempData.append(aRow)
            prevRow = aRow
    # if count>0:
        # print (" \n******%i Annual Standard Deviation Records With Value of Zero****** \n " % (count))
    if len(StartDates)-len(EndDates)!=0:
        print (" \n******Error Defining Start and End Dates for Snow Season****** \n")

    #*****************************Calculate Season Length****************************

    # List for season length (in days) to be appended to.
    SeasonLen = []
    # Index for while loop.
    i = 0
    # Variable for calculations.
    TempVar = 0
    while i<len(StartDates):
        TempVar = EndDates[i]-StartDates[i]
        TempVar = TempVar.days+1
        SeasonLen.append(TempVar)
        i = i+1
    if len(SeasonLen)!=len(StartDates):
        print (" \n******Error Calculating Snow Season Length****** \n")

    #*********************************Season End and Start********
    # Replace years to allow for simple subtraction. The years
    # shown here, from 1999-2000, represent a leap year. This 
    # will allow for the calculation of start or end date from year start
    # for all years, mostly in place incase the first or final day is
    # occuring on the final day of Feburary during a leap year. 
    TheDate = ('%s/%s/1999' % (Dayx, MonthX))
    Day1 = datetime.strptime(TheDate, '%d/%m/%Y')

    Diff = 0

    DayStart = []
    DayEnd = []

    for aRow in EndDates:
        String = str(aRow)
        Date = String[0:10]
        Year = Date[0:4]
        TempVar = int(Date[-5:-3])
        if TempVar>=MonthX:
            Date = Date.replace(Year, "1999")
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Diff = Date-Day1
            Diff = Diff.days
            DayEnd.append(Diff)
        if TempVar<=MonthX-1:
            Date = Date.replace(Year, "2000")
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Diff = Date-Day1
            Diff = Diff.days
            DayEnd.append(Diff)

    for aRow in StartDates:
        String = str(aRow)
        Date = String[0:10]
        Year = Date[0:4]
        TempVar = int(Date[-5:-3])
        if TempVar>=MonthX:
            Date = Date.replace(Year, "1999")
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Diff = Date-Day1
            Diff = Diff.days
            DayStart.append(Diff)
        if TempVar<=MonthX-1:
            Date = Date.replace(Year, "2000")
            Date = datetime.strptime(Date, '%Y-%m-%d')
            Diff = Date-Day1
            Diff = Diff.days
            DayStart.append(Diff)

    if len(DayStart)!=len(DayEnd):
        print (" \n******Error Calculating Snow Start and End Positions****** \n")

    #*********************************Extreme Events CDF******************************

    # Write a snowfall *VALUE* only list.
    x = []
    for aRow in allData:
        x.append(aRow[-5])
    SnowData = copy.deepcopy(x)
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
    ax.text(-0.01, 0.93, '%s' % (SE), verticalalignment='top', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=9,
        fontweight='bold', color='r')
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    ax.plot(x, y, label='CDF')
    # ax.plot(x, y2, label='Reversed emp.')
    ax.legend(loc='right')
    ax.set_title('Cumulative Distrbution of Snowfall')
    ax.set_xlabel('Daily Snowfall (mm)')
    ax.set_ylabel('CDF Value')
    # ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1], minor=False)
    ax.set_yticks([SE], minor=True)
    # ax.yaxis.grid(True, which='major', color='g', linewidth=0.5)
    ax.yaxis.grid(True, which='minor', color='r', linewidth=1.25)
    plt.savefig('%s/CDF_Snowfall.%s' % (dir, f), 
        dpi=None, facecolor='w', edgecolor='b', orientation='portrait', 
        papertype=None, format=None, transparent=False, bbox_inches=None, 
        pad_inches=0.1, frameon=None)
    # plt.show()
    plt.close()
    #****************************Identify snowfall minimum CDF***********

    # ExtremeEventsCDF is a list of extreme events per year.
    ExtremeEventsCDF = []
    # ExtremeEventsSF is a list of snow values meeting the CDF threshold.
    ExtremeEventsSF = []
    # i is the index counting the location of the first sig record in y.
    # y is given in the function above as CDF values (y-axis) for the graph.
    i = 0
    #SE is pre-defined variable representing CDF limit
    for aRow in y:
        if aRow < SE:
            i = i+1
        if aRow >= SE:
            ExtremeEventsCDF.append(aRow)
    #******************Identify Extreme Snowfall Events********************

    # ExtremeEventsSF is a list of snow values meeting the CDF threshold.
    ExtremeEventsSF = []
    ExtremeEventsSF = copy.deepcopy(x[i::])
    # ValueMinS is the snowfall value which represents the percentile of SE.
    # SE is defined at the start of the program.
    ValueMinS = copy.deepcopy(ExtremeEventsSF[0])
    #
    StationExports.append(ValueMinS)
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

    for aRow in allData:
        records = records+1
        if aRow[-1]==StudyYearList[i]:
            if aRow[-5] >= ValueMinS:
                numbevents = numbevents+1
        if aRow[-1]!=StudyYearList[i]:
            if aRow[-1]==StudyYearList[i+1]:
                ExtremeEventsPerYearCDF.append(numbevents)
                numbevents = 0
                i = i+1
                # print i
                if aRow[-5] >= ValueMinS:
                    numbevents = numbevents+1
        if records == len(allData):
            ExtremeEventsPerYearCDF.append(numbevents)
            numbevents = 0
            i = i+1
            if aRow[-5] >= ValueMinS:
                numbevents = numbevents+1

    #******************************Fill in mising hydro years********

    # Defines first hydro year in RawData. If no snowfall data is found in 
    # first year, this must be defined to fill missing years.
    FirstY = RawData[0][-1]
    # Defines last hydro year in RawData. If no snowfall data is found in 
    # last year, this must be defined to fill missing years.
    FinalY = RawData[-1][-1]
    # List of years with data gaps filled. Used to complete x-axis for graphing.
    AllYears = []
    # Index counting year value for loop cycle.
    i = 0
    while i<FinalY:
        AllYears.append(FirstY)
        FirstY = FirstY+1
        i = i+1
    # Write a list of missing years
    MissingHydroY = []
    # Write an index where these values are located within full year list.
    # This allows for the insertion of nan values at those locations.
    MissingHydroIndex = []
    # Defines the years not found in both sets (Missing records).
    diff = set(AllYears)-set(StudyYearList)
    MissYearCount = len(diff)
    MissingHydroY = sorted(diff)
    MissingHydroIndex= []
    for aRow in MissingHydroY:
        temp = aRow-1
        MissingHydroIndex.append(temp)
    #***********************************Insert NaN values***********

    YSFarray = YSFarray.tolist()
    SDarray = SDarray.tolist()
    for aRow in MissingHydroIndex:
        temp = np.nan
        SDarray.insert(aRow, temp)
        YSFarray.insert(aRow, temp)
        ExtremeEventsPerYearCDF.insert(aRow, temp)
        AnnualStandardDev.insert(aRow, temp)
        SeasonLen.insert(aRow, temp)
        DayStart.insert(aRow, temp)
        DayEnd.insert(aRow, temp)

    DayStart = np.array(DayStart)

    DayEnd = np.array(DayEnd)

    SDarray = np.array(SDarray)

    YSFarray = np.array(YSFarray)

    DailyAverage=np.array([YSFarray/SDarray], dtype=np.float)

    ExtremeEventsPerYearCDF = np.array(ExtremeEventsPerYearCDF)

    AnnualStandardDev = np.array(AnnualStandardDev)

    SeasonLen = np.array(SeasonLen)

    x = np.array(AllYears)

    ##********************************Start Dates
    mask = ~np.isnan(x) & ~np.isnan(DayStart)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Year')
    ax.set_ylabel('Days From Year Start MM/DD: %s/%s' % (MonthX, Dayx))
    ax.set_title('Days From Year Start to First Snow Event', fontweight='bold')
    plt.plot(x,DayStart,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],DayStart[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.008, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' 
        % (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/SnowSeasonStart.%s' % (dir, f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##********************************End Dates
    # MEET AND DISCUSS
    # MEET AND DISCUSS
    # MEET AND DISCUSS
    mask = ~np.isnan(x) & ~np.isnan(DayEnd)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Year')
    ax.set_ylabel('Days From Year Start MM/DD: %s/%s' % (MonthX, Dayx))
    ax.set_title('Days From Year Start to Final Snow Event', fontweight='bold')
    plt.plot(x,DayEnd,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],DayEnd[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.008, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' 
        % (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/SnowSeasonEnd.%s' % (dir, f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##********************* Snow Season Length
    mask = ~np.isnan(x) & ~np.isnan(SeasonLen)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Hydro Year')
    ax.set_ylabel('Days')
    ax.set_title('Length of Snow Seasons', fontweight='bold')
    plt.plot(x,SeasonLen,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],SeasonLen[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.008, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' 
        % (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)

    plt.savefig('%s/SnowSeasonLen.%s' % (dir, f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    ##********************* Extreme Snow Events CDF
    mask = ~np.isnan(x) & ~np.isnan(ExtremeEventsPerYearCDF)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Hydro Year')
    ax.set_ylabel('Days of Extreme Events (CDF>%s)' % (SE))
    ax.set_title('Extreme Snowfall Events Per Year', fontweight='bold')
    plt.plot(x,ExtremeEventsPerYearCDF,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],ExtremeEventsPerYearCDF[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.008, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' 
        % (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/Extreme_Events.%s' % (dir, f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##*********************Snow Days
    mask = ~np.isnan(x) & ~np.isnan(SDarray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Hydro Year')
    ax.set_ylabel('Snow Days')
    ax.set_title('Total Annual Snowdays', fontweight='bold')
    plt.plot(x,SDarray,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],SDarray[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/Snow_Days_Annual.%s' % (dir, f))
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##****************Annual Snowfall
    mask = ~np.isnan(x) & ~np.isnan(YSFarray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Hydro Year')
    ax.set_ylabel('Annual Snowfall (mm)')
    ax.set_title('Annual Snowfall Totals (mm)', fontweight='bold')
    plt.plot(x,YSFarray,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],YSFarray[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/AnnualTotals_mm.%s' % (dir, f))
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##************** Standard Dev
    mask = ~np.isnan(x) & ~np.isnan(AnnualStandardDev)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Hydro Year')
    ax.set_ylabel('Sigma (mm)')
    ax.set_title('Annual Average of Daily Snowfall Standard Deviation', fontweight='bold')
    plt.plot(x,AnnualStandardDev,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], AnnualStandardDev[mask])
    plt.plot(x,intercept+slope*x, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/Annual_Average_Daily_STD.%s' % (dir, f))
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    # plt.show()
    plt.close()

    ###**************Additional Data Check****************
    ###**************Additional Data Check****************
    ###**************Additional Data Check****************

    StationExports.append(MissYearCount)


    # Data gap can mean no winter data was available or all records were 0.0.

    # if MissYearCount>0:
    #     os.makedirs(os.path.join(dir, 'ErrorData'))
    #     print ("*******************%i Data Gap(s) Identified******************" % (MissYearCount))
    #     print ("Years Missing: %s\n " % (MissingHydroY))


        # This section was used to output a graph for each year with
        # missing snowfall data. This is currently unavailable for 
        # this analysis.

        # Temp = []
        # ZeroSnowYears = []
        # x = 0
        # i = 0

        # for aRow in RawData:
        #     if aRow[-1]==MissingHydroY[x]: 
        #         Temp.append(aRow)
        #         # print prevRow
        #         if aRow==RawData[-1]:
        #             Temp.append(aRow)
        #             ZeroSnowYears.append(Temp)
        #             Temp = []
        #     if aRow[-1]!=MissingHydroY[x]:
        #         if x==len(MissingHydroY)-1:
        #             # If dataset has full final year, this is needed to break 
        #             # the loop partway through RawData.
        #             ZeroSnowYears.append(Temp)                        
        #             Temp = []
        #             break
        #         if aRow[-1]==MissingHydroY[x+1]:
        #             ZeroSnowYears.append(Temp)
        #             x = x+1                           
        #             Temp = []
        #             if x != len(MissingHydroY):
        #                 Temp.append(aRow)

        # ## All Data for no snowfall years parced in ZeroSnowYears

        # # x counts how many loops have occured
        # x = 0
        # # y defines the cutoff value for the loop
        # y = len(ZeroSnowYears)
        # # i is record index to define limit threshold to initiate graphing function
        # i = 0
        # # M is used to act as the Month variable
        # M = 0
        # # RY and LY represent regular and leap year. The values proceeding are days per month.
        # # Representing what 100% coverage per month would be.
        # MonthRY = [31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30]
        # MonthLY = [31, 30, 31, 31, 29, 31, 30, 31, 30, 31, 31, 30]
        # # Months per year in order of Hydro 
        # MonthsPerYear = [10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        # # Daycount counts days per month with recorded snow data (including 0.0)
        # Daycount = 0
        # # MonthX is used to represent which months are present (x-axis) in the dataset.
        # MonthX = []
        # # MonthY is used to represent how many days are present per month (y-axis) in the dataset.
        # MonthY = []

        # while x<y:
        #     for aRow in ZeroSnowYears[x]:
        #         # print ZeroSnowYears[x][0]
        #         Start = ZeroSnowYears[x][0][0:3]
        #         Start = str(Start)
        #         Start = Start.replace(", ", "/")
        #         Start = datetime.strptime(Start, '[%Y/%d/%m]')
        #         End = ZeroSnowYears[x][-1][0:3]
        #         End = str(End)
        #         End = End.replace(", ", "/")
        #         End = datetime.strptime(End, '[%Y/%d/%m]')
        #         delta = End-Start
        #         delta = delta.days + 1
        #         # print delta
        #         # print x
        #         if delta==365:
        #             # print "Norm"
        #             M = ZeroSnowYears[x][0][2]
        #             for aRow in ZeroSnowYears[x]:
        #                 i=i+1
        #                 if aRow[2]==M and aRow[4]!="":
        #                     Daycount = Daycount+1
        #                 if aRow[2]!=M and aRow[4]!="":
        #                     MonthX.append(M)
        #                     M = aRow[2]
        #                     MonthY.append(Daycount)
        #                     Daycount = 0
        #                 if i==len(ZeroSnowYears[x]):
        #                     MonthX.append(M)
        #                     M = aRow[2]
        #                     MonthY.append(Daycount)
        #                     Daycount = 0
        #                 if i==len(ZeroSnowYears[x]):
        #                     year = ZeroSnowYears[x][0][-1]
        #                     PercentRCov = float(sum(MonthY))/float(365)
        #                     plt.figure(figsize=(12,6))
        #                     plt.bar(MonthsPerYear, MonthRY, align='center', color='r', label='Missing Snowfall Records')
        #                     plt.bar(MonthX, MonthY, align='center', color='b', label='Coverage of Snowfall Records')
        #                     plt.xticks(MonthsPerYear)
        #                     plt.xlabel('Months')
        #                     plt.ylabel('Days of Coverage')
        #                     plt.title('Missing Snowfall Records Hydro Year %i' % (year))
        #                     plt.legend(loc='right')
        #                     plt.text(1, 32, 'Total Record Coverage For Study Period: %f' % 
        #                         (PercentRCov), verticalalignment='top') 
        #                     plt.savefig('%s/%s/MissingWinterDataYear%i.%s' % (dir,'ErrorData', year, f), dpi=None, 
        #                         facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        #                         format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        #                         frameon=None)
        #                     plt.close()
        #         if delta==366:
        #             # print "Leap"
        #             M = ZeroSnowYears[x][0][2]
        #             for aRow in ZeroSnowYears[x]:
        #                 i=i+1
        #                 if aRow[2]==M and aRow[4]!="":
        #                     Daycount = Daycount+1
        #                 if aRow[2]!=M and aRow[4]!="":
        #                     MonthX.append(M)
        #                     M = aRow[2]
        #                     MonthY.append(Daycount)
        #                     Daycount = 0
        #                 if i==len(ZeroSnowYears[x]):
        #                     MonthX.append(M)
        #                     M = aRow[2]
        #                     MonthY.append(Daycount)
        #                     Daycount = 0
        #                 if i==len(ZeroSnowYears[x]):
        #                     year = ZeroSnowYears[x][0][-1]
        #                     PercentRCov = float(sum(MonthY))/float(366)
        #                     plt.figure(figsize=(12,6))
        #                     plt.bar(MonthsPerYear, MonthLY, align='center', color='r', label='Missing Snowfall Records')
        #                     plt.bar(MonthX, MonthY, align='center', color='b', label='Coverage of Snowfall Records')
        #                     plt.xticks(MonthsPerYear)
        #                     plt.xlabel('Months')
        #                     plt.ylabel('Days of Coverage')
        #                     plt.title('Missing Snowfall Records Hydro Year %i' % (year))
        #                     plt.legend(loc='right')
        #                     plt.text(1, 32, 'Total Record Coverage For Study Period: %f' % 
        #                         (PercentRCov), verticalalignment='top') 
        #                     plt.savefig('%s/%s/MissingWinterDataYear%i.%s' % (dir,'ErrorData', year, f), dpi=None, 
        #                         facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        #                         format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        #                         frameon=None)
        #                     plt.close()
        #     Daycount = 0
        #     MonthX = []
        #     MonthY = []
        #     x = x+1
        #     i=0

    # print len(ZeroSnowYears)
    # print ("END of Snowfall Analysis")

########
# List of stuff for possible future use
# SDarray
# YSFarray
# ExtremeEventsPerYearCDF
# AnnualStandardDev
# SeasonLen
# DayStart
# DayEnd
# AllYears
# MissingHydroY
# MissingHydroIndex
# ExtremeEventsSF