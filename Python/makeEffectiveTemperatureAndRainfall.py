"""

# MY 8.8.2025
# - tarvitaan: Effective temperature sum (vuorokauden keskilämpötila - 5 ja negatiiviset pois) ja annual precipitation sum
# Paitulista datat (netcdf): 10km_daily_mean_temperature ja 10km_monthly_precipitation (kumulatiivinen) (Ilmatieteenlaitos, CC BY 4.0)
# hydrologisen vuoden ajalta: 1.6.-31.5.
# kuntien keskipisteelle

RUN:
python makeEffectiveTemperatureAndRainfall.py

# tulosteessa:
# kunta: kunnan nimi
# kuntaID: kuntanumero
# kunta2: kuntaID_aloitusvuosi
# alkuvuosi: hydrologisen vuoden alkuvuosi (1.6.)
# cumulativeEffectiveTemperature: hydrologisen vuoden tehoisa lämpösumma 
# Cumulative rainfall: hydrologisen vuoden kumulatiivinen sademäärä (mm)

"""
# Syötteet luetaan lokaalisti:
inputpaths = "~/Documents/ilmastoData/10km_daily_mean_temperature/netcdf/*.nc"
inputpaths2 = "~/Documents/ilmastoData/10km_monthly_precipitation/netcdf/*.nc"

# Tulostetiedosto:
#outputpath = "~/Documents/ilmastoData/ilmastodatoja/aikasarjoja2/cumulativeEffectiveTemperature.csv"
#outputpath2 = "~/Documents/ilmastoData/ilmastodatoja/aikasarjoja2/cumulativeRainfall.csv"

outputpath3 = "~/Documents/ilmastoData/ilmastodatoja/Karimaalle/cumulativeRainfall-cumulativeEffectiveTemperature.csv"

# Tarvittavat kuntatiedostot:
kunnat2023_shapefile = "~/Documents/GISdata/mml/hallintorajat_milj_tk/2023/kunnat_2023_milj.shp" 

import xarray as xr
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc


# read in municipalities:
kunnat = gpd.read_file(kunnat2023_shapefile)
# calculate the centroid of a municipality:
kunnat['keskipiste'] = kunnat.centroid

print('\nCumulative effective Temperature Jun 1 - May 31 from daily mean temperatures')

datacube = xr.open_mfdataset(inputpaths, parallel=True)

results = list()

for i in range(len(kunnat)):
    #print(kunnat['NAMEFIN'][i])
    kuntaNAME = kunnat['NAMEFIN'][i]
    kuntaID = kunnat['NATCODE'][i]
    
    # käydään läpi kaikki vuodet:
    for alku in range(1961,2023):
        loppu = alku + 1
        #print(alku, loppu)
        alkuvuosi = alku
        # valitaan aikaikkuna 1.6.alkuvuosi - 31.5.loppuvuosi:
        datacube2 = datacube['Tday'].sel(Lon = kunnat['keskipiste'][i].x, Lat = kunnat['keskipiste'][i].y, method = 'nearest').sel(Time = slice(str(alku) + '-06-01', str(loppu) + '-05-31'))
        datacube22 = datacube2 - 5
        datacube3 = datacube22.where(datacube22 > 0).cumsum()
        cumulativeSum = int(datacube3.values[-1])
        results.append([kuntaNAME, kuntaID, alkuvuosi, cumulativeSum])
            
        
# kootaan tulokset:    
dfTemp = pd.DataFrame(results,columns = ['kunta', 'kuntaID', 'alkuvuosi', 'cumulativeEffectiveTemperature'])
dfTemp['kunta2'] = dfTemp['kuntaID'].astype(str) + '_' + dfTemp['alkuvuosi'].astype(str)


print('\nCumulative rainfall for Jun 1 - May 31 from monthly sums of precipitation')

datacube = xr.open_mfdataset(inputpaths2, parallel=True)


results = list()

for i in range(len(kunnat)):
    #print(kunnat['NAMEFIN'][i])
    kuntaNAME = kunnat['NAMEFIN'][i]
    kuntaID = kunnat['NATCODE'][i]
    for alku in range(1961,2023):
        loppu = alku + 1
        #print(alku, loppu)
        alkuvuosi = alku
        datacube2 = datacube['RRmon'].sel(Lon = kunnat['keskipiste'][i].x, Lat = kunnat['keskipiste'][i].y, method = 'nearest').sel(Time = slice(str(alku) + '-06-01', str(loppu) + '-05-31'))
        datacube3 = datacube2.cumsum()
        cumulativeSum = int(datacube3.values[-1])
        results.append([kuntaNAME, kuntaID, alkuvuosi, cumulativeSum])
            
        
    
dfRain = pd.DataFrame(results,columns = ['kunta', 'kuntaID', 'alkuvuosi', 'Cumulative rainfall'])
dfRain['kunta2'] = dfRain['kuntaID'].astype(str) + '_' + dfRain['alkuvuosi'].astype(str)

print('Merge the two datasets')
dfAll = dfTemp.merge(dfRain[['kunta2', 'Cumulative rainfall']], on = 'kunta2', how = 'right')

# modify columns names according to N-leach model:
dfAll.rename(columns = {'cumulativeEffectiveTemperature': 'Ef_Lamposumma', 'Cumulative rainfall': 'Sadesumma'}, inplace = True)
print(dfAll.head())
print(f'\nSave to file {outputpath3}')
dfAll.to_csv(outputpath3, index = False, sep = ';')
