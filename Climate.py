
from BasicImports import *

sys.path.append("PythonFiles")
sys.path.append("INPUT_DATA")
sys.path.append("INPUT_DATA/Output")

############################# Mute for autorun
# Determine data location based upon data download method
FilterOptions = ['Country', 'Station/City', 'State/Province']
df = pd.DataFrame(FilterOptions,index=[1, 2, 3], columns = ["SELECTION PARAMETERS"])
print df
print(' \n**********CHOOSE DATA SELECTION METHOD**********\n ')
selection = 'INDEX'           
Data = 'SELECTION PARAMETERS'
query = input('Which method was used to download the data?:')
query = int(query)
############################ Mute for autorun

# Autorun
# query = 2

# Write main output folder
dir = 'Output'
if not os.path.exists(dir):
    os.makedirs(dir)

# Return csv of stations from query.
if query>3 or query < 0:
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

# Time Variables. SE, MonthX, and DayX are specific to Snowfall and Temperature.
# Annual temperature trends will be calculated using the same year setup.
SE = 0.95
f = 'png'
FirstYear = 1965
FinalYear = 2018
YearLabel = 'Year'
MonthX = 7
# Define Day each month will start at for MonthX
Dayx = 1

############################## Mute for autorun

# # Prompt options for analysis
# print ('*'*25)
# # Define the cdf limit for the snowfall extremes
# query = input('Select CDF Limit For Snowfall Extremes (i.e. 0.95):')
# SE = float(query)
# print ('*'*25)
# # Choose file extension for graphing outputs
# query = raw_input('Define File Extention For Saved Figures (i.e. pdf):')
# f = str(query)
# print ('*'*25)
# # Define start year for clipping data
# query = input('Define Starting Year for Analysis (YYYY):')
# FirstYear = int(query)
# if FirstYear > 2018:
#   print('%i Not a Valid Year' % (FirstYear))
# print ('*'*25)
# # Define final year for clipping data
# query = input('Define Final Year for Analysis (YYYY):')
# FinalYear = int(query)
# if FinalYear > 2018:
#   print('%i Not a Valid Year' % (FinalYear))

# print ('*'*25)
# # Choose MonthX, the month that will be the first month of each year
# print ('Re-structure analysis years. For example, choose 1 (January) for standard years\nor 10 for Hydrological years.\n')
# query = raw_input('Define First Month of Each Year:')
# MonthX = int(query)
# # Not Written in as an option yet. This selects day and month to parse
# # the data by. 
# # MonthX = 7
# print ('*'*25)
# # Choose label for x-axis on graphing outputs using the custom
# # year clip (MonthX and Dayx).
# query = raw_input('Define Year Labels for x-axis on Figures (i.e. Hydro Year):')
# YearLabel = str(query)


# Define final output header. Length determines if
# records will be rejected.
Header = ['Station', 'State', 'Country', 'Elevation',
  # Basic Station information and data coverage  
  'Lat', 'Long', 'MonthCov', 'DailyCov', 'TempCov',
  # Min CDF is snowfall mm limit for that station, 3yr average
  # extreme evetns is next. Followed by the 5 and 9 year moving EE ave. 
  'SnowCov', 'RainCov', 'Min CDF', '3yrAveSEE Slp', 
  '3yrAveSEE Pval', '3yrAveSEE Rval', '5yrAveSEE Slp', 
  '5yrAveSEE Pval', '5yrAveSEE Rval','9yrAveSEE Slp', 
  # The day end and starts refer to the beginning of a snow season
  # as well as its end. Leading into the lenght of the season.
  '9yrAveSEE Pval', '9yrAveSEE Rval','Day Start Slp',
  'Day Start Pval', 'Day Start Rval', 'Day End Slp',
  'Day End Pval', 'Day End Rval', 'Snow S len Slp',
  # Extreme events here are per annum, not a rolling average.
  'Snow S len Pval', 'Snow S len Rval', 'Extrm Evnt Slp',
  # Total snow days per year is given below
  'Extrm Evnt Pval', 'Extrm Evnt Rval', 'Tot Snw Dy Slp',
  # Annual snowfall totals are graphed, followed by moving 
  # averages of 3, 5, and 9 years
  'Tot Snw Dy Pval', 'Tot Snw Dy Rval', 'Ann Snw Ttl Slp',
  'Ann Snw Ttl Pval', 'Ann Snw Ttl Rval', '3yrAveSf Slp',
  '3yrAveSf Pval', '3yrAveSf Rval', '5yrAveSf Slp',
  '5yrAveSf Pval', '5yrAveSf Rval','9yrAveSf Slp',
  # The annual STD for snow events is graphed, followed by missing
  # snow years, or years of no snow.
  '9yrAveSf Pval', '9yrAveSf Rval','Ann Snw STD Slp',
  'Ann Snw STD Pval', 'Ann Snw STD Rval', 'MissingSnowYear',
  # Temperature data, monthly followed by season.
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
  # Annual temperature is based upon the snowfall clip date
  # this means the year goes from July to June of the following year.
  # This was done to focus the average over the fall, winter, and spring 
  # seasons.
  'AnnualAve Slp', 'AnnualAve Pval', 'AnnualAve Rval', 
  'AnnualSTD Slp', 'AnnualSDT Pval', 'AnnualSTD Rval',
  # Precipitation is part of the Seasonality analysis. 
  # Includes both solid and liquid precip. The years used for this
  # are standard.
  'SprPrecip', 'SumPrecip', 'FallPrecip', 'WinPrecip',
  'WinSsn Slp', 'WinSsn Pval', 'WinSsn Rval', 'SprSsn Slp',
  'SprSsn Pval', 'SprSsn Rval', 'SumSsn Slp', 'SumSsn Pval',
  'SumSsn Rval', 'FallSsn Slp', 'FallSsn Pval', 'FallSsn Rval',
  'Ave3SI Slp', 'Ave3SI Pval', 'Ave3SI Rval', 'Ave5SI Slp', 
  'Ave5SI Pval', 'Ave5SI Rval', 'Ave9SI Slp', 'Ave9SI Pval', 
  'Ave9SI Rval','Ave3Precip Slp',
  'Ave3Precip Pval','Ave3Precip Rval', 'Ave6Precip Slp',
  'Ave6Precip Pval','Ave6Precip Rval', 'Ave9Precip Slp',
  # Rainfall is analyzed after Seasonality, the years used for this
  # are standard.
  'Ave9Precip Pval','Ave9Precip Rval', 'AnnualRain Slp', 
  'AnnualRain Pval', 'AnnualRain Rval', '3yrAveRain Slp', 
  '3yrAveRain Pval', '3yrAveRain Rval', '5yrAveRain Slp', 
  '5yrAveRain Pval', '5yrAveRain Rval', '9yrAveRain Slp', 
  '9yrAveRain Pval', '9yrAveRain Rval', 'AREE Slp', 'AREE Pval',
  'AREE Rval', '3AveREE Slp', '3AveREE Pval', '3AveREE Rval',
  '5AveREE Slp', '5AveREE Pval', '5AveREE Rval', '9AveREE Slp', 
  '9AveREE Pval', '9AveREE Rval']



# Start Loop
CheckRecords = []
FinalData = []
i = 0
if Path != 2:
  ProgBarLimit = len(Stations)
if Path == 2:
  ProgBarLimit = 1
print ('\n')
print ('Initiating Analysis...')
for i in tqdm.tqdm(range(ProgBarLimit)):
  # Years for temperature to omit
  OmitYearsT = []
  # Data cut for analysis
  RawData = []
  # Uncut data
  BaseData = []
  # Main export location for station analysis data
  StationExports = []
  # Stats for missing snowfall records per winter season
  WinterStats = []
  # Years for Winter stats
  WSY = []
  # Define set for missing snow records per winter season.
  # Modified in Split Data
  MissingSnowData = []
  # Write a list for season rejected containing one snow day
  SingleYearSnowfall = []
  # Write list for number of ee events per year
  EE = []
  # Export list for the majority of snowfall data
  StandardSnow = []

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
  
  # Format to meet current program design ([Date, PRCP, SNOW, TMAX, TMIN])
  Data = Data.drop(['ID', 'YEAR', 'MONTH', 'DAY'], axis=1)
  try:
    Data = Data[['MM/DD/YYYY', 'PRCP', 'SNOW', 'TMAX', 'TMIN']]
  except:
    if 'PRCP' not in Data:
      Data['PRCP'] = np.nan
    if 'TMAX' not in Data:
      Data['TMAX'] = np.nan
    if 'TMIN' not in Data:
      Data['TMIN'] = np.nan
    Data = Data[['MM/DD/YYYY', 'PRCP', 'SNOW', 'TMAX', 'TMIN']]
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

  def diff(list1, list2):
      c = set(list1).union(set(list2))  # or c = set(list1) | set(list2)
      d = set(list1).intersection(set(list2))  # or d = set(list1) & set(list2)
      return list(c - d)
  
  # Write list of dates only found in full date recordset. Then fill
  # the dataframe with nan values. These values will be used to
  # complete the entire data set.
  diff = (diff(indexForm, idxForm))
  df = pd.DataFrame({'NewDate' : diff})
  df['PRCP'] = np.nan
  df['SNOW'] = np.nan
  df['TMAX'] = np.nan
  df['TMIN'] = np.nan

  # Functions wont read dates before 1900,
  # used for loop to parse date manually.
  # Required since pandas wouldn't convert
  # all date records to correct format. This appends
  # a string of only the year-month-day. Drops
  # the hour-minute-second extension.
  Fix = []
  for aItem in idxForm:
    date = aItem[0:10]
    Fix.append(date)

  # Prep the fixed dates for merge. This combines
  # the re-formatted dates with the initial format
  # for the dataframe to be merged with.
  df2 = pd.DataFrame({'NewDate' : idxForm})
  df3 = pd.DataFrame({'FixedDate' : Fix})
  df4 = df2.join(df3, how='outer')

  ###############################################################################
  # This list is equivalent to the dates already in the set.
  # due to format issue, the dates had to be processed seprately.
  # This inserts a copy of the dates present, but in a different format.
  # (Formatted as indexForm)

  # Make list of index
  m = 0
  IFix = []
  for aItem in indexForm:
    IFix.append(m)
    m = m+1

  # Failed 12/8/19
  # Data['NewDate'] = IFix

  Data.loc[IFix,'NewDate'] = indexForm
 ##################################################################################
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
  DataFull = DataFull.drop(['PRCP', 'SNOW', 'TMAX', 'TMIN'], axis=1)
  DataFull['MM/DD/YYYY'] = DataFull['MM/DD/YYYY'].astype(str)
  DataFull = DataFull.rename(columns={'PRCP_y': 'PRCP', 'SNOW_y': 'SNOW', 'TMAX_y': 'TMAX', 'TMIN_y': 'TMIN'})
  
  # Merge the dates in correct format to main dataframe
  # DataFull = pd.merge(DataFull, df4, on='NewDate')
  DataFull = DataFull.merge(df4, on = 'NewDate', how='outer')
  # DataFull = DataFull.merge(df4, how='outer', left_on = 'NewDate', right_on = 'NewDate')

  DataFull = DataFull.drop(columns=['NewDate', 'MM/DD/YYYY'])
  DataFull = DataFull[['FixedDate', 'PRCP', 'SNOW', 'TMAX', 'TMIN']]
  # Convert to meet prior format standard
  Data = DataFull
  # Convert data from 10ths to full value
  Data['TMIN'] = Data['TMIN'].apply(lambda x: x/10)
  Data['TMAX'] = Data['TMAX'].apply(lambda x: x/10)
  Data['PRCP'] = Data['PRCP'].apply(lambda x: x/10)
  Data = Data.values.tolist()
  # Loop analysis
  # Specified to pass stations with errors
  if Path != 2:
    try:
      from SplitData import *
      Split_Data(Data, StationName, f, FirstYear, RawData, 
        BaseData, MonthX, Dayx, StationExports, OmitYearsT, FinalYear,
        WinterStats, WSY, MissingSnowData, YearLabel)
    except:
      pass

    try:
      from Snowfall_Analysis import *
      SnowFallAnalysis(StationName, RawData, SE, f, 
        StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
        MissingSnowData, BaseData, SingleYearSnowfall, EE, StandardSnow)
    except:
      pass

    try:
      from Temperature_Analysis import *
      Temperature(RawData, StationName, f, BaseData, StationExports, OmitYearsT, YearLabel)
    except:
      pass

    try:
      from Seasonality import *
      Seasonality(StationName, RawData, SE, f, 
        StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
        MissingSnowData, BaseData, EE, StandardSnow)
    except:
      pass

    try:
      from Rainfall import *
      Rainfall(StationName, RawData, SE, f, 
        StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
        MissingSnowData, BaseData)
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
    print ('\n')
    from SplitData import *
    Split_Data(Data, StationName, f, FirstYear, RawData, 
      BaseData, MonthX, Dayx, StationExports, OmitYearsT, FinalYear,
      WinterStats, WSY, MissingSnowData, YearLabel)

    from Snowfall_Analysis import *
    SnowFallAnalysis(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData, SingleYearSnowfall, EE, StandardSnow)

    from Temperature_Analysis import *
    Temperature(RawData, StationName, f, BaseData, 
      StationExports, OmitYearsT, YearLabel)

    from Seasonality import *
    Seasonality(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData, EE, StandardSnow)

    from Rainfall import *
    Rainfall(StationName, RawData, SE, f, 
      StationExports, Dayx, MonthX, YearLabel, WinterStats, WSY,
      MissingSnowData, BaseData)
      
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



    

