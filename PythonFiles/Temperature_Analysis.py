from BasicImports import *

def Temperature (RawData, StationName, f, BaseData, StationExports, OmitYearsT):
    dir = 'Output/'+StationName+'/Temperature'
    if not os.path.exists(dir):
        os.makedirs('Output/'+StationName+'/Temperature')
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)

    subfolder_names = ['Monthly', 'Annual', 'Seasonal']
    for subfolder_name in subfolder_names:
        os.makedirs(os.path.join(dir, subfolder_name))

    # Name x axis on graphs:
    NameX = 'Years'

    # Ensure clipping of years missing data. SplitData initially does this.
    # However, the modification is overwritten/forgotten prior to use by this 
    # module.
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
        del aRow[3:5]
        RawData.append(aRow)

    ###TEMP TEMP TEMP TEMP
    # CutData contains entire snow season record set of snowfall and 
    # liquid precipitation. CutData is in chronological order
    # DATA FORMAT [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro]
    #************    0   1    2     3     4      5      6    7      8
    allData = copy.deepcopy(BaseData)

    #*****************************Temp only record*******************

    # Count Months with average temp available 
    CheckDataM = []
    for aRow in allData:
        del aRow[3:5]
        CheckDataM.append(aRow[2])
    # FORMAT [Year, DD, MM, Tmax, Tmin, TOBS, Hydro]
    #***************************Month Averages*********************
    # Year index
    i = RawData[0][0]
    # Month index
    M = RawData[0][2]
    # List of years analyzed by loop
    YList = []
    # List of months in order of analysis
    MonthList = []
    # List of standard deviation values for each month
    MonthSTD = []
    # List of monthly averages
    MonthAve = []
    # Temporary List for daily data to be placed into
    MonthTemp = []
    # Count of records passed to count to final record for loop break
    index = 0
    # Write index to locate records in temp dataset with missing high and low
    missingHL = []
    # Number of records missing all temperature data
    NullRecords = 0

    for aRow in RawData:
        if index==(len(RawData)-1):
            if np.isnan(aRow[3]) != True and np.isnan(aRow[4]) != True:
                TempVar = (aRow[3]+aRow[4])/2
                MonthTemp.append(TempVar)
            if np.isnan(aRow[3]) != True or np.isnan(aRow[4]) != True:
                MonthTemp.append(np.nan)
                if np.isnan(aRow[5]) != True:
                    missingHL.append(index)
                if np.isnan(aRow[5]) == True:
                    NullRecords = NullRecords+1
            YList.append(i)
            MonthList.append(M)
            MonthSTD.append(np.nanstd(MonthTemp))
            MonthAve.append(np.nanmean(MonthTemp))
        if aRow[0]==i:
            if aRow[2]==M:
                if np.isnan(aRow[3]) != True and np.isnan(aRow[4]) != True:
                    TempVar = (aRow[3]+aRow[4])/2
                    MonthTemp.append(TempVar)
                if np.isnan(aRow[3]) != True or np.isnan(aRow[4]) != True:
                    MonthTemp.append(np.nan)
                    if np.isnan(aRow[5]) != True:
                        missingHL.append(index)
                    if np.isnan(aRow[5]) == True:
                        NullRecords = NullRecords+1
            if aRow[2]!=M:
                MonthList.append(M)
                YList.append(i)
                if len(MonthTemp)!=0:
                    # Will still get error message from nanmean if 
                    # nan value is the only value for month. 
                    MonthSTD.append(np.nanstd(MonthTemp))
                    MonthAve.append(np.nanmean(MonthTemp))
                if len(MonthTemp)==0:
                    # Manually insert nan value if all data is missing. This
                    # prevents Degrees of Freedom error message from printing for
                    # for mean and std calculations.
                    MonthSTD.append(np.nan)
                    MonthAve.append(np.nan)
                MonthTemp = []
                if np.isnan(aRow[3]) != True and np.isnan(aRow[4]) != True:
                    TempVar = (aRow[3]+aRow[4])/2
                    MonthTemp.append(TempVar)
                if np.isnan(aRow[3]) != True or np.isnan(aRow[4]) != True:
                    MonthTemp.append(np.nan)
                    if np.isnan(aRow[5]) != True:
                        missingHL.append(index)
                    if np.isnan(aRow[5]) == True:
                        NullRecords = NullRecords+1
            index = index+1
            M = aRow[2]
        if aRow[0]!=i:
            MonthList.append(M)
            YList.append(i)
            MonthSTD.append(np.nanstd(MonthTemp))
            MonthAve.append(np.nanmean(MonthTemp))
            index=index+1
            M = aRow[2]
            i = aRow[0]
            MonthTemp = []
            if np.isnan(aRow[3]) != True and np.isnan(aRow[4]) != True:
                TempVar = (aRow[3]+aRow[4])/2
                MonthTemp.append(TempVar)
            if np.isnan(aRow[3]) != True or np.isnan(aRow[4]) != True:
                MonthTemp.append(np.nan)
                if np.isnan(aRow[5]) != True:
                    missingHL.append(index)
                if np.isnan(aRow[5]) == True:
                    NullRecords = NullRecords+1

    df = pd.DataFrame(MonthList, columns=['Month'])
    idx = 0
    df.insert(idx, column='Year', value=YList)
    df.insert(idx, column='STD', value=MonthSTD)
    df.insert(idx, column='Average', value=MonthAve)
    GroupData = df.values.tolist()
    # Format [AverageT, STD, Year, Month]
    JanAve = []
    JanSTD = []
    YearsJan = []

    FebAve = []
    FebSTD = []
    YearsFeb = []

    MarAve = []
    MarSTD = []
    YearsMar = []

    AprAve = []
    AprSTD = []
    YearsApr = []

    MayAve = []
    MaySTD = []
    YearsMay = []

    JunAve = []
    JunSTD = []
    YearsJun = []

    JulAve = []
    JulSTD = []
    YearsJul = []

    AugAve = []
    AugSTD = []
    YearsAug = []

    SepAve = []
    SepSTD = []
    YearsSep = []

    OctAve = []
    OctSTD = []
    YearsOct = []

    NovAve = []
    NovSTD = []
    YearsNov = []

    DecAve = []
    DecSTD = []
    YearsDec = []

    for aRow in GroupData:
        if aRow[-1]==1:
            JanAve.append(aRow[0])
            JanSTD.append(aRow[1])
            YearsJan.append(aRow[-2])
        if aRow[-1]==2:
            FebAve.append(aRow[0])
            FebSTD.append(aRow[1])
            YearsFeb.append(aRow[-2])        
        if aRow[-1]==3:
            MarAve.append(aRow[0])
            MarSTD.append(aRow[1])
            YearsMar.append(aRow[-2])
        if aRow[-1]==4:
            AprAve.append(aRow[0])
            AprSTD.append(aRow[1])
            YearsApr.append(aRow[-2])
        if aRow[-1]==5:
            MayAve.append(aRow[0])
            MaySTD.append(aRow[1])
            YearsMay.append(aRow[-2])
        if aRow[-1]==6:
            JunAve.append(aRow[0])
            JunSTD.append(aRow[1])
            YearsJun.append(aRow[-2])
        if aRow[-1]==7:
            JulAve.append(aRow[0])
            JulSTD.append(aRow[1])
            YearsJul.append(aRow[-2])
        if aRow[-1]==8:
            AugAve.append(aRow[0])
            AugSTD.append(aRow[1])
            YearsAug.append(aRow[-2])
        if aRow[-1]==9:
            SepAve.append(aRow[0])
            SepSTD.append(aRow[1])
            YearsSep.append(aRow[-2])
        if aRow[-1]==10:
            OctAve.append(aRow[0])
            OctSTD.append(aRow[1])
            YearsOct.append(aRow[-2])
        if aRow[-1]==11:
            NovAve.append(aRow[0])
            NovSTD.append(aRow[1])
            YearsNov.append(aRow[-2])
        if aRow[-1]==12:
            DecAve.append(aRow[0])
            DecSTD.append(aRow[1])
            YearsDec.append(aRow[-2])

    # Seasonal stats

    # Suggest data coverage check for this analysis

    #### SPRING
    SpringAve = []
    SpringSTD = []
    SpringYears = []
    TemperTemp = []
    i = allData[0][0]

    for aRow in allData:
        if aRow[0]==i:
            if aRow[2]==3 or aRow[2]==4 or aRow[2]==5:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
        if aRow[0]!=i:
            if len(TemperTemp)==0:
                SpringSTD.append(np.nan)
                SpringAve.append(np.nan)
            if len(TemperTemp)!=0:
                SpringSTD.append(np.std(TemperTemp))
                SpringAve.append(np.mean(TemperTemp))
            SpringYears.append(i)
            i = aRow[0]
            TemperTemp=[]
            if aRow[2]==3 or aRow[2]==4 or aRow[2]==5:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
    SpringSTD.append(np.std(TemperTemp))
    SpringAve.append(np.mean(TemperTemp))
    SpringYears.append(i)

    if len(SpringYears)!= len(SpringSTD) or len(SpringYears)!= len(SpringAve):
        print (" \n******Spring Temperature Analysis Miscalculation******\n ")

    #### SUMMER
    SummerAve = []
    SummerSTD = []
    SummerYears = []
    TemperTemp = []
    i = allData[0][0]

    for aRow in allData:
        if aRow[0]==i:
            if aRow[2]==6 or aRow[2]==7 or aRow[2]==8:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
        if aRow[0]!=i:
            if len(TemperTemp)==0:
                SummerSTD.append(np.nan)
                SummerAve.append(np.nan)
            if len(TemperTemp)!=0:
                SummerSTD.append(np.std(TemperTemp))
                SummerAve.append(np.mean(TemperTemp))
            SummerYears.append(i)
            i = aRow[0]
            TemperTemp=[]
            if aRow[2]==6 or aRow[2]==7 or aRow[2]==8:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
    SummerSTD.append(np.std(TemperTemp))
    SummerAve.append(np.mean(TemperTemp))
    SummerYears.append(i)

    if len(SummerYears)!= len(SummerSTD) or len(SummerYears)!= len(SummerAve):
        print (" \n******Summer Temperature Analysis Miscalculation******\n ")


    #### Fall
    FallAve = []
    FallSTD = []
    FallYears = []
    TemperTemp = []
    i = allData[0][0]

    for aRow in allData:
        if aRow[0]==i:
            if aRow[2]==9 or aRow[2]==10 or aRow[2]==11:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
        if aRow[0]!=i:
            if len(TemperTemp)==0:
                FallSTD.append(np.nan)
                FallAve.append(np.nan)
            if len(TemperTemp)!=0:
                FallSTD.append(np.std(TemperTemp))
                FallAve.append(np.mean(TemperTemp))
            FallYears.append(i)
            i = aRow[0]
            TemperTemp=[]
            if aRow[2]==9 or aRow[2]==10 or aRow[2]==11:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
    FallSTD.append(np.std(TemperTemp))
    FallAve.append(np.mean(TemperTemp))
    FallYears.append(i)

    if len(FallYears)!= len(FallSTD) or len(FallYears)!= len(FallAve):
        print (" \n******Fall Temperature Analysis Miscalculation******\n ")

    #### Winter
    # Since this season is between years, the year clip from RawData
    # must be used to ensure records from same winter season are
    # being compared per year. As opposed to January, February, and
    # December of the same year YYYY. This leads to less winter seasons
    # being analyzed if data gaps are present. The program clips anything
    # that isn't a full year (based on RawData year clip). 
    # If every year is present in the data, no winter gaps will 
    # be found. 
    WinterAve = []
    WinterSTD = []
    WinterYears = []
    TemperTemp = []
    # Switch to RawData for winter
    i = RawData[0][-1]

    for aRow in RawData:
        if aRow[-1]==i:
            if aRow[2]==12 or aRow[2]==1 or aRow[2]==2:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
        if aRow[-1]!=i:
            if len(TemperTemp)==0:
                WinterSTD.append(np.nan)
                WinterAve.append(np.nan)
            if len(TemperTemp)!=0:
                WinterSTD.append(np.std(TemperTemp))
                WinterAve.append(np.mean(TemperTemp))
            WinterYears.append(i)
            i = aRow[-1]
            TemperTemp=[]
            if aRow[2]==12 or aRow[2]==1 or aRow[2]==2:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
    WinterSTD.append(np.std(TemperTemp))
    WinterAve.append(np.mean(TemperTemp))
    WinterYears.append(i)

    if len(WinterYears)!= len(WinterSTD) or len(WinterYears)!= len(WinterAve):
        print (" \n******Winter Temperature Analysis Miscalculation******\n ")

    # Annual Average
 
    TemperTemp = []
    AnnualYears = []
    AnnualAve = []
    AnnualSTD = []
    i = RawData[0][-1]
    z = 0
    for aRow in RawData:
        if aRow[-1]!=OmitYearsT[z]:
            if aRow[-1]==i:
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
            if aRow[-1]!=i:
                if len(TemperTemp)==0:
                    AnnualSTD.append(np.nan)
                    AnnualAve.append(np.nan)
                if len(TemperTemp)!=0:
                    AnnualSTD.append(np.std(TemperTemp))
                    AnnualAve.append(np.mean(TemperTemp))
                AnnualYears.append(i)
                i = aRow[-1]
                TemperTemp=[]
                if np.isnan(aRow[-3]) != True and np.isnan(aRow[-4]) != True:
                    ave = (aRow[-3]+aRow[-4])/2
                    TemperTemp.append(ave)
        if z!=len(OmitYearsT)-1:
            if aRow[-1]==OmitYearsT[z]:
                AnnualSTD.append(np.std(np.nan))
                AnnualAve.append(np.mean(np.nan))
                AnnualYears.append(i)
                z = z+1         
    AnnualSTD.append(np.std(TemperTemp))
    AnnualAve.append(np.mean(TemperTemp))
    AnnualYears.append(i)
    # print AnnualYears
    # print len(AnnualSTD)
    # sys.exit()
    if len(AnnualYears)!= len(AnnualSTD) or len(AnnualYears)!= len(AnnualAve):
        print (" \n******Annual Temperature Analysis Miscalculation******\n ")


    #***************************************** Month Graphing
    #***************************************** Month Graphing
    #***************************************** Month Graphing
    #***************************************** Month Graphing

    #***************************************************
    Y1 = BaseData[0][0]
    YF = BaseData[-1][0]
    FullY = range(Y1, YF+1)

    temp = set(YearsJan).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    #**********************************For this month
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : JanAve, "b" : YearsJan})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : JanSTD, "b" : YearsJan})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    JanAve = Tdf['a'].values.tolist()
    YearsJan = Tdf['b'].values.tolist()
    JanSTD = Tdf2['a'].values.tolist()
    YearsJan = np.array(YearsJan)
    JanAve = np.array(JanAve)
    JanSTD = np.array(JanSTD)
    #**************************************************
    mask = ~np.isnan(YearsJan) & ~np.isnan(JanAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for January', fontweight='bold')
    plt.plot(YearsJan,JanAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJan[mask], JanAve[mask])
    plt.plot(YearsJan,intercept+slope*YearsJan, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JanuaryAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    # plt.show()
    plt.close()

    JanSTD = np.array(JanSTD)

    mask = ~np.isnan(YearsJan) & ~np.isnan(JanSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for January', fontweight='bold')
    plt.plot(YearsJan,JanSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJan[mask], JanSTD[mask])
    plt.plot(YearsJan,intercept+slope*YearsJan, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JanuarySTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    # plt.show()
    plt.close()

    # February
        #**********************************For this month

    temp = set(YearsFeb).symmetric_difference(set(FullY))
    temp = list(temp)


    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : FebAve, "b" : YearsFeb})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : FebSTD, "b" : YearsFeb})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    FebAve = Tdf['a'].values.tolist()
    YearsFeb = Tdf['b'].values.tolist()
    FebSTD = Tdf2['a'].values.tolist()
    YearsFeb = np.array(YearsFeb)
    FebAve = np.array(FebAve)
    FebSTD = np.array(FebSTD)
    #**************************************************
    YearsFeb = np.array(YearsFeb)
    FebAve = np.array(FebAve)

    mask = ~np.isnan(YearsFeb) & ~np.isnan(FebAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for February', fontweight='bold')
    plt.plot(YearsFeb,FebAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsFeb[mask], FebAve[mask])
    plt.plot(YearsFeb,intercept+slope*YearsFeb, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/FebruaryAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    FebSTD = np.array(FebSTD)

    mask = ~np.isnan(YearsFeb) & ~np.isnan(FebSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for February', fontweight='bold')
    plt.plot(YearsFeb,FebSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsFeb[mask], FebSTD[mask])
    plt.plot(YearsFeb,intercept+slope*YearsFeb, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/FebruarySTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    # plt.show()
    plt.close()


    # March
    #**********************************For this month

    temp = set(YearsMar).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : MarAve, "b" : YearsMar})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : MarSTD, "b" : YearsMar})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    MarAve = Tdf['a'].values.tolist()
    YearsMar = Tdf['b'].values.tolist()
    MarSTD = Tdf2['a'].values.tolist()
    YearsMar = np.array(YearsMar)
    MarAve = np.array(MarAve)
    MarSTD = np.array(MarSTD)
    #**************************************************
    YearsMar = np.array(YearsMar)
    MarAve = np.array(MarAve)

    mask = ~np.isnan(YearsMar) & ~np.isnan(MarAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for March', fontweight='bold')
    plt.plot(YearsMar,MarAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMar[mask], MarAve[mask])
    plt.plot(YearsMar,intercept+slope*YearsMar, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/MarchAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    MarSTD = np.array(MarSTD)

    mask = ~np.isnan(YearsMar) & ~np.isnan(MarSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for March', fontweight='bold')
    plt.plot(YearsMar,MarSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMar[mask], MarSTD[mask])
    plt.plot(YearsMar,intercept+slope*YearsMar, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/MarchSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()


    # April
    #**********************************For this month

    temp = set(YearsApr).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : AprAve, "b" : YearsApr})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : AprSTD, "b" : YearsApr})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    AprAve = Tdf['a'].values.tolist()
    YearsApr = Tdf['b'].values.tolist()
    AprSTD = Tdf2['a'].values.tolist()
    YearsApr = np.array(YearsApr)
    AprAve = np.array(AprAve)
    AprSTD = np.array(AprSTD)
    #**************************************************
    YearsApr = np.array(YearsApr)
    AprAve = np.array(AprAve)

    mask = ~np.isnan(YearsApr) & ~np.isnan(AprAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for April', fontweight='bold')
    plt.plot(YearsApr,AprAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsApr[mask], AprAve[mask])
    plt.plot(YearsApr,intercept+slope*YearsApr, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AprilAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    AprSTD = np.array(AprSTD)

    mask = ~np.isnan(YearsApr) & ~np.isnan(AprSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for April', fontweight='bold')
    plt.plot(YearsApr,AprSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsApr[mask], AprSTD[mask])
    plt.plot(YearsApr,intercept+slope*YearsApr, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AprilSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()


    # May
    #**********************************For this month
    temp = set(YearsMay).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : MayAve, "b" : YearsMay})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : MaySTD, "b" : YearsMay})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    MayAve = Tdf['a'].values.tolist()
    YearsMay = Tdf['b'].values.tolist()
    MaySTD = Tdf2['a'].values.tolist()
    YearsMay = np.array(YearsMay)
    MayAve = np.array(MayAve)
    MaySTD = np.array(MaySTD)
    #**************************************************
    YearsMay = np.array(YearsMay)
    MayAve = np.array(MayAve)

    mask = ~np.isnan(YearsMay) & ~np.isnan(MayAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for May', fontweight='bold')
    plt.plot(YearsMay,MayAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMay[mask], MayAve[mask])
    plt.plot(YearsMay,intercept+slope*YearsMay, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/MayAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    MaySTD = np.array(MaySTD)

    mask = ~np.isnan(YearsMay) & ~np.isnan(MaySTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for May', fontweight='bold')
    plt.plot(YearsMay,MaySTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMay[mask], MaySTD[mask])
    plt.plot(YearsMay,intercept+slope*YearsMay, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/MaySTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()


    # June
    #**********************************For this month

    temp = set(YearsJun).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : JunAve, "b" : YearsJun})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : JunSTD, "b" : YearsJun})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    JunAve = Tdf['a'].values.tolist()
    YearsJun = Tdf['b'].values.tolist()
    JunSTD = Tdf2['a'].values.tolist()
    YearsJun = np.array(YearsJun)
    JunAve = np.array(JunAve)
    JunSTD = np.array(JunSTD)
    #**************************************************
    YearsJun = np.array(YearsJun)
    JunAve = np.array(JunAve)

    mask = ~np.isnan(YearsJun) & ~np.isnan(JunAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for June', fontweight='bold')
    plt.plot(YearsJun,JunAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJun[mask], JunAve[mask])
    plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JuneAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    JunSTD = np.array(JunSTD)

    mask = ~np.isnan(YearsJun) & ~np.isnan(JunSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for June', fontweight='bold')
    plt.plot(YearsJun,JunSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJun[mask], JunSTD[mask])
    plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JuneSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()


    # July
    #**********************************For this month

    temp = set(YearsJul).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : JulAve, "b" : YearsJul})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : JulSTD, "b" : YearsJul})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    JulAve = Tdf['a'].values.tolist()
    YearsJul = Tdf['b'].values.tolist()
    JulSTD = Tdf2['a'].values.tolist()
    YearsJul = np.array(YearsJul)
    JulAve = np.array(JulAve)
    JulSTD = np.array(JulSTD)
    #**************************************************
    YearsJul = np.array(YearsJul)
    JulAve = np.array(JulAve)

    mask = ~np.isnan(YearsJul) & ~np.isnan(JulAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for July', fontweight='bold')
    plt.plot(YearsJul,JulAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulAve[mask])
    plt.plot(YearsJul,intercept+slope*YearsJul, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JulyAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    JulSTD = np.array(JulSTD)

    mask = ~np.isnan(YearsJul) & ~np.isnan(JulSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for July', fontweight='bold')
    plt.plot(YearsJul,JulSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulSTD[mask])
    plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/JulySTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # August
    #**********************************For this month

    temp = set(YearsAug).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : AugAve, "b" : YearsAug})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : AugSTD, "b" : YearsAug})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    AugAve = Tdf['a'].values.tolist()
    YearsAug = Tdf['b'].values.tolist()
    AugSTD = Tdf2['a'].values.tolist()
    YearsAug = np.array(YearsAug)
    AugAve = np.array(AugAve)
    AugSTD = np.array(AugSTD)
    #**************************************************
    YearsAug = np.array(YearsAug)
    AugAve = np.array(AugAve)

    mask = ~np.isnan(YearsAug) & ~np.isnan(AugAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for August', fontweight='bold')
    plt.plot(YearsAug,AugAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsAug[mask], AugAve[mask])
    plt.plot(YearsAug,intercept+slope*YearsAug, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AugustAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    AugSTD = np.array(AugSTD)

    mask = ~np.isnan(YearsAug) & ~np.isnan(AugSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for August', fontweight='bold')
    plt.plot(YearsAug,AugSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsAug[mask], AugSTD[mask])
    plt.plot(YearsAug,intercept+slope*YearsAug, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AugustSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # September
    #**********************************For this month

    temp = set(YearsSep).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : SepAve, "b" : YearsSep})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : SepSTD, "b" : YearsSep})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    SepAve = Tdf['a'].values.tolist()
    YearsSep = Tdf['b'].values.tolist()
    SepSTD = Tdf2['a'].values.tolist()
    YearsSep = np.array(YearsSep)
    SepAve = np.array(SepAve)
    SepSTD = np.array(SepSTD)
    #**************************************************
    YearsSep = np.array(YearsSep)
    SepAve = np.array(SepAve)

    mask = ~np.isnan(YearsSep) & ~np.isnan(SepAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for September', fontweight='bold')
    plt.plot(YearsSep,SepAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsSep[mask], SepAve[mask])
    plt.plot(YearsSep,intercept+slope*YearsSep, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SeptemberAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    SepSTD = np.array(SepSTD)

    mask = ~np.isnan(YearsSep) & ~np.isnan(SepSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for September', fontweight='bold')
    plt.plot(YearsSep,SepSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsSep[mask], SepSTD[mask])
    plt.plot(YearsSep,intercept+slope*YearsSep, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SeptemberSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # October
    #**********************************For this month

    temp = set(YearsOct).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : OctAve, "b" : YearsOct})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : OctSTD, "b" : YearsOct})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    OctAve = Tdf['a'].values.tolist()
    YearsOct = Tdf['b'].values.tolist()
    OctSTD = Tdf2['a'].values.tolist()
    YearsOct = np.array(YearsOct)
    OctAve = np.array(OctAve)
    OctSTD = np.array(OctSTD)
    #**************************************************
    YearsOct = np.array(YearsOct)
    OctAve = np.array(OctAve)

    mask = ~np.isnan(YearsOct) & ~np.isnan(OctAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for October', fontweight='bold')
    plt.plot(YearsOct,OctAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsOct[mask], OctAve[mask])
    plt.plot(YearsOct,intercept+slope*YearsOct, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/OctoberAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    OctSTD = np.array(OctSTD)

    mask = ~np.isnan(YearsOct) & ~np.isnan(OctSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for October', fontweight='bold')
    plt.plot(YearsOct,OctSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsOct[mask], OctSTD[mask])
    plt.plot(YearsOct,intercept+slope*YearsOct, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/OctoberSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # November
    #**********************************For this month

    temp = set(YearsNov).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : NovAve, "b" : YearsNov})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : NovSTD, "b" : YearsNov})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    NovAve = Tdf['a'].values.tolist()
    YearsNov = Tdf['b'].values.tolist()
    NovSTD = Tdf2['a'].values.tolist()
    YearsNov = np.array(YearsNov)
    NovAve = np.array(NovAve)
    NovSTD = np.array(NovSTD)
    #**************************************************
    YearsNov = np.array(YearsNov)
    NovAve = np.array(NovAve)

    mask = ~np.isnan(YearsNov) & ~np.isnan(NovAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for November', fontweight='bold')
    plt.plot(YearsNov,NovAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsNov[mask], NovAve[mask])
    plt.plot(YearsNov,intercept+slope*YearsNov, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/NovemberAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    NovSTD = np.array(NovSTD)

    mask = ~np.isnan(YearsNov) & ~np.isnan(NovSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for November', fontweight='bold')
    plt.plot(YearsNov,NovSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsNov[mask], NovSTD[mask])
    plt.plot(YearsNov,intercept+slope*YearsNov, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/NovemberSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # December
    #**********************************For this month

    temp = set(YearsDec).symmetric_difference(set(FullY))
    temp = list(temp)

    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : DecAve, "b" : YearsDec})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : DecSTD, "b" : YearsDec})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    DecAve = Tdf['a'].values.tolist()
    YearsDec = Tdf['b'].values.tolist()
    DecSTD = Tdf2['a'].values.tolist()
    YearsDec = np.array(YearsDec)
    DecAve = np.array(DecAve)
    DecSTD = np.array(DecSTD)
    #**************************************************
    YearsDec = np.array(YearsDec)
    DecAve = np.array(DecAve)

    mask = ~np.isnan(YearsDec) & ~np.isnan(DecAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Monthly Temperature for December', fontweight='bold')
    plt.plot(YearsDec,DecAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsDec[mask], DecAve[mask])
    plt.plot(YearsDec,intercept+slope*YearsDec, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/DecemberAve.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    DecSTD = np.array(DecSTD)

    mask = ~np.isnan(YearsDec) & ~np.isnan(DecSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Monthly Temperature STD for December', fontweight='bold')
    plt.plot(YearsDec,DecSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(YearsDec[mask], DecSTD[mask])
    plt.plot(YearsDec,intercept+slope*YearsDec, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/DecemberSTD.%s' % (dir, 'Monthly', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # *******************************Seasonal Graphing 
    # *******************************Seasonal Graphing 
    # *******************************Seasonal Graphing 
    # *******************************Seasonal Graphing 
    # Summer
    SummerSTD = np.array(SummerSTD)
    SummerYears = np.array(SummerYears)
    SummerAve = np.array(SummerAve)

    mask = ~np.isnan(SummerYears) & ~np.isnan(SummerAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Summer Season Temperature', fontweight='bold')
    plt.plot(SummerYears,SummerAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(SummerYears[mask], SummerAve[mask])
    plt.plot(SummerYears,intercept+slope*SummerYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SummerAve.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    SummerSTD = np.array(SummerSTD)

    mask = ~np.isnan(SummerYears) & ~np.isnan(SummerSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Summer Temperature STD', fontweight='bold')
    plt.plot(SummerYears,SummerSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(SummerYears[mask], SummerSTD[mask])
    plt.plot(SummerYears,intercept+slope*SummerYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SummerSTD.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()


    # Fall
    FallYears = np.array(FallYears)
    FallAve = np.array(FallAve)

    mask = ~np.isnan(FallYears) & ~np.isnan(FallAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Fall Season Temperature', fontweight='bold')
    plt.plot(FallYears,FallAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(FallYears[mask], FallAve[mask])
    plt.plot(FallYears,intercept+slope*FallYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/FallAve.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    FallSTD = np.array(FallSTD)

    mask = ~np.isnan(FallYears) & ~np.isnan(FallSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Fall Temperature STD', fontweight='bold')
    plt.plot(FallYears,FallSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(FallYears[mask], FallSTD[mask])
    plt.plot(FallYears,intercept+slope*FallYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/FallSTD.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    # print slope
    # print p_value
    # print r_value
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()
    # Winter
    WinterYears = np.array(WinterYears)
    WinterAve = np.array(WinterAve)

    mask = ~np.isnan(WinterYears) & ~np.isnan(WinterAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Winter Season Temperature', fontweight='bold')
    plt.plot(WinterYears,WinterAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(WinterYears[mask], WinterAve[mask])
    plt.plot(WinterYears,intercept+slope*WinterYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/WinterAve.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    WinterSTD = np.array(WinterSTD)

    mask = ~np.isnan(WinterYears) & ~np.isnan(WinterSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Winter Temperature STD', fontweight='bold')
    plt.plot(WinterYears,WinterSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(WinterYears[mask], WinterSTD[mask])
    plt.plot(WinterYears,intercept+slope*WinterYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/WinterSTD.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # Spring
    #***********************************
    SpringYears = np.array(SpringYears)
    SpringAve = np.array(SpringAve)
    SpringSTD = np.array(SpringSTD)
    #**********************************************

    mask = ~np.isnan(SpringYears) & ~np.isnan(SpringAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Spring Season Temperature', fontweight='bold')
    plt.plot(SpringYears,SpringAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(SpringYears[mask], SpringAve[mask])
    plt.plot(SpringYears,intercept+slope*SpringYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SpringAve.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    SpringSTD = np.array(SpringSTD)

    mask = ~np.isnan(SpringYears) & ~np.isnan(SpringSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Spring Temperature STD', fontweight='bold')
    plt.plot(SpringYears,SpringSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(SpringYears[mask], SpringSTD[mask])
    plt.plot(SpringYears,intercept+slope*SpringYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/SpringSTD.%s' % (dir, 'Seasonal', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # ********************************Annual Graphing
    # ********************************Annual Graphing
    # ********************************Annual Graphing
    # ********************************Annual Graphing

    Y1 = RawData[0][-1]
    YF = RawData[-1][-1]
    FullY = range(Y1, YF+1)
    # print SpringYears
    # print FullY

    temp = set(AnnualYears).symmetric_difference(set(FullY))
    temp = list(temp)
    # Write a value of 365 for each year missing
    MissingYears = []
    for aRow in temp:
        MissingYears.append(np.nan)
    # Write dataframes for missing years and data covereage within 
    # present records.
    df = pd.DataFrame({"a" : MissingYears, "b" : temp})
    df2 = pd.DataFrame({"a" : AnnualAve, "b" : AnnualYears})
    # Combine these based upon year (ave).
    Tdf = pd.merge(df, df2, how='outer')
    Tdf = Tdf.sort_values('b')
    # Combine these based upon year (STD).
    df3 = pd.DataFrame({"a" : AnnualSTD, "b" : AnnualYears})
    Tdf2 = pd.merge(df, df3, how='outer')
    Tdf2 = Tdf2.sort_values('b')
    # Write these columns to list (order will be sorted in graph)
    AnnualAve = Tdf['a'].values.tolist()
    AnnualYears = Tdf['b'].values.tolist()
    AnnualSTD = Tdf2['a'].values.tolist()
    AnnualYears = np.array(AnnualYears)
    AnnualAve = np.array(AnnualAve)
    AnnualSTD = np.array(AnnualSTD)

    # AnnualYears = np.array(AnnualYears)
    # AnnualAve = np.array(AnnualAve)

    mask = ~np.isnan(AnnualYears) & ~np.isnan(AnnualAve)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Average Temperature (C)')
    ax.set_title('Average Annual Temperature', fontweight='bold')
    plt.plot(AnnualYears,AnnualAve,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(AnnualYears[mask], AnnualAve[mask])
    plt.plot(AnnualYears,intercept+slope*AnnualYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AnnualAve.%s' % (dir, 'Annual', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    AnnualSTD = np.array(AnnualSTD)

    mask = ~np.isnan(AnnualYears) & ~np.isnan(AnnualSTD)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
        horizontalalignment='center', transform=ax.transAxes, fontsize=12,
        fontweight=None, color='black')
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel(NameX)
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Annual Temperature STD', fontweight='bold')
    plt.plot(AnnualYears,AnnualSTD,  '-')
    slope, intercept, r_value, p_value, std_err = stats.linregress(AnnualYears[mask], AnnualSTD[mask])
    plt.plot(AnnualYears,intercept+slope*AnnualYears, 'r')
    ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
        (slope, p_value, r_value), verticalalignment='bottom', 
        horizontalalignment='right', transform=ax.transAxes, fontsize=8)
    plt.savefig('%s/%s/AnnualSTD.%s' % (dir, 'Annual', f), dpi=None, 
        facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
        format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
        frameon=None)
    # plt.show()
    StationExports.append(slope)
    StationExports.append(p_value)
    StationExports.append(r_value)
    plt.close()

    # print ("END of Temperature Analysis")