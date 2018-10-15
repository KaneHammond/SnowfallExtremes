import pandas as pd
import sys
sys.path.append("DataModules")
# import ImportFTP
# ImportFTP
# from ImportFTP import*
# print df

FilterOptions = ['Country', 'Station/City', 'State/Province', 'Coordinates']
df = pd.DataFrame(FilterOptions,index=[1, 2, 3, 4], columns = ["SELECTION PARAMETERS"])

print(' \n**********CHOOSE DATA SELECTION METHOD**********\n ')
selection = 'INDEX'						
Data = 'SELECTION PARAMETERS'
# print('{: <6}  {: <31}'.format(selection,Data))
# print('-'*5 + '   ' + '-'*28)

for i in list(df.index):
	print('{: <1}: {: <31}'.format(i, df.loc[i,'SELECTION PARAMETERS']))
	print('-' + '  ' + '-'*15)

try:
    query = input('Enter Index selection (ex. 001, 3): ')
    query = int(query)
    if query>len(FilterOptions) or query<=0:
    	sys.exit()
except:
    print('Please enter valid selection (ex. 001, 3)')
    sys.exit()

if query==1:
	import Country
	Country

if query==2:
	import Station_City
	Station_City

if query==3:
	import State_Province
	State_Province

if query==4:
	print "Module missing or incomplete"
	sys.exit()	