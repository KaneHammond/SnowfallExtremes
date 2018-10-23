
from BasicImports import *

sys.path.append("PythonFiles")
sys.path.append("INPUT_DATA")
sys.path.append("INPUT_DATA/Output")

# Determine data location based upon data download method
FilterOptions = ['Country', 'Station/City', 'State/Province', 'Coordinates']
df = pd.DataFrame(FilterOptions,index=[1, 2, 3, 4], columns = ["SELECTION PARAMETERS"])
print df
print(' \n**********CHOOSE DATA SELECTION METHOD**********\n ')
selection = 'INDEX'           
Data = 'SELECTION PARAMETERS'
query = input('Which method was used to download the data?:')
query = int(query)

# # Autorun
# query = 2

# Write main output folder
dir = 'Output'
if not os.path.exists(dir):
    os.makedirs(dir)



# Return csv of stations from query.
if query>4 or query < 0:
  print ('Choice Not Within Range')
  sys.exit()

if query==1:
  # Choose the file path specific to output from download type
  sys.path.append("INPUT_DATA/Output/Country")
  # Choose station information specific to download type
  allStations = pd.read_csv("INPUT_DATA/Output/Country/StationInformation.csv",
    header=0)
  # Define the path for station daily records to be imported from (csv)
  Import_Path = 'INPUT_DATA/Output/Country/'

if query==2:
  sys.path.append("INPUT_DATA/Output/Station")
  allStations = pd.read_csv("INPUT_DATA/Output/Station/StationInformation.csv",
    header=0)
  Import_Path = 'INPUT_DATA/Output/Station/'

if query==3:
  sys.path.append("INPUT_DATA/Output/State_Province")
  # inFile = open('INPUT_DATA/Output/State_Province/StationInformation.csv', 'r')
  allStations = pd.read_csv("INPUT_DATA/Output/State_Province/StationInformation.csv",
    header=0, index_col=False)
  Import_Path = 'INPUT_DATA/Output/State_Province/'

if query==4:
  print('Currently Unavailable')
  sys.exit()

# Define lists of variables to be indexed and used for 
# the looping analysis
# print allStations
Path = 0
if query == 3:
  Path = 3
  Stations = allStations['STATION_ID'].tolist()
  States = allStations['STATE'].tolist()
  StationNames = allStations['STATION_NAME'].tolist()
  Country = allStations['COUNTRY_CODE'].tolist()
  Elevation = allStations['ELEVATION'].tolist()
  Lat = allStations['LATITUDE'].tolist()
  Long = allStations['LONGITUDE'].tolist()
if query == 1:
  Path = 1
  Stations = allStations['STATION_ID'].tolist()
  # StationNames = allStations['STATION_NAME'].tolist()
  Country = allStations['COUNTRY_CODE'].tolist()
  Elevation = allStations['Unnamed: 0'].tolist()
  Lat = allStations['LATITUDE'].tolist()
  Long = allStations['LONGITUDE'].tolist()
if query == 2:
  Path = 2
  Data = list(allStations.columns.values)
  Stations = Data[-1]
  Name = Data[1]

# Autorun
# SE = 0.95
# f = 'pdf'
# FirstYear = 1950
# FinalYear = 2016
# YearLabel = 'Year'
# Prompt options for analysis
print ('*'*25)
# Define the cdf limit for the snowfall extremes
query = input('Select CDF Limit For Snowfall Extremes (i.e. 0.95):')
SE = float(query)
print ('*'*25)
# Choose file extension for graphing outputs
query = raw_input('Define File Extention For Saved Figures (i.e. pdf):')
f = str(query)
print ('*'*25)
# Define start year for clipping data
query = input('Define Starting Year for Analysis (YYYY):')
FirstYear = int(query)
if FirstYear > 2018:
  print('%i Not a Valid Year' % (FirstYear))
print ('*'*25)
# Define final year for clipping data
query = input('Define Final Year for Analysis (YYYY):')
FinalYear = int(query)
if FinalYear > 2018:
  print('%i Not a Valid Year' % (FinalYear))
print ('*'*25)
# Choose label for x-axis on graphing outputs using the custom
# year clip (MonthX and Dayx).
query = raw_input('Define Year Labels for x-axis on Figures (i.e. Hydro Year):')
YearLabel = str(query)

# Not Written in as an option yet. This selects day and month to parse
# the data by. 
MonthX = 10
Dayx = 1


# Define final output header. Lenght determines if
# records will be rejected.
Header = ['Station', 'State', 'Country', 'Elevation', 
  'Lat', 'Long', 'MonthCov', 'DailyCov', 'TempCov', 
  'SnowCov', 'RainCov', 'Min CDF', 'Day Start Slp',
  'Day Start Pval', 'Day Start Rval', 'Day End Slp',
  'Day End Pval', 'Day End Rval', 'Snow S len Slp',
  'Snow S len Pval', 'Snow S len Rval', 'Extrm Evnt Slp',
  'Extrm Evnt Pval', 'Extrm Evnt Rval', 'Tot Snw Dy Slp',
  'Tot Snw Dy Pval', 'Tot Snw Dy Rval', 'Ann Snw Ttl Slp',
  'Ann Snw Ttl Pval', 'Ann Snw Ttl Rval', 'Ann Snw STD Slp',
  'Ann Snw STD Pval', 'Ann Snw STD Rval', 'MissingSnowYear',
  'JanAve Slp', 'JanAve Pval', 'JanAve Rval', 
  'JanSTD Slp', 'JanSDT Pval', 'JanSTD Rval',
  'FebAve Slp', 'FebAve Pval', 'FebAve Rval', 
  'FebSTD Slp', 'FebSDT Pval', 'FebSTD Rval',
  'MarAve Slp', 'MarAve Pval', 'MarAve Rval', 
  'MarSTD Slp', 'MarSDT Pval', 'MarSTD Rval',
  'AprAve Slp', 'AprAve Pval', 'AprAve Rval', 
  'AprSTD Slp', 'AprSDT Pval', 'AprSTD Rval',
  'MayAve Slp', 'MayAve Pval', 'MayAve Rval', 
  'MaySTD Slp', 'MaySDT Pval', 'MaySTD Rval',
  'JunAve Slp', 'JunAve Pval', 'JunAve Rval', 
  'JunSTD Slp', 'JunSDT Pval', 'JunSTD Rval',
  'JulAve Slp', 'JulAve Pval', 'JulAve Rval', 
  'JulSTD Slp', 'JulSDT Pval', 'JulSTD Rval',
  'AugAve Slp', 'AugAve Pval', 'AugAve Rval', 
  'AugSTD Slp', 'AugSDT Pval', 'AugSTD Rval',
  'SepAve Slp', 'SepAve Pval', 'SepAve Rval', 
  'SepSTD Slp', 'SepSDT Pval', 'SepSTD Rval',
  'OctAve Slp', 'OctAve Pval', 'OctAve Rval', 
  'OctSTD Slp', 'OctSDT Pval', 'OctSTD Rval',
  'NovAve Slp', 'NovAve Pval', 'NovAve Rval', 
  'NovSTD Slp', 'NovSDT Pval', 'NovSTD Rval',
  'DecAve Slp', 'DecAve Pval', 'DecAve Rval', 
  'DecSTD Slp', 'DecSDT Pval', 'DecSTD Rval',
  'SummerAve Slp', 'SummerAve Pval', 'SummerAve Rval', 
  'SummerSTD Slp', 'SummerSDT Pval', 'SummerSTD Rval',
  'FallAve Slp', 'FallAve Pval', 'FallAve Rval', 
  'FallSTD Slp', 'FallSDT Pval', 'FallSTD Rval',
  'WinterAve Slp', 'WinterAve Pval', 'WinterAve Rval', 
  'WinterSTD Slp', 'WinterSDT Pval', 'WinterSTD Rval',
  'SpringAve Slp', 'SpringAve Pval', 'SpringAve Rval', 
  'SpringSTD Slp', 'SpringSDT Pval', 'SpringSTD Rval',
  'AnnualAve Slp', 'AnnualAve Pval', 'AnnualAve Rval', 
  'AnnualSTD Slp', 'AnnualSDT Pval', 'AnnualSTD Rval']



# Start Loop
CheckRecords = []
FinalData = []
i = 0
if Path != 2:
  ProgBarLimit = len(Stations)
if Path == 2:
  ProgBarLimit = 1
print ('Initiating Analysis...')
for i in tqdm.tqdm(range(ProgBarLimit)):
  OmitYearsT = []
  SnowData = []
  RawData = []
  BaseData = []
  StationExports = []
  if Path == 1:
    StationExports.append(Stations[i])
    # Insert a null for state column.
    # Data download/prep does not include a state section
    # when downloading data only by country/latitude.
    StationExports.append('null')
    StationExports.append(Country[i])
    StationExports.append(Elevation[i])
    StationExports.append(Lat[i])
    StationExports.append(Long[i])
    StationName = Stations[i]
    # StationExports.append(Stations[i])
    State = Country[i]
  if Path == 2:
    StationExports.append(Stations)
    StationExports.append('null')
    StationExports.append('null')
    StationExports.append('null')
    StationExports.append('null')
    StationExports.append('null')
    StationName = Name
  if Path == 3:
    StationExports.append(Stations[i])
    StationExports.append(States[i])
    StationExports.append(Country[i])
    StationExports.append(Elevation[i])
    StationExports.append(Lat[i])
    StationExports.append(Long[i])
    StationName = StationNames[i]
    State = States[i]
  # Select stations from state folders using StationInformation.csv
  # State = States[i]
  # Read specific station (Stations[i]=Station) at given state path
  if Path == 3 or Path == 1:
    Data = pd.read_csv((Import_Path+State+'/'+Stations[i]+'.csv'), header=0)
  if Path == 2:
    Data = pd.read_csv((Import_Path+'/'+Stations+'.csv'), header=0)
  

  # Format to meet current program design ([Date, PRCP, SNOW, TMAX, TMIN, TOBS])
  Data = Data.drop(columns=['ID', 'YEAR', 'MONTH', 'DAY'])
  try:
    Data = Data[['MM/DD/YYYY', 'PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS']]
  except:
    Data = Data[['MM/DD/YYYY', 'SNOW', 'TMAX', 'TMIN']]
    Data['PRCP'] = np.nan
    Data['TOBS'] = np.nan
    Data = Data[['MM/DD/YYYY', 'PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS']]

  # Fill in missing dates with nan records to close data gaps.

  # Define range of dates in dataset
  index = Data['MM/DD/YYYY']
  index = index.values.tolist()
  Date1 = datetime.strptime(index[0], '%Y-%m-%d')
  Date2 = datetime.strptime(index[-1], '%Y-%m-%d')

  # Write list of dates found in raw data. Converts it to datetime
  # so it can be compared to find missing dates.
  indexForm = []
  for aItem in index:
    aItem = datetime.strptime(aItem, '%Y-%m-%d')
    aItem = str(aItem)
    indexForm.append(aItem)

  # Write a full list of dates that occured between the start
  # and end date of raw data. Already in datetime format.
  idx = pd.date_range(Date1, Date2)
  idxForm = []
  for aItem in idx:
    aItem=str(aItem)
    idxForm.append(aItem)

  # Determine the difference between the lists. This identifies missing 
  # years in the data to later fill with null values. Datetime format
  # is required to compare the sets.

  # Python code the get difference of two lists 
  # Not using set()
  list2 = idxForm
  list1 = indexForm
  def diff(list1, list2):
      c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
      d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
      return list(c - d)
  
  # Write list of dates only found in full date recordset. Then fill
  # the dataframe with nan values.
  diff = (diff(list1, list2))
  df = pd.DataFrame({'NewDate' : diff})
  df['PRCP'] = np.nan
  df['SNOW'] = np.nan
  df['TMAX'] = np.nan
  df['TMIN'] = np.nan
  df['TOBS'] = np.nan

  # New df of full dates
  df2 = pd.DataFrame({'Date' : idxForm})
  df2['NewDate'] = df2['Date']
  FullDate = df2['NewDate'].tolist()
  FormatedDate = df2['Date'].tolist()

  # Functions wont read dates before 1900,
  # used for loop to parse date manually.
  # Required since pandas wouldn't convert
  # all date records to correct format. This appends
  # a string of only the year-month-day. Drops
  # the hour-minute-second extension.
  Fix = []
  for aItem in FormatedDate:
    date = aItem[0:10]
    Fix.append(date)

  # Prep the fixed dates for merge. This combines
  # the re-formatted dates with the initial format
  # for the dataframe to be merged with.
  df2 = []
  df2 = pd.DataFrame({'NewDate' : FullDate})
  df3 = pd.DataFrame({'FixedDate' : Fix})
  df4 = df2.join(df3, how='outer')

  # This list is equivalent to the dates already in the set.
  # due to format issue, the dates had to be processed seprately.
  # This inserts a copy of the dates present, but in a different format.
  # (Formatted as indexForm)
  Data['NewDate'] = list1
 
  # Merge Data with the df containing the missing data. This
  # writes DataFull.
  DataFull = df.merge(Data, on='NewDate',
                 how='outer', suffixes=('', '_y'))
  DataFull['MM/DD/YYYY'] = pd.to_datetime(DataFull['NewDate'])

  # Index by datetime format
  DataFull = DataFull.set_index('NewDate')
  DataFull = DataFull.sort_index()

  # Drop basic columns. Pandas merge format changed the format of 
  # named columns. Renamed below back to basic format.
  DataFull = DataFull.drop(columns=['PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS'])
  DataFull['MM/DD/YYYY'] = DataFull['MM/DD/YYYY'].astype(str)
  DataFull = DataFull.rename(columns={'PRCP_y': 'PRCP', 'SNOW_y': 'SNOW', 'TMAX_y': 'TMAX', 'TMIN_y': 'TMIN', 'TOBS_y': 'TOBS'})
  
  # Merge the dates in correct format to main dataframe
  DataFull = pd.merge(DataFull, df4, on='NewDate', how='outer')
  DataFull = DataFull.drop(columns=['NewDate', 'MM/DD/YYYY'])
  DataFull = DataFull[['FixedDate', 'PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS']]
  # Convert to meet prior format standard
  Data = DataFull



  # Convert data from 10ths to full value
  Data['TOBS'] = Data['TOBS'].apply(lambda x: x/10)
  Data['TMIN'] = Data['TMIN'].apply(lambda x: x/10)
  Data['TMAX'] = Data['TMAX'].apply(lambda x: x/10)
  Data = Data.values.tolist()
  # Loop analysis
  # Specified to pass stations with errors
  if Path != 2:
    try:
      from SplitData import *
      Split_Data(Data, StationName, f, FirstYear, SnowData, RawData, BaseData, MonthX, Dayx, StationExports, OmitYearsT, FinalYear)
    except:
      pass
    try:
      from Snowfall_Analysis import *
      SnowFallAnalysis(StationName, SnowData, RawData, SE, f, StationExports, Dayx, MonthX, YearLabel)
    except:
      pass
    try:
      from Temperature_Analysis import *
      Temperature(RawData, StationName, f, BaseData, StationExports, OmitYearsT, YearLabel)
      # FinalData.append(StationExports)
    except:
      pass
    if len(StationExports)==len(Header):
      FinalData.append(StationExports)
    if len(StationExports)!=len(Header):
      CheckRecords.append(Stations[i])
  # This path will not force errors to pass for later analysis.
  # Purpose is to run troubled stations individually to define where
  # errors are occuring.
  if Path == 2:
    # Print to move response away from loading bar
    # print ('\n')
    from SplitData import *
    Split_Data(Data, StationName, f, FirstYear, SnowData, RawData, BaseData, MonthX, Dayx, StationExports, OmitYearsT, FinalYear)

    from Snowfall_Analysis import *
    SnowFallAnalysis(StationName, SnowData, RawData, SE, f, StationExports, Dayx, MonthX, YearLabel)

    from Temperature_Analysis import *
    Temperature(RawData, StationName, f, BaseData, StationExports, OmitYearsT, YearLabel)
    # FinalData.append(StationExports)
    if len(StationExports)==len(Header):
      FinalData.append(StationExports)
    if len(StationExports)!=len(Header):
      CheckRecords.append(Stations[i])
    i = i+1

if Path != 2:
  print ('Writting Output File...')
  with open("Output/TotalOutSO.csv", "w") as fp:
    a = csv.writer(fp, delimiter=',', lineterminator='\n')
    FinalData.insert(0, Header)
    data = FinalData
    a.writerows(data)

if Path == 2:
  print ('Writting Output File...')
  with open("Output/%s/TotalOutSO.csv" % (Name), "w") as fp:
    a = csv.writer(fp, delimiter=',', lineterminator='\n')
    FinalData.insert(0, Header)
    data = FinalData
    a.writerows(data)

if len(CheckRecords)>0:
  if Path == 2:
    print('Station Rejected')
    sys.exit()
  print ('Writting Rejected Stations File...')
  if Path != 2:
    with open("Output/ERROR_STATIONS.csv", "w") as fp:
      a = csv.writer(fp)
      data = CheckRecords
      a.writerow(data)



    

