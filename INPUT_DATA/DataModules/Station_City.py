
import sys
import pandas as pd
from ftplib import FTP
import os
import io
import csv

output_dir = os.path.relpath('Output')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)

output_dir = os.path.relpath('Output/Station')
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)


ftp_path_dly = '/pub/data/ghcn/daily/'
ftp_path_dly_all = '/pub/data/ghcn/daily/all/'
ftp_filename = 'ghcnd-stations.txt'

def connect_to_ftp():
    ftp_path_root = 'ftp.ncdc.noaa.gov'

    # Access NOAA FTP server
    ftp = FTP(ftp_path_root)
    message = ftp.login()  # No credentials needed
    print(message)
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
    
    # Write .dly file to stream using StringIO using FTP command 'RETR'
    s = io.BytesIO()
    ftp.retrlines('RETR ' + ftp_path_dly_all + ftp_filename, s.write)
    s.seek(0)
    
    # Write .dly file to dir to preserve original # FIXME make optional?
    with open(os.path.join(output_dir, ftp_filename), 'wb+') as f:
        ftp.retrbinary('RETR ' + ftp_path_dly_all + ftp_filename, f.write)
    
    # Move to first char in file
    s.seek(0)
    
    # File params
    num_chars_line = 269
    num_chars_metadata = 21

    element_list = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN']
    
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
        Print status
        '''
        if year != prev_year:
            print('Year {} | Line {}'.format(year, i))
            prev_year = year
        
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
    df_all = df_all.loc[df_all['ID'].notnull(), :]
    # print df_all # Missing Data at this point
    
    '''
    Output to CSV, convert everything to strings first
    '''
    # NOTE: To open the CSV in Excel, go through the CSV import wizard, otherwise it will come out broken
    df_out = df_all.astype(str)
    df_out.to_csv(os.path.join(output_dir, station_id + '.csv'))
    print('\nOutput CSV saved to: {}'.format(os.path.join(output_dir, station_id + '.csv')))

def get_station_id(ftp):
    '''
    Get stations file
    '''
    ftp_full_path = os.path.join(ftp_path_dly, ftp_filename)
    local_full_path = os.path.join(output_dir, ftp_filename)
    if not os.path.isfile(local_full_path):
        with open(local_full_path, 'wb+') as f:
            ftp.retrbinary('RETR ' + ftp_full_path, f.write)

    '''
    Get user search term
    '''
    print()
    query = raw_input('Enter station name, full or partial. (ex. Washington, san fran, USC): ')
    query = query.upper()
    # FIXME try/catch and clean input
    print()

    '''
    Read stations text file using fixed-width-file reader built into pandas
    '''
    # http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_fwf.html
    dtype = {'STATION_ID': str,
             'LATITUDE': str,
             'LONGITUDE': str,
             'ELEVATION': str,
             'STATE': str,
             'STATION_NAME': str,
             'GSN_FLAG': str,
             'HCN_CRN_FLAG': str,
             'WMO_ID': str}
    names = ['STATION_ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE', 'STATION_NAME', 'GSN_FLAG', 'HCN_CRN_FLAG', 'WMO_ID']
    widths = [11,  # Station ID
              9,   # Latitude (decimal degrees)
              10,  # Longitude (decimal degrees)
              7,   # Elevation (meters)
              3,   # State (USA stations only)
              31,  # Station Name
              4,   # GSN Flag
              4,   # HCN/CRN Flag
              6]   # WMO ID
    df = pd.read_fwf(local_full_path, widths=widths, names=names, dtype=dtype, header=None)
    # print list(df.columns.values)
    # print df

    '''
    Replace missing values (nan, -999.9)
    '''
    df['STATE'] = df['STATE'].replace('nan', '--')
    df['GSN_FLAG'] = df['GSN_FLAG'].replace('nan', '---')
    df['HCN_CRN_FLAG'] = df['GSN_FLAG'].replace('nan', '---')
    df = df.replace(-999.9, float('nan'))
    
    try:
        '''
        Get query results, but only the columns we care about
        '''
        print('Searching records...')
        matches = df['STATION_NAME'].str.contains(query)
        df = df.loc[matches, ['STATION_ID', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'STATE', 'STATION_NAME']]
        df.reset_index(drop=True, inplace=True)

        '''
        Get file sizes of each station's records to augment results
        '''
        print('Getting file sizes...')
        ftp.voidcmd('TYPE I')  # Needed to avoid FTP error with ftp.size()
        for i in list(df.index):
            print('.')
            ftp_dly_file = ftp_path_dly + 'all/' + df.loc[i, 'STATION_ID'] + '.dly'
            df.loc[i, 'SIZE'] = round(ftp.size(ftp_dly_file)/1000)  # Kilobytes
        print()
        print()

        '''
        Sort by size then by rounded lat/long values to group geographic areas and show stations with most data
        '''
        df_sort = df.round(0)
        df_sort.sort_values(['LATITUDE', 'LONGITUDE', 'SIZE'], ascending=False, inplace=True)
        df = df.loc[df_sort.index]
        df.reset_index(drop=True, inplace=True)
        
    except:
        print('Station not found')
        sys.exit()
    
    '''
    Print headers and values to facilitate reading
    '''
    selection = 'Index'
    station_id = 'Station_ID '
    lat = 'Latitude'
    lon = 'Longitude'
    state = 'State'
    name = 'Station_Name                '
    size = ' File_Size'
    # Format output to be pretty, hopefully there is a prettier way to do this.
    print('{: <6}{: <31}{: <6}({: >8},{: >10}){: >13}'.format(selection, name, state, lat, lon, size))
    print('-'*5 + ' ' + '-'*30 + ' ' + '-'*5 + ' ' + '-'*21 + ' ' + '-'*12)
    for i in list(df.index):
        print('{: 4}: {: <31}{: <6}({: >8},{: >10}){: >10} Kb'.format(i,
                                                                          df.loc[i,'STATION_NAME'],
                                                                          df.loc[i,'STATE'],
                                                                          df.loc[i,'LATITUDE'],
                                                                          df.loc[i,'LONGITUDE'],
                                                                          df.loc[i,'SIZE']))

    '''
    Get user selection
    '''
    try:
        query = input('Enter selection (ex. 001, 42): ')
        query = int(query)
        Name.append(df.loc[query, 'STATION_NAME'])
    except:
        print('Please enter valid selection (ex. 001, 42)')
        sys.exit()

    station_id = df.loc[query, 'STATION_ID']
    return station_id
# Define list to append station name to. Needed to ensure
# its returned from the def.
Name = []
ftp = connect_to_ftp()
station_id = get_station_id(ftp)
print(station_id)
dly_to_csv(ftp, station_id)
ftp.quit()
# Define variables for the station info csv. This is for the
# Snowfall program to read, allowing it to identify the location
# of the data file.
Header = 'STATION_ID'
Station = [station_id]
Station.insert(0, Header)
# Change the variable Name from list to an individual string item.
Name = Name[0]
Station.insert(-1, Name)

with open("Output/Station/StationInformation.csv", "w") as fp:
    a = csv.writer(fp, delimiter=',', lineterminator='\n')
    data = Station
    print data
    # for aRow in data:
    #     print aRow
    a.writerow(data)
