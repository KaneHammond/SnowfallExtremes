import csv
import os

MainOutput1 = open("TotalOutSO.cvs", "w")
MainOutput1.close()
inFile = open('FormanEdited.csv', 'r') #this just opens the file
theCsvData = csv.reader(inFile) #this creates a special object that the csv library knows how to access
allData=[]

for aRow in theCsvData:   #This takes the information read from the cvs and creates an index from it
  allData.append(aRow[:])

x = []  
SepData = [] 
PrevStation = (allData[0][0]) 
# print (PrevStation)

for aRow in allData:
  if aRow[0]==PrevStation: 
    x.append(aRow)
    PrevStation = aRow[0] 
  if aRow[0]!=PrevStation or aRow==allData[-1]: 
    SepData.append(x)                           
    x = []
    PrevStation = aRow[0]
    # print (PrevStation)
inFile.close()


import Analysis

xxx=0
SepData=allData
for aRow in SepData:
    Analysis
    xxx=xxx+1
    

# TempSet = []
# Index = 0
# Limit = len(allData)-1
# for aRow in allData:
#   Index = Index+1
#   if aRow[0]==PrevStation:
#     TempSet.append(aRow)
#     PrevStation = aRow[0]
#   if aRow[0]!=PrevStation:
#     PrevStation = aRow[0]
#     Run(TempSet)
#     TempSet = []
#   if Index==Limit:
#     Run(TempSet)
#     del TempSet
#     break
# inFile.close()

