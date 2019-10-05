#SNOWFALL EXTREMES!

Introduction:
This program was developed to define what an extreme snowfall event is
from a weather stations daily historical snowfall records. A Cumulative 
Distribution Function (CDF) is used to define what events at that specific
location are statistical anomalies. This method allows for a better understanding
of how snowfall at specific locations have either changed or remained the same over the
years of the analysis. I did this to highlight changes on local
levels. An extreme snowfall event may be very different from a station 50 miles 
away. This could simply be a product of where the jet stream passes, the 
geomorphology of the landscape, etc. Many factors play into the development of
precipitation at the local level. Therefore, I sought to define these events 
locally. No mapping outputs were written in this program, outputs include figures and
a total output file in the form of a .csv. This contains all the statistical 
information from the analysis. Temperature data is also included in the analysis.

Installation:
To start the installation process, it is best to start with the data download module.
This can be found separately on my GitHub under the GHCN extension, but is also
included in this package. Change the directory to the INPUT_DATA folder. This is where
the data download process takes place, providing the input data for the analysis. To 
install the data download module, simply run the Master.py file in the INPUT_DATA 
folder. The  dependencies will be sought and downloaded. To ensure all dependencies 
are met for the overall analysis, run the Snowfall.py file from the SnowfallExtremes
folder. If all imports for both are successful, you are ready to use the program.

Running an analysis:
To use this program, you must first provide data for the analysis. Run the Master.py 
file from the INPUT_DATA folder to select your download method. You can choose
to download a single station, country, state/province, list of countries, or list of 
states/provinces. You will also be given the option to filter by latitude for larger 
downloads. For example, if you wish to only run the Northern portion of the United
States, you can specify by inputing a latitude. If downloading a single station,
all available data will be pulled. When downloading larger data sets, you are 
prompted what data types are available for the date range you provided for that 
given collection. For a basic analysis you need snowfall, max temperature, and 
minimum temperature. I found temperature at observation to be missing in many places.
After these have been selected, the program will update to tell you how many stations 
contain the specified data. From there you download the data.

After the data has been downloaded you run the Snowfall.py file to initiate the 
snowfall extreme and temperature analysis. Once you start the Snowfall.py 
analysis it will ask several questions on how you would like to conduct the data
processing. Including start and end dates, cdf limit, file format, year start and end,
etc. The year start and end was included as a standard calendar year doesn't really
incorporate the transition between Fall, Winter, and Spring. For best results I 
suggest using July as the start of each year. This will be close to summer solstice.
After you define the basic parameters, the analysis will run. If you are processing 
a country or more, it may take a day to run. Errors will not cause the program to exit
and all failed stations will be listed in the error output for further observation. 
The end results will be figures for every station in the file format you define, as 
well as a total output csv including coordinates for each station. This will allow you
to import it into mapping software for a spatial analysis, or import into another 
program.
