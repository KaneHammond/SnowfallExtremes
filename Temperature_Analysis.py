from Analysis import *

dir = StationName+"/Temperature"
if not os.path.exists(dir):
    os.makedirs(StationName+"/Temperature")
else:
    shutil.rmtree(dir)
    os.makedirs(dir)

subfolder_names = ['Monthly', 'Annual', 'Seasonal']
for subfolder_name in subfolder_names:
    os.makedirs(os.path.join(StationName+"/Temperature", subfolder_name))

###TEMP TEMP TEMP TEMP
# CutData contains entire snow season record set of snowfall and 
# liquid precipitation. CutData is in chronological order
# DATA FORMAT [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro]
#************    0   1    2     3     4      5      6    7      8

allData = copy.deepcopy(RawData)
#*****************************Temp only record*******************

# Count Months with average temp available 
CheckDataM = []
for aRow in allData:
    del aRow[3:5]
    CheckDataM.append(aRow[2])

# FORMAT [Year, DD, MM, Tmax, Tmin, TOBS, Hydro]
#***************************Month Averages*********************

# Hydro Year index
i = allData[0][-1]
# Month index
M = allData[0][2]
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


for aRow in allData:
    if index==(len(allData)-1):
        if aRow[3]!="" and aRow[4]!="":
            TempVar = (aRow[3]+aRow[4])/2
            MonthTemp.append(TempVar)
        if aRow[3]!="" or aRow[4]!="":
            MonthTemp.append(np.nan)
            if aRow[5]!="":
                missingHL.append(index)
            if aRow[5]=="":
                NullRecords = NullRecords+1
        YList.append(i)
        MonthList.append(M)
        MonthSTD.append(np.nanstd(MonthTemp))
        MonthAve.append(np.nanmean(MonthTemp))
    if aRow[-1]==i:
        if aRow[2]==M:
            if aRow[3]!="" and aRow[4]!="":
                TempVar = (aRow[3]+aRow[4])/2
                MonthTemp.append(TempVar)
            if aRow[3]!="" or aRow[4]!="":
                MonthTemp.append(np.nan)
                if aRow[5]!="":
                    missingHL.append(index)
                if aRow[5]=="":
                    NullRecords = NullRecords+1
        if aRow[2]!=M:
            MonthList.append(M)
            YList.append(i)
            if len(MonthTemp)!=0:
                MonthSTD.append(np.nanstd(MonthTemp))
                MonthAve.append(np.nanmean(MonthTemp))
            if len(MonthTemp)==0:
                # Manually insert nan value if all data is missing. This
                # prevents Degrees of Freedom error message from printing for
                # for mean and std calculations.
                MonthSTD.append(np.nan)
                MonthAve.append(np.nan)
            MonthTemp = []
            if aRow[3]!="" and aRow[4]!="":
                TempVar = (aRow[3]+aRow[4])/2
                MonthTemp.append(TempVar)
            if aRow[3]!="" or aRow[4]!="":
                MonthTemp.append(np.nan)
                if aRow[5]!="":
                    missingHL.append(index)
                if aRow[5]=="":
                    NullRecords = NullRecords+1
        index = index+1
        M = aRow[2]
    if aRow[-1]!=i:
        MonthList.append(M)
        YList.append(i)
        MonthSTD.append(np.nanstd(MonthTemp))
        MonthAve.append(np.nanmean(MonthTemp))
        index=index+1
        M = aRow[2]
        i = aRow[-1]
        if aRow[3]!="" and aRow[4]!="":
            TempVar = (aRow[3]+aRow[4])/2
            MonthTemp.append(TempVar)
        if aRow[3]!="" or aRow[4]!="":
            MonthTemp.append(np.nan)
            if aRow[5]!="":
                missingHL.append(index)
            if aRow[5]=="":
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
i = allData[0][-1]

for aRow in allData:
    if aRow[-1]==i:
        if aRow[2]==3 or aRow[2]==4 or aRow[2]==5:
            if aRow[-3]!="" and aRow[-4]!="":
                ave = (aRow[-3]+aRow[-4])/2
                TemperTemp.append(ave)
    if aRow[-1]!=i:
        if len(TemperTemp)==0:
            SpringSTD.append(np.nan)
            SpringAve.append(np.nan)
        if len(TemperTemp)!=0:
            SpringSTD.append(np.std(TemperTemp))
            SpringAve.append(np.mean(TemperTemp))
        SpringYears.append(i)
        i = aRow[-1]
        TemperTemp=[]
        if aRow[2]==3 or aRow[2]==4 or aRow[2]==5:
            if aRow[-3]!="" and aRow[-4]!="":
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
i = allData[0][-1]

for aRow in allData:
    if aRow[-1]==i:
        if aRow[2]==6 or aRow[2]==7 or aRow[2]==8:
            if aRow[-3]!="" and aRow[-4]!="":
                ave = (aRow[-3]+aRow[-4])/2
                TemperTemp.append(ave)
    if aRow[-1]!=i:
        if len(TemperTemp)==0:
            SummerSTD.append(np.nan)
            SummerAve.append(np.nan)
        if len(TemperTemp)!=0:
            SummerSTD.append(np.std(TemperTemp))
            SummerAve.append(np.mean(TemperTemp))
        SummerYears.append(i)
        i = aRow[-1]
        TemperTemp=[]
        if aRow[2]==6 or aRow[2]==7 or aRow[2]==8:
            if aRow[-3]!="" and aRow[-4]!="":
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
i = allData[0][-1]

for aRow in allData:
    if aRow[-1]==i:
        if aRow[2]==9 or aRow[2]==10 or aRow[2]==11:
            if aRow[-3]!="" and aRow[-4]!="":
                ave = (aRow[-3]+aRow[-4])/2
                TemperTemp.append(ave)
    if aRow[-1]!=i:
        if len(TemperTemp)==0:
            FallSTD.append(np.nan)
            FallAve.append(np.nan)
        if len(TemperTemp)!=0:
            FallSTD.append(np.std(TemperTemp))
            FallAve.append(np.mean(TemperTemp))
        FallYears.append(i)
        i = aRow[-1]
        TemperTemp=[]
        if aRow[2]==9 or aRow[2]==10 or aRow[2]==11:
            if aRow[-3]!="" and aRow[-4]!="":
                ave = (aRow[-3]+aRow[-4])/2
                TemperTemp.append(ave)
FallSTD.append(np.std(TemperTemp))
FallAve.append(np.mean(TemperTemp))
FallYears.append(i)

if len(FallYears)!= len(FallSTD) or len(FallYears)!= len(FallAve):
    print (" \n******Fall Temperature Analysis Miscalculation******\n ")

#### Winter
WinterAve = []
WinterSTD = []
WinterYears = []
TemperTemp = []
i = allData[0][-1]

for aRow in allData:
    if aRow[-1]==i:
        if aRow[2]==12 or aRow[2]==1 or aRow[2]==2:
            if aRow[-3]!="" and aRow[-4]!="":
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
            if aRow[-3]!="" and aRow[-4]!="":
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
i = allData[0][-1]

for aRow in allData:
    if aRow[-1]==i:
        if aRow[-3]!="" and aRow[-4]!="":
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
        if aRow[-3]!="" and aRow[-4]!="":
            ave = (aRow[-3]+aRow[-4])/2
            TemperTemp.append(ave)
AnnualSTD.append(np.std(TemperTemp))
AnnualAve.append(np.mean(TemperTemp))
AnnualYears.append(i)

if len(AnnualYears)!= len(AnnualSTD) or len(AnnualYears)!= len(AnnualAve):
    print (" \n******Annual Temperature Analysis Miscalculation******\n ")


#***************************************** Month Graphing
#***************************************** Month Graphing
#***************************************** Month Graphing
#***************************************** Month Graphing

# January
YearsJan = np.array(YearsJan)
JanAve = np.array(JanAve)

mask = ~np.isnan(YearsJan) & ~np.isnan(JanAve)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
    fontweight=None, color='black')
fig.subplots_adjust(top=0.85)
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for January', fontweight='bold')
plt.plot(YearsJan,JanAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJan[mask], JanAve[mask])
plt.plot(YearsJan,intercept+slope*YearsJan, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JanuaryAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for January', fontweight='bold')
plt.plot(YearsJan,JanSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJan[mask], JanSTD[mask])
plt.plot(YearsJan,intercept+slope*YearsJan, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JanuarySTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# February
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for February', fontweight='bold')
plt.plot(YearsFeb,FebAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsFeb[mask], FebAve[mask])
plt.plot(YearsFeb,intercept+slope*YearsFeb, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/FebruaryAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for February', fontweight='bold')
plt.plot(YearsFeb,FebSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsFeb[mask], FebSTD[mask])
plt.plot(YearsFeb,intercept+slope*YearsFeb, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/FebruarySTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()


# March
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for March', fontweight='bold')
plt.plot(YearsMar,MarAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMar[mask], MarAve[mask])
plt.plot(YearsMar,intercept+slope*YearsMar, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/MarchAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for March', fontweight='bold')
plt.plot(YearsMar,MarSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMar[mask], MarSTD[mask])
plt.plot(YearsMar,intercept+slope*YearsMar, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/MarchSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()


# April
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for April', fontweight='bold')
plt.plot(YearsApr,AprAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsApr[mask], AprAve[mask])
plt.plot(YearsApr,intercept+slope*YearsApr, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AprilAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for April', fontweight='bold')
plt.plot(YearsApr,AprSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsApr[mask], AprSTD[mask])
plt.plot(YearsApr,intercept+slope*YearsApr, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AprilSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()


# May
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for May', fontweight='bold')
plt.plot(YearsMay,MayAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMay[mask], MayAve[mask])
plt.plot(YearsMay,intercept+slope*YearsMay, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/MayAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for May', fontweight='bold')
plt.plot(YearsMay,MaySTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsMay[mask], MaySTD[mask])
plt.plot(YearsMay,intercept+slope*YearsMay, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/MaySTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()


# June
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for June', fontweight='bold')
plt.plot(YearsJun,JunAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJun[mask], JunAve[mask])
plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JuneAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for June', fontweight='bold')
plt.plot(YearsJun,JunSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJun[mask], JunSTD[mask])
plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JuneSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()


# July
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for July', fontweight='bold')
plt.plot(YearsJul,JulAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulAve[mask])
plt.plot(YearsJul,intercept+slope*YearsJul, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JulyAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for July', fontweight='bold')
plt.plot(YearsJul,JulSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulSTD[mask])
plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/JulySTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# August
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for August', fontweight='bold')
plt.plot(YearsAug,AugAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsAug[mask], AugAve[mask])
plt.plot(YearsAug,intercept+slope*YearsAug, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AugustAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for August', fontweight='bold')
plt.plot(YearsAug,AugSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsAug[mask], AugSTD[mask])
plt.plot(YearsAug,intercept+slope*YearsAug, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AugustSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# September
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for September', fontweight='bold')
plt.plot(YearsSep,SepAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsSep[mask], SepAve[mask])
plt.plot(YearsSep,intercept+slope*YearsSep, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SeptemberAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for September', fontweight='bold')
plt.plot(YearsSep,SepSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsSep[mask], SepSTD[mask])
plt.plot(YearsSep,intercept+slope*YearsSep, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SeptemberSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# October
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for October', fontweight='bold')
plt.plot(YearsOct,OctAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsOct[mask], OctAve[mask])
plt.plot(YearsOct,intercept+slope*YearsOct, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/OctoberAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for October', fontweight='bold')
plt.plot(YearsOct,OctSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsOct[mask], OctSTD[mask])
plt.plot(YearsOct,intercept+slope*YearsOct, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/OctoberSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# November
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for November', fontweight='bold')
plt.plot(YearsNov,NovAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsNov[mask], NovAve[mask])
plt.plot(YearsNov,intercept+slope*YearsNov, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/NovemberAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for November', fontweight='bold')
plt.plot(YearsNov,NovSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsNov[mask], NovSTD[mask])
plt.plot(YearsNov,intercept+slope*YearsNov, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/NovemberSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# December
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Monthly Temperature for December', fontweight='bold')
plt.plot(YearsDec,DecAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsDec[mask], DecAve[mask])
plt.plot(YearsDec,intercept+slope*YearsDec, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/DecemberAve.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Monthly Temperature STD for December', fontweight='bold')
plt.plot(YearsDec,DecSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsDec[mask], DecSTD[mask])
plt.plot(YearsDec,intercept+slope*YearsDec, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/DecemberSTD.%s' % (StationName, 'Temperature', 'Monthly', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# *******************************Seasonal Graphing 
# *******************************Seasonal Graphing 
# *******************************Seasonal Graphing 
# *******************************Seasonal Graphing 
# Summer
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Summer Season Temperature', fontweight='bold')
plt.plot(SummerYears,SummerAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(SummerYears[mask], SummerAve[mask])
plt.plot(SummerYears,intercept+slope*SummerYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SummerAve.%s' % (StationName, 'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Summer Temperature STD', fontweight='bold')
plt.plot(SummerYears,SummerSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(SummerYears[mask], SummerSTD[mask])
plt.plot(SummerYears,intercept+slope*SummerYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SummerSTD.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Fall Season Temperature', fontweight='bold')
plt.plot(FallYears,FallAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(FallYears[mask], FallAve[mask])
plt.plot(FallYears,intercept+slope*FallYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/FallAve.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Fall Temperature STD', fontweight='bold')
plt.plot(FallYears,FallSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(FallYears[mask], FallSTD[mask])
plt.plot(FallYears,intercept+slope*FallYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/FallSTD.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Winter Season Temperature', fontweight='bold')
plt.plot(WinterYears,WinterAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(WinterYears[mask], WinterAve[mask])
plt.plot(WinterYears,intercept+slope*WinterYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/WinterAve.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Winter Temperature STD', fontweight='bold')
plt.plot(WinterYears,WinterSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(WinterYears[mask], WinterSTD[mask])
plt.plot(WinterYears,intercept+slope*WinterYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/WinterSTD.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# Spring
SpringYears = np.array(SpringYears)
SpringAve = np.array(SpringAve)

mask = ~np.isnan(SpringYears) & ~np.isnan(SpringAve)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
    fontweight=None, color='black')
fig.subplots_adjust(top=0.85)
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Spring Season Temperature', fontweight='bold')
plt.plot(SpringYears,SpringAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(SpringYears[mask], SpringAve[mask])
plt.plot(SpringYears,intercept+slope*SpringYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SpringAve.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Spring Temperature STD', fontweight='bold')
plt.plot(SpringYears,SpringSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(SpringYears[mask], SpringSTD[mask])
plt.plot(SpringYears,intercept+slope*SpringYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/SpringSTD.%s' % (StationName,'Temperature', 'Seasonal', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# ********************************Annual Graphing
# ********************************Annual Graphing
# ********************************Annual Graphing
# ********************************Annual Graphing

AnnualYears = np.array(AnnualYears)
AnnualAve = np.array(AnnualAve)

mask = ~np.isnan(AnnualYears) & ~np.isnan(AnnualAve)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.text(.5, 1.1, 'Station: %s' % (StationName), verticalalignment='center', 
    horizontalalignment='center', transform=ax.transAxes, fontsize=12,
    fontweight=None, color='black')
fig.subplots_adjust(top=0.85)
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Average Temperature (C)')
ax.set_title('Average Annual Temperature', fontweight='bold')
plt.plot(AnnualYears,AnnualAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(AnnualYears[mask], AnnualAve[mask])
plt.plot(AnnualYears,intercept+slope*AnnualYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AnnualAve.%s' % (StationName,'Temperature', 'Annual', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
ax.set_xlabel('Hydro Year')
ax.set_ylabel('Standard Deviation')
ax.set_title('Annual Temperature STD', fontweight='bold')
plt.plot(AnnualYears,AnnualSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(AnnualYears[mask], AnnualSTD[mask])
plt.plot(AnnualYears,intercept+slope*AnnualYears, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/%s/%s/AnnualSTD.%s' % (StationName,'Temperature', 'Annual', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

print ("END of Temperature Analysis")