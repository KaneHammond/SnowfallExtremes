from Analysis import *
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
#*****************************************Month Average Analysis
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
plt.savefig('%s/JanuaryAve.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/JanuarySTD.%s' % (StationName, f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

###***************Is this one OK??
# fig, ax1 = plt.subplots(figsize=(13, 8))
# ax1.plot(YearsJan, JanAve, label = 'Average Temperature', color='blue')

# ax2 = ax1.twinx()
# ax2.plot(YearsJan, JanSTD, label = 'Monthly STD', color='red', linestyle='dashed', alpha=0.4)

# slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJan[mask], JanAve[mask])
# ax1.plot(YearsJan,intercept+slope*YearsJan, 'r')
# ax1.text(.95, .25, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
#     (slope, p_value, r_value), verticalalignment='bottom', 
#     horizontalalignment='right', transform=ax.transAxes, fontsize=8)
# #LABEL
# ax2.legend(loc='upper right')
# ax1.legend(loc='upper left')
# ax1.set_title('January Average Temperature')
# ax1.set_xlabel('Year')
# ax1.set_ylabel('Degrees Celsius')
# ax2.set_ylabel('Standard Deviation')
# # ax2.set_ylim(ax.get_ylim())
# ax1.grid(True)
# fig.autofmt_xdate()
# # plt.legend(loc='upper left')
# plt.xticks(rotation=90)
# # plt.show()
# # plt.savefig('SST_RecentData.pdf')
# plt.close()


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
plt.savefig('%s/FebruaryAve.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/FebruarySTD.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/MarchAve.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/MarchSTD.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/AprilAve.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/AprilSTD.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/MayAve.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/MaySTD.%s' % (StationName, f), dpi=None, 
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
plt.savefig('%s/JuneAve.%s' % (StationName, f), dpi=None, 
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
ax.set_title('Monthly Temperature STD for May', fontweight='bold')
plt.plot(YearsJun,JunSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJun[mask], JunSTD[mask])
plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/MaySTD.%s' % (StationName, f), dpi=None, 
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
ax.set_title('Average Monthly Temperature for June', fontweight='bold')
plt.plot(YearsJul,JulAve,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulAve[mask])
plt.plot(YearsJul,intercept+slope*YearsJul, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/JuneAve.%s' % (StationName, f), dpi=None, 
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
ax.set_title('Monthly Temperature STD for May', fontweight='bold')
plt.plot(YearsJul,JulSTD,  '-')
slope, intercept, r_value, p_value, std_err = stats.linregress(YearsJul[mask], JulSTD[mask])
plt.plot(YearsJun,intercept+slope*YearsJun, 'r')
ax.text(0.95, 0.01, 'Trendline Slope: %f P Value: %f RSqrd Value: %f' % 
    (slope, p_value, r_value), verticalalignment='bottom', 
    horizontalalignment='right', transform=ax.transAxes, fontsize=8)
plt.savefig('%s/MaySTD.%s' % (StationName, f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()