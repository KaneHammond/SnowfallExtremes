from Analysis import *

# This File processes raw data for analysis
# by removing records without snowfall and 
# defining hydrological years.

Selection = SepData
Latitude = Selection[0][2]
# print (Latitude)
Longitude = Selection[0][3]
# print (Longitude)
Elevation = Selection[0][4]
# print (Elevation)
StationID = Selection[0][0]
# print (StationID)
StationName = Selection[0][1]
# print (StationName)
for aRow in Selection:
    del aRow[0:5]

dir = StationName
if not os.path.exists(dir):
    os.makedirs(StationName)
else:
    shutil.rmtree(dir)
    os.makedirs(dir)

subfolder_names = ['Data_Coverage']
for subfolder_name in subfolder_names:
    os.makedirs(os.path.join(StationName, subfolder_name))

#DATA FORMAT: [Date, Precip, Snow, Tmax, Tmin, TOBS]
# This section does not remove any records. Only converts available data to float.
allData = []
for aRow in Selection:
    splitDateInfo = aRow[0].split('/')
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

#***************************************TRIM YEARS*********************
#***************************************&HYDRO YEARS&*************************
#*****Format [Year, MM, DD, Precip, Snow, Tmax, Tmin, TOBS]
# Defines the hydrological years (Starting in October ending last day of Sepetember)
for aRow in allData:
    if aRow[0] < FirstYear:
        del aRow[:]
hydroYear = 0                   
prevMonth = 0
prevYear = FirstYear
for aRow in allData:
    if aRow[2]==10 and aRow[1]==1:
        hydroYear=hydroYear+1
    elif prevMonth<=9 and aRow[2]>=10:
        hydroYear=hydroYear+1
    elif prevYear!=aRow[0]:
        if aRow[0]!= prevYear+1:
            hydroYear=hydroYear+1
        elif prevMonth<=9:
            hydroYear=hydroYear+1
    aRow.append(hydroYear)
    prevMonth=aRow[2]
    prevYear=aRow[0]

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
RawData = copy.deepcopy(TempDataIndex[:])
TempDataIndex = []
#New Format [Year, DD, MM, Precip, Snow, Tmax, Tmin, TOBS, Hydro Year]

#*******************Data Coverage Analysis**********************
# This section counts the occurrence of months per hydro year

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

MonthsInSet = copy.deepcopy(ListMonthFilt)
ListMonths = []
ListMonths = copy.deepcopy(ListMonthFilt)
ListMonthFilt = []

# This provides a coverage percentage of months
# FHY is final hydro year. Multiplied by 12 represents total number of months expected.
FHY = RawData[-1][-1] 
TotalMonths = float(FHY*12)
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
TotalDays = float(delta.days)


PercentRCov = (Fsum/TotalMonths)*100

plt.figure(figsize=(12,6))
plt.bar(Months, MonthlyCoverage, align='center', alpha=0.5)
plt.gca().yaxis.grid(True)
plt.xticks(Months)
plt.xlabel('Months')
plt.ylabel('Percentage of Coverage')
plt.title('Month Coverage Over Study Period')
plt.text(1, 1.04, 'Total Record Coverage For Study Period: %f' % 
    (PercentRCov), verticalalignment='top') 
plt.savefig('%s/%s/MissingMonthsData.%s' % (StationName, 'Data_Coverage', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

# Provides percentage of daily record coverage for study period
DailyRecordCoverage = float(len(RawData))/TotalDays

# ***************************Missing Temperature Analysis
# ***************************Missing Temperature Analysis
# ***************************Missing Temperature Analysis
MissingTempData = [] # Dataset containing count of missing records per year
Tx = [] # The x axis value set of hydro years
Temp = 0
HY = 1 # Hydro Year

for aRow in RawData:
    if aRow[-1]==HY:   
        if aRow[-2]=="" and aRow[6]=="":
            Temp = Temp+1
        if aRow[-2]=="" and aRow[5]=="":
            Temp = Temp+1
    if aRow[-1]!=HY:
        Tx.append(HY)
        HY = aRow[-1]
        MissingTempData.append(Temp)
        Temp=0
Tx.append(HY)
MissingTempData.append(Temp)
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
plt.savefig('%s/%s/MissingTempData.%s' % (StationName,'Data_Coverage', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()
# print PercentRCov
# print Tx
# print MissingTempData

# ***************************Missing Snowfall Data
# ***************************Missing Snowfall Data
# ***************************Missing Snowfall Data
MissingSnowData = [] # Dataset containing count of missing records per year
Sx = [] # The x axis value set of hydro years
Temp = 0
HY = 1 # Hydro Year

for aRow in RawData:
    if aRow[-1]==HY:   
        if aRow[-5]=="":
            Temp = Temp+1
    if aRow[-1]!=HY:
        Sx.append(HY)
        HY = aRow[-1]
        MissingSnowData.append(Temp)
        Temp=0
Sx.append(HY)
MissingSnowData.append(Temp)
# print Sx
# print MissingSnowData

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
plt.savefig('%s/%s/MissingSnowData.%s' % (StationName,'Data_Coverage', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
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
        if aRow[-6]=="":
            Temp = Temp+1
    if aRow[-1]!=HY:
        Rx.append(HY)
        HY = aRow[-1]
        MissingRainData.append(Temp)
        Temp=0
Rx.append(HY)
MissingRainData.append(Temp)

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
plt.savefig('%s/%s/MissingRainData.%s' % (StationName, 'Data_Coverage', f), dpi=None, 
    facecolor='w', edgecolor='b', orientation='portrait', papertype=None, 
    format=None, transparent=False, bbox_inches=None, pad_inches=0.1, 
    frameon=None)
# plt.show()
plt.close()

#Snow only record
for aRow in RawData:
    if aRow[-5]!=0.0 and aRow[-5] != "":
        TempDataIndex.append(aRow[:])

print "END of SplitData"