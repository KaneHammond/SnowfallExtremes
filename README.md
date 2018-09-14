# SnowfallExtremes
Python 2.7
###### Objectives:
  1. Identify daily snowfall extremes
  2. Analyze snow season length
  3. Analyze snowfall variation
  4. Analyze temperature dynamics (Annual, Seasonal, Monthly)
  5. Compare temperatures with snowfall extremes/frequency
  6. Check for correlations over time.
  
###### Instructions:
This program requires python 2.7.

*Download => https://www.python.org/download/releases/2.7/

*Adding Paths => https://helpdeskgeek.com/windows-10/add-windows-path-environment-variable/

#Data:

To run the analysis, data is required in the form of a .csv. Test data can be obtained through this repository, or via https://www.ncdc.noaa.gov/cdo-web/search?datasetid=GHCND. The test data within this repository is highly parsed and modified to emulate corrupt and incomplete data. *At the moment* the looping function in the Master.py file is not working, only single stations can be run at a time. Therefore, only one station can be downloaded at a time (1 per .csv). The data required for this analysis is listed below:

#### DOWNLOAD DETAILS PRIOR TO DATA REQUEST TO NCDC ####

Station Detail & Data Flag Options:
  1) Station Name
  2) Geographic Location
  3) Units *This program will work with either standard or metric units*
  
Select data types for custom output:
  1) Precipitation:
  
    * Precipitation (PRCP)
    
    * Snowfall (SNOW)
    
  2) Air Temperature
  
    * Maximum temperature (TMAX)
    
    * Minimum temperature (TMIN)
    
    * Temperature at the time of observation (TOBS)

#Using the Program:

Data is available within this repository for the Foreman weather station in North Dakota. The dataset has been edited to incorporate errors. This was done for checking the elasticity of the program. To run the analysis, all python files, accompanied by the .csv data, must be located in the same folder. Once they are all located in the same vicinity, the program can be initiated from the command prompt (python 2.7 must be installed and have appropriate path access). In order to do this, change the directory path in the command prompt to the location of the python files and data. Once the file path has been adjusted, the Master.py module can be initiated by: 

Within Command Prompt:

C:\\(wherever the files have been placed)> python Master.py



