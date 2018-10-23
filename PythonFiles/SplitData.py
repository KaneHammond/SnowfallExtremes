from BasicImports import *
def Split_Data(Data, StationName, f, FirstYear, SnowData, RawData, BaseData, MonthX, DayX, StationExports, OmitYearsT, FinalYear):
    # This File processes raw data for analysis
    # by removing records without snowfall and 
    # defining hydrological years.
    dir = 'Output/'+StationName
    if not os.path.exists(dir):
        os.makedirs('Output/'+StationName)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)

    subfolder_names = ['Data_Coverage']
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(dir, subfolder_name))

    #Coverage Outputs
    OutputLoc = dir+'/'+subfolder_name+'/'
    #DATA FORMAT: [Date, Precip, Snow, Tmax, Tmin, TOBS]
    # This section does not remove any records. Only converts available data to float.
    allData = []
    for aRow in Data:
        splitDateInfo = aRow[0].split('-')
        for aItem in splitDateInfo:
            aRow.insert(0, int(aItem)) #this turns items in the list into integers (dd, mm, yyyy)
        del aRow[3] #deletes the original date info '12/27/1967'
    #Converts data to float
        if aRow[-1]!="":
            aRow[-1] = float (aRow[-1])
        if aRow[-2]!="":
            aRow[-2] = float (aRow[-2])
        if aRow[-3]!="":
            aRow[-3] = float (aRow[-3])
        if aRow[-4]!="":
            aRow[-4] = float (aRow[-4])
        if aRow[-5]!="":
            aRow[-5] = float (aRow[-5])
        allData.append(aRow)
    # Convert the parsed date data to a pandas dataframe to 
    # re-organize the date format to match initial program design
    df = pd.DataFrame(allData)
    df = df[[2, 0, 1, 3, 4, 5, 6, 7]]
    allData = df.values.tolist()
    # Convert the re-ordered date info back to int
    for aRow in allData:
        aRow[0] = int(aRow[0])
        aRow[1] = int(aRow[1])
        aRow[2] = int(aRow[2])

    # Keep base rcord data without year HY or Clip trim.
    # Still starts at study year from query.
    for aRow in allData:
        if aRow[0]>=FirstYear:
            if aRow[0]<=FinalYear:
                BaseData.append(aRow)
    #***************************************TRIM YEARS*********************
    #***************************************&HYDRO YEARS&*************************
    #*****Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS]
    # Defines the hydrological years (Starting in October ending last day of Sepetember)
    # Filter out dates only greater than or equal to defined year(from query)

    temp = []
    for aRow in allData:
        if aRow[0] >= FirstYear:
            temp.append(aRow)
    allData = []
    allData = copy.deepcopy(temp)
    temp = []
    hydroYear = 0                   
    prevMonth = 0
    prevYear = FirstYear
    for aRow in allData:
        if aRow[0]==prevYear or aRow[0]==prevYear+1:
            try:
                if aRow[2]==MonthX and aRow[1]==DayX:
                    hydroYear=hydroYear+1
            except:
                if prevMonth<=MonthX-1 and aRow[2]>=MonthX:
                    hydroYear=hydroYear+1
                if prevYear!=aRow[0]:
                    if aRow[0]!= prevYear+1:
                        hydroYear=hydroYear+1
                    elif prevMonth<=9:
                        hydroYear=hydroYear+1
            aRow.append(hydroYear)
            prevMonth=aRow[2]
            prevYear=aRow[0]
        if aRow[0]>=prevYear+2:
            x = aRow[0]-prevYear
            hydroYear = hydroYear+x
            prevYear = aRow[0]
            aRow.append(hydroYear)
            pass

    #**********TRIM HYDRO YEARS TO FULL ONES (Cut Final & First Year)#**********
    # This removes the first and last hydro years. This will trim incomplete
    # years providing the data download starts in January and ends in December.
    TempDataIndex = []
    # x is the final year of the analysis. Which in this case will be a partial year, as will the first year(0).
    x = allData[-1][-1]
    for aRow in allData:
        if aRow[:][-1]>0 and aRow[:][-1]<x:
            TempDataIndex.append(aRow)

    allData = []
    # Append method used here. copy.deepcopy resulted in blank index
    # after exported from definition
    # TESTING THIS REMOVES YEARS ON PURPOSE REMOVE FOR ANALYSIS 
    for aRow in TempDataIndex:
        RawData.append(aRow)
    # TempDataIndex = []
    # for aRow in RawData:
    #     if aRow[0]!=1956:
    #         TempDataIndex.append(aRow)
    # RawData = []
    # for aRow in TempDataIndex:
    #     RawData.append(aRow)
    # TempDataIndex = []
    # Remove partial years in middle of dataset.
    # Define the first Yearclip from dataset.

    YearClip = RawData[0][-1]
    # Temp variable for reading which years are present in year clip.
    # i.e. which YYYY are present in year set X or XX. Switch from hydro year
    # makes this a general year cut at a given date. So 2 YYYY years should 
    # be present. If only one is found to exist, then portions of the year
    # are missing and that section of the record will be omitted.
    YearsInSet = []
    # Define count, this is used to define which YYYY are present
    Count = 0
    # List for the year cuts that dont included 2 YYYY formats in records.
    FaultyHY = []
    for aRow in RawData:
        if aRow[-1]==YearClip:
            YearsInSet.append(aRow[0])
        if aRow[-1]!=YearClip:
            Count = collections.Counter(YearsInSet)
            Count = copy.deepcopy(Count.keys())
            if len(Count)==2:
                pass
            if len(Count)==1:
                FaultyHY.append(YearClip)
            YearClip = aRow[-1]
            YearsInSet = []

    # Write a list containing only full years from start to end of 
    # defined clip.   
    TempDataIndex = []
    for aRow in RawData:
        if aRow[-1] not in FaultyHY:
            TempDataIndex.append(aRow)
    RawData = []
    for aRow in TempDataIndex:
        RawData.append(aRow)

    TempDataIndex = []

    #New Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
    #*******************Data Coverage Analysis**********************
    # This section counts the occurrence of months per hydro year
    # Write list of years and hydro years (fill in missing data)
    # List of Hydro Years
    HYearList = []
    # List of years 
    YearList = []
    for aRow in RawData:
        HYearList.append(aRow[-1])
        YearList.append(aRow[0])

    # Counter function for identifying years within dataset
    YearKeys = collections.Counter(HYearList)
    YearList = copy.deepcopy(YearKeys.keys())
    # print YearList

    # Write list with full year list
    FullHY = range(RawData[0][-1], RawData[-1][-1]+1)

    # Initial month records
    ListMonths = [] 
    for aRow in RawData:
        ListMonths.append(aRow[2])

    # Filters out months to leave only key variables per hydro year.
    # Result is a list of numbers 1 to 12 for each year. If no data for a 
    # month is found for a given year, then that month will not appear in that range.
    prevRow = ListMonths[0]
    ListMonthFilt = [] 
    for aRow in ListMonths:
        if aRow==prevRow:
            prevRow=aRow
        if aRow!=prevRow:
            ListMonthFilt.append(prevRow)
            prevRow=aRow
    ListMonthFilt.append(prevRow)

    # Change name back to listmonths 
    ListMonths = []
    ListMonths = copy.deepcopy(ListMonthFilt)
    ListMonthFilt = []

    # This provides a coverage percentage of months
    # FHY is final hydro year. Multiplied by 12 represents total number of months expected.
    FHY = RawData[-1][-1] 
    TotalMonths = float(FHY*12)
    # Use counter import to count which months are present
    # and how many times they occur in the dataset
    MonthStats = collections.Counter(ListMonths)
    Months = copy.deepcopy(MonthStats.keys())
    Freq = copy.deepcopy(MonthStats.values())
    Fsum = float(sum(Freq))

    Freq = np.array(Freq, dtype=float)
    MonthlyCoverage = np.array(Freq/FHY, dtype=float)

    # Provides daily coverage percentage
    DateStart = copy.deepcopy(RawData[0][0:3])
    DateStart = str(DateStart)
    DateStart = DateStart.replace(", ", "/")
    DateStart = datetime.strptime(DateStart, '[%Y/%d/%m]')

    DateEnd = copy.deepcopy(RawData[-1][0:3])
    DateEnd = str(DateEnd)
    DateEnd = DateEnd.replace(", ", "/")
    DateEnd = datetime.strptime(DateEnd, '[%Y/%d/%m]')

    delta = DateEnd-DateStart
    # Add 1 to total days to include the first day 
    # of the analysis. Without the +1, it doesn't count
    # for the first day.
    TotalDays = float(delta.days)+1
    PercentRCov = (Fsum/TotalMonths)*100

    plt.figure(figsize=(12,6))
    plt.bar(Months, MonthlyCoverage, align='center', alpha=0.5)
    plt.gca().yaxis.grid(True)
    plt.xticks(Months)
    plt.xlabel('Months')
    plt.ylabel('Percentage of Coverage')
    plt.title('Month Coverage Over Study Period')
    plt.text(1, .1, 'Total Record Coverage For Study Period: %f' % 
        (PercentRCov), verticalalignment='top') 
    # plt.savefig('%s/MissingMonthsData.%s' % (OutputLoc, f), dpi=None, 
    #     facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    #     format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    #     frameon=None)
    # plt.show()
    # Monthly Coverage
    StationExports.append(PercentRCov)
    plt.close()

    # Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]
    # Provides percentage of daily record coverage for study period
    # including nan inserts to fill dates. This value should always be
    # 100 percent.
    DailyRecordCoverage = (float(len(RawData))/TotalDays)*100
    StationExports.append(DailyRecordCoverage)
    # ***************************Missing Temperature Analysis
    # ***************************Missing Temperature Analysis
    # ***************************Missing Temperature Analysis
    # WORK
    # Define omitted years WORK
    MissingTempData = [] # Dataset containing count of missing records per year
    Tx = [] # The x axis value set on hydro years
    Temp = 0
    HY = RawData[0][-1] # Hydro Year

    for aRow in RawData:
        if aRow[-1]==HY: 
            try:  
                if np.isnan(aRow[-2]) == True and np.isnan(aRow[6]) == True:
                    Temp = Temp+1
            except:
                if np.isnan(aRow[-2]) == True and np.isnan(aRow[5]) == True:
                    Temp = Temp+1
        if aRow[-1]!=HY:
            Tx.append(HY)
            HY = aRow[-1]
            try:  
                if np.isnan(aRow[-2]) == True and np.isnan(aRow[6]) == True:
                    Temp = Temp+1
            except:
                if np.isnan(aRow[-2]) == True and np.isnan(aRow[5]) == True:
                    Temp = Temp+1
            MissingTempData.append(Temp)
            Temp=0
    Tx.append(HY)
    MissingTempData.append(Temp)

    # Define years missing data to omit from annual averages
    # WORK WORK
    temp = 0
    i = 0
    for aRow in MissingTempData:
        aRow = float(aRow)
        temp = aRow/365
        # Anything greater than 100 years
        if temp >= 0.2739:
            OmitYearsT.append(Tx[i])
        i = i+1


    # Write data for missing years. Estimates missing 365 records per
    # year. Ignores leap years of 366 as 365 (not considered significant)
    temp = set(Tx).symmetric_difference(set(FullHY))
    temp = list(temp)

    # Write a value of 365 for each year missing.
    # If nan inserts do not fail, no manual inserts will be required.
    MissingYears = []
    for aRow in temp:
        MissingYears.append(365)

    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : MissingTempData, "b" : Tx})

    # Combine these based upon hydro year.
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')

    # Write these columns to list (order will be sorted in graph)
    MissingTempData = Tdf['a'].values.tolist()
    Tx = Tdf['b'].values.tolist()

    # Xplace defines location on y axis to place text
    Xplace = 0
    for aRow in MissingTempData:
        if aRow>Xplace:
            Xplace=aRow
    PercentMissing = float(sum(MissingTempData))/TotalDays
    PercentRCov = (1-PercentMissing)*100
    plt.figure(figsize=(12,6))
    plt.bar(Tx, MissingTempData, align='center', alpha=0.5)
    plt.gca().yaxis.grid(True)
    plt.xticks(Tx, rotation='vertical')
    plt.xlabel('Hydro Year')
    plt.ylabel('Missing Records')
    plt.title('Missing Temperature Records Per Hydro Year')
    plt.text(1, Xplace, 'Percent Coverage For Study Period: %f' % 
        (PercentRCov), verticalalignment='top') 
    plt.savefig('%s/MissingTempData.%s' % (OutputLoc, f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    plt.close()
    # print PercentRCov
    # print Tx
    # print MissingTempData

    # Temperature coverage insert for final data
    StationExports.append(PercentRCov)
    # ***************************Missing Snowfall Data
    # ***************************Missing Snowfall Data
    # ***************************Missing Snowfall Data
    # WORK
    MissingSnowData = [] # Dataset containing count of missing records per year
    Sx = [] # The x axis value set of hydro years
    Temp = 0
    HY = 1 # Hydro Year
    for aRow in RawData:
        if aRow[-1]==HY:   
            if np.isnan(aRow[-5]) == True:
                Temp = Temp+1
        if aRow[-1]!=HY:
            Sx.append(HY)
            HY = aRow[-1]
            if np.isnan(aRow[-5]) == True:
                Temp = Temp+1
            MissingSnowData.append(Temp)
            Temp=0
    Sx.append(HY)
    MissingSnowData.append(Temp)
    # print Sx
    # print MissingSnowData

    # Write data for missing years. Estimates missing 365 records per
    # year. Overwrites leap years of 366 as 365 (not considered significant)
    temp = set(Sx).symmetric_difference(set(FullHY))
    temp = list(temp)
    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(365)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : MissingSnowData, "b" : Sx})
    # Combine these based upon hydro year.
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    MissingSnowData = Tdf['a'].values.tolist()
    Sx = Tdf['b'].values.tolist()

    PercentMissing = float(sum(MissingSnowData))/TotalDays
    PercentRCov = (1-PercentMissing)*100
    # Xplace defines location on y axis to place text
    Xplace = 0
    for aRow in MissingSnowData:
        if aRow>Xplace:
            Xplace=aRow
    plt.figure(figsize=(12,6))
    plt.bar(Sx, MissingSnowData, align='center', alpha=0.5)
    plt.gca().yaxis.grid(True)
    plt.xticks(Sx, rotation='vertical')
    plt.xlabel('Hydro Year')
    plt.ylabel('Missing Records')
    plt.title('Missing Snowfall Records Per Hydro Year')
    plt.text(1, Xplace, 'Percent Coverage For Study Period: %f' % 
        (PercentRCov), verticalalignment='top') 
    plt.savefig('%s/MissingSnowData.%s' % (OutputLoc, f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()

    # Snowfall coverage insert for final data
    StationExports.append(PercentRCov)
    plt.close()


    # ***************************Missing Rainfall Data
    # ***************************Missing Rainfall Data
    # ***************************Missing Rainfall Data
    MissingRainData = [] # Dataset containing count of missing records per year
    Rx = [] # The x axis value set of hydro years
    Temp = 0
    HY = 1 # Hydro Year

    for aRow in RawData:
        if aRow[-1]==HY:   
            if np.isnan(aRow[-6]) == True:
                Temp = Temp+1
        if aRow[-1]!=HY:
            Rx.append(HY)
            HY = aRow[-1]
            if np.isnan(aRow[-6]) == True:
                Temp = Temp+1
            MissingRainData.append(Temp)
            Temp=0
    Rx.append(HY)
    MissingRainData.append(Temp)

    # Write data for missing years. Estimates missing 365 records per
    # year. Overwrites leap years of 366 as 365 (not considered significant)
    temp = set(Rx).symmetric_difference(set(FullHY))
    temp = list(temp)
    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(365)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : MissingRainData, "b" : Rx})
    # Combine these based upon hydro year.
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    MissingRainData = Tdf['a'].values.tolist()
    Rx = Tdf['b'].values.tolist()

    PercentMissing = float(sum(MissingRainData))/TotalDays
    PercentRCov = (1-PercentMissing)*100
    # Xplace defines location on y axis to place text
    Xplace = 0
    for aRow in MissingRainData:
        if aRow>Xplace:
            Xplace=aRow
    plt.figure(figsize=(12,6))
    plt.bar(Rx, MissingRainData, align='center', alpha=0.5)
    plt.gca().yaxis.grid(True)
    plt.xticks(Rx, rotation='vertical')
    plt.xlabel('Hydro Year')
    plt.ylabel('Missing Records')
    plt.title('Missing Rain Records Per Hydro Year')
    plt.text(1, Xplace, 'Percent Coverage For Study Period: %f' % 
        (PercentRCov), verticalalignment='top') 
    plt.savefig('%s/MissingRainData.%s' % (OutputLoc, f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    # Rain coverage insert for final data
    StationExports.append(PercentRCov)
    plt.close()

    #Snow only record
    # print RawData
    # WORK RawData is not being exported
    for aRow in RawData:
        if aRow[-5]!=0.0 and np.isnan(aRow[-5]) != True:
            SnowData.append(aRow)
    RawData = copy.deepcopy(RawData)
    # print "END of SplitData"