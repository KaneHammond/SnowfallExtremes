
import os
import pandas as pd
import sys
from ftplib import FTP
import csv
import io
import numpy as np
import copy
sys.path.append("Output")
sys.path.append("TXT_FILES")

# Write output directory
output_dir = os.path.relpath('Output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
output_dir = os.path.relpath('Output/Country')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
output_dir = os.path.relpath('TXT_FILES')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

# Definition for printing full dataframe
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
#************************************ DATA COVERAGE CHECK FTP
ftp_path_dly = '/pub/data/ghcn/daily/'
ftp_path_dly_all = '/pub/data/ghcn/daily/all/'
local_full_path = 'TXT_FILES/ghcnd-inventory.txt'

# This ftp definition is the first one to run, this is defined here and 
# later. The reason is to run it whith the login message once. The second
# connection made to the ftp server does not prompt the message a second time.

def connect_to_ftp():
    """
    Get FTP server and file details
    """
    ftp_path_root = 'ftp.ncdc.noaa.gov'
    # Access NOAA FTP server
    ftp = FTP(ftp_path_root)
    message = ftp.login()  # No credentials needed
    print('%s \n ' % (message))
    return ftp
# Run to show login message. 
connect_to_ftp()

def Inventory(ftp):    
    ftp_filename = 'ghcnd-inventory.txt'

    ftp_full_path = os.path.join(ftp_path_dly, ftp_filename)
    local_full_path = os.path.join(output_dir, ftp_filename)
    if not os.path.isfile(local_full_path):
        with open(local_full_path, 'wb+') as f:
            ftp.retrbinary('RETR ' + ftp_full_path, f.write)

    # Variable   Columns   Type
    # ------------------------------
    # ID            1-11   Character
    # LATITUDE     13-20   Real
    # LONGITUDE    22-30   Real
    # ELEMENT      32-35   Character
    # FIRSTYEAR    37-40   Integer
    # LASTYEAR     42-45   Integer
    # values provided above. These values are given by the readme file 
    # on the FTP server.
    dtype = {'STATION_ID': str,
    		'LATITUDE': str,
    		'LONGITUDE': str,
    		'ELEMENT': str,
    		'FIRSTYEAR': str,
    		'LASTYEAR': str,}
    names = ['STATION_ID', 'LATITUDE', 'LONGITUDE', 'ELEMENT', 'FIRSTYEAR', 'LASTYEAR']
    widths = [11,  # Station ID
    			9,   # Latitude (decimal degrees)
    			10,  # Longitude (decimal degrees)
    			5,   # Element
    			5,   # FY
    			5]   # LY
    df = pd.read_fwf(local_full_path, widths=widths, names=names, dtype=dtype, header=None)
    # Write country codes and insert into the station df
    CC = []
    for aItem in df['STATION_ID']:
        CC.append(aItem[0:2])
    df.insert(0, 'COUNTRY_CODE', value=CC)
    # Define list of stations from Country selection
    # to be entered into a list for data download
    df = df[df.COUNTRY_CODE.isin(Countries)]
    df = df.values.tolist()
    for aItem in df:
        Filter.append(aItem)
    return Filter


# ftp = connect_to_ftp()
# Inventory(ftp)

# ******************************* NATION LIST/CODES FTP

# Define file paths within folders and on the ftp server.

ftp_path_dly = '/pub/data/ghcn/daily/'
ftp_filename = 'ghcnd-countries.txt'
local_full_path = 'TXT_FILES/ghcnd-countries.txt'

# Connects to the server for ftp download. This def prints the 
# ftp connection message/warning.

def connect_to_ftp():
    """
    Get FTP server and file details
    """
    ftp_path_root = 'ftp.ncdc.noaa.gov'
    # Access NOAA FTP server
    ftp = FTP(ftp_path_root)
    message = ftp.login()  # No credentials needed
    return ftp

# This section opens the text file containing country data. Then it is used
# to prompt which countries are of interest for the download.

def countries(ftp):    
    ftp_full_path = os.path.join(ftp_path_dly, ftp_filename)
    local_full_path = os.path.join(output_dir, ftp_filename)
    if not os.path.isfile(local_full_path):
        with open(local_full_path, 'wb+') as f:
            ftp.retrbinary('RETR ' + ftp_full_path, f.write)

# Variable   Columns   Type
# ------------------------------
# CODE          1-2    Character
# NAME         4-50    Character
# ------------------------------
    # This section will parse the text file into a pandas df based upon 
    # values provided above. These values are given by the readme file 
    # on the FTP server.
    dtype = {'CODE': str,
            'COUNTRY': str}
    names = ['CODE', 'COUNTRY']
    widths = [2,  # CODE
                48]   # COUNTRY
    df = pd.read_fwf(local_full_path, widths=widths, names=names, dtype=dtype, header=None)
    print ('*'*25)
    # Query for country selection (multiple values), must be separated 
    # by ', ' to meet requirements.
    query = raw_input('View List of Available Countries(Y/N):')
    query = query.upper()
    if query=='Y':
        print_full(df)
    print ('*'*25)
    print('Enter Country Code(s):')
    a = [str(x) for x in raw_input().upper().split(', ')]
    print('')
    print('Searching records...\n')
    i=0
    # Loop though the query to identify countries if variables are missing.
    # Does not work if too many variables are provided (USA vs US). Only 2
    # letter or single letter entries are recognized. Three letter
    # combinations are ignored and passed.
    for aItem in a:
        print ('%s...\n' % (aItem))
        matches = df['CODE'].str.contains(aItem)
        dfM = df.loc[matches, ['CODE', 'COUNTRY']]
        matches = dfM
        try:
            if len(matches)==1:
                Countries.append(matches.iloc[0]['CODE'])
            if len(matches)>1:
                dfM.reset_index(drop=True, inplace=True)
                dfM.index = dfM.index+1
                CODE = str('CODE')
                COUNTRY = str('COUNTRY')
                print('{: <6}{: <31}'.format(CODE,COUNTRY))
                print('-'*5 + ' ' + '-'*15 + '-'*10)
                for i in list(dfM.index):
                    print('{: 4}: {: <14}{: <9}'.format(i,
                                                dfM.loc[i,'CODE'],
                                                dfM.loc[i,'COUNTRY'])) 
                print('Country not found: %s' % (aItem))
                print ('Select Correct Country')
                query = input()
                query = int(query)
                Countries.append(dfM.loc[query, 'CODE'])
        except:
            print ('Country Code %s Not Found' % (aItem))
            sys.exit()

# Run main functions, sets up data for download and individual parsing.
Filter = []
Countries = []
ftp = connect_to_ftp()
countries(ftp)
Inventory(ftp)

# Filter through start dates, selecting start dates that are at least
# the given value from the query.
print ('*'*25)
query = input('Identify Start Date (YYYY):')
query = int(query)
Filter2 = []
for aRow in Filter:
    aRow[-2] = int(aRow[-2])
    if aRow[-2]<=query:
        # print aRow[-2]
        Filter2.append(aRow)

# Filter through end dates, selecting end dates that are at least 
# the given value from the query.
Filter = []
print ('*'*25)
query = input('Identify End Date (YYYY):')
query = int(query)
for aRow in Filter2:
    aRow[-1] = int(aRow[-1])
    if aRow[-1]>=query:
        Filter.append(aRow)

# Filter by latitude. Longitude is not currently an option for this software.
# This section is an optional addition and can be passed in the prompt.
Filter2 = []
print ('*'*25)
query = raw_input('Filter by Latitude(Y/N):')
query = query.upper()
if query == 'Y':
    print ('*'*25)
    print ('1. Equal to or Greater Than\n2. Equal to or Less Than')
    query = input('Drop Records Which Are(1/2):')
    query = int(query)
    if query == 1:
        print ('*'*25)
        print ('Define Latitude:')
        lat = input()
        lat = float(lat)
        for aRow in Filter:
            aRow[2] = float(aRow[2])
            if aRow[2]>=lat:
                Filter2.append(aRow)
    if query == 2:
        print ('*'*25)
        print ('Define Latitude:')
        lat = input()
        lat = float(lat)
        for aRow in Filter:
            aRow[2] = float(aRow[2])
            if aRow[2]<=lat:
                Filter2.append(aRow)
    Filter = []
    if query>2 or query<0:
        print ('Please Enter Integer Within Range')
        sys.exit()

# Filter check to ensure loops have gone through and data has parsed correctly
if len(Filter2)==0 and len(Filter)==0:
    print ('Data Coverage For Defined Parameters Is Not Available')
    sys.exit()
if len(Filter2)>0 and len(Filter)>0:
    print ('Error parsing data')
    sys.exit()

# Identify which set has data present. Due to errors deleting records,
# two lists were used to filter records. Since some sections are optional,
# either list may be the correct list to write a dataframe from.
if len(Filter)>0:
    df = pd.DataFrame(Filter, columns=['COUNTRY_CODE', 'STATION_ID', 'LATITUDE', 'LONGITUDE', 'ELEMENT', 'FIRSTYEAR', 'LASTYEAR'])

if len(Filter2)>0:
    df = pd.DataFrame(Filter2, columns=['COUNTRY_CODE', 'STATION_ID', 'LATITUDE', 'LONGITUDE', 'ELEMENT', 'FIRSTYEAR', 'LASTYEAR'])

# This section prepares for selection of elements (coverage types) over
# the list of returned stations. The elements present do not mean each
# station has the full coverage. It is simply a list of what is present.

Elements = df.ELEMENT.unique()
Elements = pd.DataFrame(Elements, columns=['AVAILABLE ELEMENTS'])
Stations = df.drop_duplicates('STATION_ID')
Elements.reset_index(drop=True, inplace=True)
Elements.index = Elements.index+1
print ('*'*25)
print_full(Elements) 
print ('')
print ('Total Stations in Selection: %i' % (len(Stations.index)))
print ('Specification of Elements May Reduce Total Stations')
print ('*'*25)
print('Select Elements(ex. 001, 1):')
a = [str(x) for x in raw_input().upper().split(', ')]
element_list = []
for aItem in a:
    aItem = int(aItem)
    element_list.append(Elements.loc[aItem, 'AVAILABLE ELEMENTS'])
# Write station list 
dfList = Stations['STATION_ID'].tolist()

# Write station coordinates file and prompt for download

# Import outside of loop modifies list parsing in python
# must remian in definition for this section only
StationFilter2 = []
def SecondFilter():
    try:
        import collections
    except:
        import pip
        pip.main(['install','collections'])
    import collections
    from collections import Counter

    dfF = df[df.ELEMENT.isin(element_list)]
    # print df

    StationID = dfF['STATION_ID'].tolist()
    Count = collections.Counter(StationID)
    Keys = copy.deepcopy(Count.keys())
    Counts = copy.deepcopy(Count.values())
    # print Keys
    # print Counts
    i = 0
    for aItem in Counts:
        if aItem>=len(element_list):
            StationFilter2.append(Keys[i])
        i = i+1
    return StationFilter2

SecondFilter()

dfList = StationFilter2
# Write Stations Location and additional information csv
print ('*'*25)
query = raw_input('%i Stations Have Coverage For Selected Filter.\nDownload Data? (Y/N):' % (len(dfList)))
query = query.upper()
print ('*'*25)
for aItem in query:
    if query=='Y':
        continue
    if query!='Y':
        print ('Download Canceled')
        sys.exit()

output_dir = os.path.relpath('Output/Country/')

dfS = df[df.STATION_ID.isin(StationFilter2)]
dfS = dfS.drop_duplicates('STATION_ID')
dfS = dfS.drop(columns=['ELEMENT', 'FIRSTYEAR', 'LASTYEAR'])
df_out = dfS.astype(str)
df_out.to_csv(os.path.join(output_dir, 'StationInformation.csv'))


# Download daily file to csv 

ftp_path_dly = '/pub/data/ghcn/daily/'
ftp_path_dly_all = '/pub/data/ghcn/daily/all/'
ftp_filename = 'ghcnd-stations.txt'
local_full_path = 'TXT_FILES/ghcnd-stations.txt'

for aItem in Countries:
    CODE = aItem
    output_dir = os.path.relpath('Output/Country/%s' % (CODE))
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

output_dir = os.path.relpath('Output/Country/')


def connect_to_ftp():
    ftp_path_root = 'ftp.ncdc.noaa.gov'

    # Access NOAA FTP server
    ftp = FTP(ftp_path_root)
    message = ftp.login()  # No credentials needed
    # print(message)
    return ftp

def get_flags(s):
    """
    Get flags, replacing empty flags with '_' for clarity (' S ' becomes '_S_')
    """
    m_flag = s.read(1)
    m_flag = m_flag if m_flag.strip() else '_'
    q_flag = s.read(1)
    q_flag = q_flag if q_flag.strip() else '_'
    s_flag = s.read(1)
    s_flag = s_flag if s_flag.strip() else '_'
    return [m_flag + q_flag + s_flag]

def create_dataframe(element, dict_element):
    """
    Make dataframes out of the dicts, make the indices date strings (YYYY-MM-DD)
    """
    # element = element.upper()
    df_element = pd.DataFrame(dict_element)
    # print df_element

    # Separate dfs' pass this point containing data for full record.
    # Need to filter out unwanted data to ensure final output is complete.

    # Add dates (YYYY-MM-DD) as index on df. Pad days with zeros to two places
    df_element.index = df_element['YEAR'] + '-' + df_element['MONTH'] + '-' + df_element['DAY'].str.zfill(2)
    df_element.index.name = 'DATE'
    # Arrange columns so ID, YEAR, MONTH, DAY are at front. Leaving them in for plotting later - https://stackoverflow.com/a/31396042
    for col in ['DAY', 'MONTH', 'YEAR', 'ID']:
        df_element = move_col_to_front(col, df_element)
    # Convert numerical values to float
    df_element.loc[:,element] = df_element.loc[:,element].astype(float)
    return df_element
    
def move_col_to_front(element, df):
    element = element.upper()
    cols = df.columns.tolist()
    cols.insert(0, cols.pop(cols.index(element)))
    df = df.reindex(columns=cols)
    return df
 
def dly_to_csv(ftp, station_id):    
    ftp_filename = station_id + '.dly'
    Country_File = (station_id[0:2]+'/')

    # Write .dly file to stream using StringIO using FTP command 'RETR'
    s = io.BytesIO()
    ftp.retrlines('RETR ' + ftp_path_dly_all + ftp_filename, s.write)
    s.seek(0)
    
    # Write .dly file to dir to preserve original # FIXME make optional?
    # with open(os.path.join(output_dir, Country_File, ftp_filename), 'wb+') as f:
    #     ftp.retrbinary('RETR ' + ftp_path_dly_all + ftp_filename, f.write)
    
    # Move to first char in file
    s.seek(0)
    
    # File params
    num_chars_line = 269
    num_chars_metadata = 21

    '''
    Read through entire StringIO stream (the .dly file) and collect the data
    '''
    all_dicts = {}
    element_flag = {}
    prev_year = '0000'
    i = 0
    while True:
        i += 1
        
        '''
        Read metadata for each line (one month of data for a particular element per line)
        '''
        id_station = s.read(11)
        year = s.read(4)
        month = s.read(2)
        day = 0
        element = s.read(4)
        
        # If this is blank then we've reached EOF and should exit loop
        if not element:
            break
        
        '''
        Loop through each day in rest of row, break if current position is end of row
        '''
        while s.tell() % num_chars_line != 0:
            day += 1
            # Fill in contents of each dict depending on element type in current row
            if day == 1:
                try:
                    first_hit = element_flag[element]
                except:
                    element_flag[element] = 1
                    all_dicts[element] = {}
                    all_dicts[element]['ID'] = []
                    all_dicts[element]['YEAR'] = []
                    all_dicts[element]['MONTH'] = []
                    all_dicts[element]['DAY'] = []
                    all_dicts[element][element.upper()] = []
                    # all_dicts[element][element.upper() + '_FLAGS'] = []
                
            value = s.read(5)
            flags = get_flags(s)
            if value == '-9999':
                continue
            all_dicts[element]['ID'] += [station_id] 
            all_dicts[element]['YEAR'] += [year]
            all_dicts[element]['MONTH'] += [month]
            all_dicts[element]['DAY'] += [str(day)]
            all_dicts[element][element.upper()] += [value]
            # all_dicts[element][element.upper() + '_FLAGS'] += flags
            
    '''
    Create dataframes from dict
    '''

    all_dfs = {}
    for element in list(all_dicts.keys()):
        all_dfs[element] = create_dataframe(element, all_dicts[element])
    # print all_dicts.keys()
    BaseColumns = ['ID', 'YEAR', 'MONTH', 'DAY']
   
    '''
    Combine all element dataframes into one dataframe, indexed on date. 
    '''
    # pd.concat automagically aligns values to matching indices, therefore the data is date aligned!
    list_dfs = []
    for df in list(all_dfs.keys()):
        list_dfs += [all_dfs[df]]
    df_all = pd.concat(list_dfs, axis=1, sort='True')
    df_all.index.name = 'MM/DD/YYYY'
    
    '''
    Remove duplicated/broken columns and rows
    '''
    # https://stackoverflow.com/a/40435354
    df_all = df_all.loc[:,~df_all.columns.duplicated()]


    # Keep selected elements only
    Records = BaseColumns+element_list
    # df = list(df_all.columns.values)
    # E = [elem for elem in df if elem not in element_list ]
    # print E
    try:
        df_all = df_all[Records]
        df_out = df_all.astype(str)
        df_out.to_csv(os.path.join(output_dir, Country_File, station_id + '.csv'))
    except:
        # print('Record Missing Element(s)')
        pass

print ('Downloading Data')

ftp = connect_to_ftp()
for aItem in dfList:
    station_id = aItem
    dly_to_csv(ftp, station_id)

ftp.quit()
sys.exit()

