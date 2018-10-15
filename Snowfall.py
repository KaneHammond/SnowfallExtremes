
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
# query = 3

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
  allStations = pd.DataFrame.read_csv("INPUT_DATA/Output/Country/StationInformation.csv",
    header=0)
  # Define the path for station daily records to be imported from (csv)
  Import_Path = 'INPUT_DATA/Output/Country/'

if query==2:
  sys.path.append("INPUT_DATA/Output/Station")
  allStations = pd.DataFrame.read_csv("INPUT_DATA/Output/Station/StationInformation.csv",
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

# Write the main output file to append to
# MainOutput1 = open("TotalOutSO.csv", "w")
# MainOutput1.close()

# Define lists of variables to be indexed and used for 
# the looping analysis
Stations = allStations['STATION_ID'].tolist()
States = allStations['STATE'].tolist()
StationNames = allStations['STATION_NAME'].tolist()
Country = allStations['COUNTRY_CODE'].tolist()
Elevation = allStations['ELEVATION'].tolist()
Lat = allStations['LATITUDE'].tolist()
Long = allStations['LONGITUDE'].tolist()


# Prompt options for analysis
print ('*'*25)
query = input('Select CDF Limit For Snowfall Extremes (i.e. 0.95):')
SE = int(query)
print ('*'*25)
query = raw_input('Define File Extention For Saved Figures (i.e. pdf):')
f = str(query)
print ('*'*25)
query = input('Define Starting Year for Analysis (YYYY):')
FirstYear = int(query)
print ('*'*25)

# # Autorun
# SE = 0.95
# f = 'pdf'
# FirstYear = 1950

# Not Written in as an option yet. This selects day and month to parse
# the data by. 
MonthX = 7
Dayx = 1

CheckRecords = []
FinalData = []
i = 0
ProgBarLimit = len(Stations)
print ('Initiating Analysis...')
for i in tqdm.tqdm(range(ProgBarLimit)):
  SnowData = []
  RawData = []
  BaseData = []
  StationExports = []
  StationExports.append(Stations[i])
  StationExports.append(States[i])
  StationExports.append(Country[i])
  StationExports.append(Elevation[i])
  StationExports.append(Lat[i])
  StationExports.append(Long[i])
  # Define specific common name for station in analysis
  StationName = StationNames[i]
  # Select stations from state folders using StationInformation.csv
  State = States[i]
  # Read specific station (Stations[i]=Station) at given state path
  Data = pd.read_csv((Import_Path+State+'/'+Stations[i]+'.csv'), header=0)
  # Format to meet current program design ([Date, PRCP, SNOW, TMAX, TMIN, TOBS])
  Data = Data.drop(columns=['ID', 'YEAR', 'MONTH', 'DAY'])
  Data = Data[['MM/DD/YYYY', 'PRCP', 'SNOW', 'TMAX', 'TMIN', 'TOBS']]
  Data['TOBS'] = Data['TOBS'].apply(lambda x: x/10)
  Data['TMIN'] = Data['TMIN'].apply(lambda x: x/10)
  Data['TMAX'] = Data['TMAX'].apply(lambda x: x/10)
  Data = Data.values.tolist()
  # Loop analysis
  i = i+1
  try:
    from SplitData import *
    Split_Data(Data, StationName, f, FirstYear, SnowData, RawData, BaseData, MonthX, Dayx, StationExports)
  except:
    pass
  try:
    from Snowfall_Analysis import *
    SnowFallAnalysis(StationName, SnowData, RawData, SE, f, StationExports, Dayx, MonthX)
  except:
    pass
  try:
    from Temperature_Analysis import *
    Temperature(RawData, StationName, f, BaseData, StationExports)
    # FinalData.append(StationExports)
  except:
    pass
  if len(StationExports)==133:
    FinalData.append(StationExports)
  if len(StationExports)!=133:
    CheckRecords.append(Stations[i])


Header = ['Station', 'State', 'Country', 'Elevation', 
  'Lat', 'Long', 'MonthCov', 'DailyCov', 'Min CDF', 'Day Start Slp',
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

print ('Writting Output File...')
with open("Output/TotalOutSO.csv", "w") as fp:
  a = csv.writer(fp, delimiter=',', lineterminator='\n')
  FinalData.insert(0, Header)
  data = FinalData
  a.writerows(data)

if len(CheckRecords)>0:
  print ('Writting Rejected Stations File...')
  with open("Output/ERROR_STATIONS.csv", "w") as fp:
    a = csv.writer(fp, delimiter=',', lineterminator='\n')
    FinalData.insert(0, Stations)
    data = CheckRecords
    a.writerows(data)



    

