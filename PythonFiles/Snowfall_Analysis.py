from BasicImports import *

def SnowFallAnalysis(StationName, SnowData, RawData, SE, f, StationExports, Dayx, MonthX, YearLabel):
    
    # This ignores all numpy errors. Used to ignore NaN errors.
    # Implemented since NaN values are used to fill empty data.
    np.warnings.filterwarnings('ignore')
    
    dir = 'Output/'+StationName+'/Snowfall'
    if not os.path.exists(dir):
        os.makedirs('Output/'+StationName+'/Snowfall')
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)
    #*****************************************Snow only index****************
    #Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
    # The imported list contains no blank ("") snow records. 
    allData = copy.deepcopy(RawData)
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

    #*************************Annual snowdays/snowfall/std************************

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
        if aRow[-5]>0.0 and np.isnan(aRow[-5]) != True:
            jin.append(aRow[-1])
    # Function to count snowfall records <0 per year.
    # It lists the hydro year for each record. The total times the hydro
    # year occurs in the dataset (values), is equal to the total snowdays
    # per year. Keys values then provide which years were counted.
    Count = collections.Counter(jin)
    StudyYearList = copy.deepcopy(Count.keys())
    snowDays = copy.deepcopy(Count.values())

    # Snowfall totals annual
    # Snowfall std annual
    # Annual Snowdays

    j = allData[0][-1]
    SnowT = []
    SnowY = []
    AnnualSnowFall = []
    AnnualSnowfallSTD = []
    SnowCount = 0
    SnowDays = []
    for aRow in allData:
        if aRow[-1]==j:
            if aRow[-5]!=0.0:
                SnowT.append(aRow[-5])
                if np.isnan(aRow[-5]) != True:
                    SnowCount = SnowCount+1
        if aRow[-1]!=j:
            SnowY.append(j)
            SnowT = np.array(SnowT)
            SnowDays.append(SnowCount)
            SnowCount = 0
            if np.nansum(SnowT)==0.0:
                AnnualSnowFall.append(np.sum(SnowT))
            if np.nansum(SnowT)!=0.0:
                AnnualSnowFall.append(np.nansum(SnowT))
            AnnualSnowfallSTD.append(np.nanstd(SnowT))
            SnowT = []
            j = j+1
            # Check row passing year transition
            if aRow[-5]!=0.0:
                SnowT.append(aRow[-5])
                if np.isnan(aRow[-5]) != True:
                    SnowCount = SnowCount+1

    SnowY.append(j)
    if np.nansum(SnowT)==0.0:
        AnnualSnowFall.append(np.sum(SnowT))
    if np.nansum(SnowT)!=0.0:
        AnnualSnowFall.append(np.nansum(SnowT))
    AnnualSnowfallSTD.append(np.nanstd(SnowT))      
    SnowDays.append(SnowCount)

    # Treat 0 snowfall years as NaN:
    i = 0
    Temp = []
    for aRow in SnowDays:
        if aRow==0:
            Temp.append(np.nan)
        if aRow!=0:
            Temp.append(aRow)
        i = i+1
    StudyYearList = SnowY

    SnowDays = copy.deepcopy(Temp)

    #*********************************#Calculate Daily Averages Per Year*************
    YSFarray=np.array(AnnualSnowFall, dtype=np.float) #Defines an array of AnnualSnowFall data
    SDarray=np.array(SnowDays, dtype=np.float) #Defines an array of snowDays data
    DailyAverage=np.array([YSFarray/SDarray], dtype=np.float) #Daily average for a given year

    #*****************************Entire Study Period Standard Deviations*************
    TotalDailyAveS=np.nanmean(DailyAverage, dtype=np.float) #Calculates daily average of entire period.
    StandardDevDA = np.nanstd(DailyAverage, dtype=np.float) #Calcualtes std of total study period daily snowfall averages
    #*****************************Start and End Dates**************************

    # END AND START DATES PER SEASON
    # print StartDates
    # print EndDates
    TempVar1 = 0
    TempVar2 = 0
    SnowRecords = []
    TempVar = 0
    i = 0
    j = allData[0][-1]
    c = 0
    StartDates = []
    EndDates = []
    MissingYears = []
    for aRow in allData:
        if aRow[-1]==j:
            if aRow[-5]!=0.0 and np.isnan(aRow[-5]) != True:
                SnowRecords.append(aRow)
        if aRow[-1]!=j:
            # Define prev year for missing year check
            prevYear = j
            j = aRow[-1]
            # If 2 dates pass, that will identify a start and end date.
            # This assumes it did not snow only once a year, or no days
            # at all. 
            if len(SnowRecords)>1:
                c = c+1
                TempVar = SnowRecords[0][0:3]
                TempVar = str(TempVar)
                TempVar = TempVar.replace(", ", "/")
                TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                StartDates.append(TempVar)
                TempVar = 0
                TempVar = SnowRecords[-1][0:3]
                TempVar = str(TempVar)
                TempVar = TempVar.replace(", ", "/")
                TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
                EndDates.append(TempVar)
            # Insert nan if 1 record or less is found. Assumes no 
            # winter experiences no snowfall or always at least 2 events.
            if len(SnowRecords)<=1:
                MissingYears.append(prevYear)
                StartDates.append(np.nan)
                EndDates.append(np.nan)

            SnowRecords = [] 
            if aRow[-5]!=0.0 and np.isnan(aRow[-5]) != True:
                SnowRecords.append(aRow)
    # Append final record once loop breaks
    if len(SnowRecords)>1:
        TempVar = SnowRecords[0][0:3]
        TempVar = str(TempVar)
        TempVar = TempVar.replace(", ", "/")
        TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
        StartDates.append(TempVar)
        TempVar = SnowRecords[-1][0:3]
        TempVar = str(TempVar)
        TempVar = TempVar.replace(", ", "/")
        TempVar = datetime.strptime(TempVar, '[%Y/%d/%m]')
        EndDates.append(TempVar)
    if len(SnowRecords)<=1:
        # Prev year not required for missing data check. If data
        # is missing here, the year is the final year.
        MissingYears.append(j)
        StartDates.append(np.nan)
        EndDates.append(np.nan)
    SnowRecords = [] 

    #*****************************Calculate Season Length****************************

    # List for season length (in days) to be appended to.
    SeasonLen = []
    # Index for while loop.
    i = 0
    # Variable for calculations.
    while i<len(StartDates):
        try:
            TempVar = (EndDates[i]-StartDates[i]).days
            TempVar = TempVar+1
            SnowSeasonLen.append(TempVar)
        except:
            if TempVar == 0:
                SeasonLen.append(np.nan)
        try:
            if TempVar>=365:
                SeasonLen.append(np.nan)
            if TempVar!=0:
                SeasonLen.append(TempVar)
        # This was written in to pass the error below:
        # File "PythonFiles\Snowfall_Analysis.py", line 209, in SnowFallAnalysis
        # if TempVar>=365:
        # TypeError: can't compare datetime.datetime to int
        #
        # This occured when an end date was not present, but a start date was.
        # Resulting in a single data which should be a nan value. It all
        # other try and excepts fail to this point, it will insert a nan value.
        except:
            SeasonLen.append(np.nan)
        TempVar = 0
        i = i+1

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
    # nan values were inserted where only one record was found.
    # The try and except loops allow to pass through these nan values.
    for aRow in EndDates:
        try:
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
        except:
            if np.isnan(aRow) == True:
                DayEnd.append(np.nan)

    for aRow in StartDates:
        try:
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
        except:
            if np.isnan(aRow) == True:
                DayStart.append(np.nan)

    if len(DayStart)!=len(DayEnd):
        print (" \n******Error Calculating Snow Start and End Positions****** \n")

    #*********************************Extreme Events CDF******************************

    # Write a snowfall *VALUE* only list.
    x = []
    for aRow in allData:
        if aRow[-5]!=0.0 and np.isnan(aRow[-5]) != True:
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
            if aRow[-5] >= ValueMinS and np.isnan(aRow[-5]) != True:
                numbevents = numbevents+1
        if aRow[-1]!=StudyYearList[i]:
            if aRow[-1]==StudyYearList[i+1]:
                ExtremeEventsPerYearCDF.append(numbevents)
                numbevents = 0
                i = i+1
                if aRow[-5] >= ValueMinS:
                    numbevents = numbevents+1
        if records == len(allData):
            ExtremeEventsPerYearCDF.append(numbevents)
            numbevents = 0
            i = i+1
            if aRow[-5] >= ValueMinS:
                numbevents = numbevents+1

    x = np.array(StudyYearList)
    DayStart = np.array(DayStart)
    ##********************************Start Dates
    mask = ~np.isnan(x) & ~np.isnan(DayStart)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
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
    DayEnd = np.array(DayEnd)
    mask = ~np.isnan(x) & ~np.isnan(DayEnd)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
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
    SeasonLen = np.array(SeasonLen)
    mask = ~np.isnan(x) & ~np.isnan(SeasonLen)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
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
    SDarray = np.array(SDarray)
    mask = ~np.isnan(x) & ~np.isnan(SDarray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
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
    YSFarray = np.array(YSFarray)
    mask = ~np.isnan(x) & ~np.isnan(YSFarray)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
    ax.set_ylabel('Annual Snowfall (mm)')
    ax.set_title('Annual Snowfall Totals (mm)', fontweight='bold')
    plt.plot(x,YSFarray,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask],YSFarray[mask])
    plt.plot(x,intercept+slope.T*x, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/AnnualTotals_mm.%s' % (dir, f))
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    ##************** Standard Dev
    AnnualSnowfallSTD = np.array(AnnualSnowfallSTD)
    mask = ~np.isnan(x) & ~np.isnan(AnnualSnowfallSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(YearLabel)
    ax.set_ylabel('STD (mm)')
    ax.set_title('Daily Snowfall Standard Deviation', fontweight='bold')
    plt.plot(x,AnnualSnowfallSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(x[mask], AnnualSnowfallSTD[mask])
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
    # MissingYears consists of years with less than 2 records of snowfall
    StationExports.append(len(MissingYears))


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