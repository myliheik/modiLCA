# Municipality-level effective temperature sums and precipitation

## Overview

The script `makeEffectiveTemperatureAndRainfall.py` calculates effective temperature sums and cumulative precipitation for Finnish municipalities using gridded climate data. Indicators are calculated for annual periods extending from **1 June to 31 May** and exported for subsequent use in a nitrogen-leaching model.

## Data sources

Daily mean air temperature and monthly precipitation data were obtained from the Finnish Meteorological Institute through the Paituli spatial data service at a spatial resolution of 10 km. The datasets are distributed under the Creative Commons Attribution 4.0 licence.

Municipality boundaries were taken from the 2023 municipality boundary dataset. A geometric centroid was calculated for each municipality, and climate values were extracted from the nearest grid location to that centroid. These values therefore represent conditions at a single grid location rather than spatial averages over the municipality.

| Input | Description |
|---|---|
| `10km_daily_mean_temperature` | Daily mean air temperature; NetCDF variable `Tday` |
| `10km_monthly_precipitation` | Monthly precipitation totals; NetCDF variable `RRmon` |
| `kunnat_2023_milj.shp` | Municipality boundaries, names, and identifiers |

## Calculation methods

### Annual periods

The analysis covers starting years 1961–2022, corresponding to periods from June 1961–May 1962 through June 2022–May 2023. Each period is labelled by its starting year.

The term *hydrological year* is used here specifically for the June–May period.

### Effective temperature sum

The effective temperature sum is calculated by accumulating daily mean temperatures above a base temperature of 5 °C:

$$\mathrm{ETS}_{m,y} = \sum_{d \in H_y}\max\left(T_{m,d}-5^\circ\mathrm{C}\,0\right),$$

where $$T_{m,d}$$ is the daily mean temperature at the selected grid location for municipality $$m$$, and $$H_y$$ denotes the June–May period beginning in year $$y$$.

Days with daily mean temperatures at or below 5 °C contribute zero. The resulting indicator is expressed in degree-days (°C·days).

This calculation includes all qualifying days within the annual period; it does not identify or restrict the calculation to a separate growing season.

### Cumulative precipitation

Cumulative precipitation is calculated by summing monthly precipitation totals over the same June–May period. The resulting indicator is expressed in millimetres.
 
## Output

The configured output filename is `cumulativeRainfall-cumulativeEffectiveTemperature.csv`.

| Column | Description | Unit or format |
|---|---|---|
| `kunta` | Municipality name | Text |
| `kuntaID` | Municipality identifier | Municipality code |
| `alkuvuosi` | Starting year of the June–May period | Year |
| `Ef_Lamposumma` | Effective temperature sum above 5 °C | °C·days, truncated to an integer |
| `kunta2` | Combined municipality and starting-year identifier | `municipalityCode_startYear` |
| `Sadesumma` | Cumulative precipitation | mm, truncated to an integer |

The names `Ef_Lamposumma` and `Sadesumma` are used to match the input conventions of the nitrogen-leaching model.

## Requirements and execution

The script imports `xarray`, `geopandas`, `pandas`, `numpy`, `matplotlib`, and `netCDF4`. Multi-file loading with `xarray.open_mfdataset` also requires Dask.

Before running `python makeEffectiveTemperatureAndRainfall.py`, configure the temperature and precipitation input paths, the municipality shapefile path, and the output path. The output directory must already exist.

## Attribution

The climate datasets are attributed to the Finnish Meteorological Institute and were accessed through Paituli under the CC BY 4.0 licence.

Formal reporting should additionally identify the exact dataset versions, access dates, and the source and licence of the municipality boundary dataset.
