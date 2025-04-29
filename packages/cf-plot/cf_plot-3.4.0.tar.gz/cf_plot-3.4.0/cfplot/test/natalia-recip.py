import cfplot as cfp
import cf
import sys
import scipy.stats.mstats as mstats
import matplotlib.pyplot as plt

# Read in our data - note we are investigating the influence of the
# land height on the snow cover, so snow cover is the dependent variable
ddir = "~/summerstudents/datasets"
orog = cf.read(f"{ddir}/1km_elevation.nc")[0]
snow = cf.read(f"{ddir}/snowcover")[0]

snow_day = snow[0]  # first day, Jan 1st of this year (2024)

# Choose this region since it is mostly land, to avoid places where the snow
# cover isn't relevant e.g. on the sea.
# TODO NATALIA - choose whatever region you like, but make sure it is n the
# UK-Ireland area since the snow datasets only cover that, and don't make it
# too big - over the whole dataset might crash the regridding on our laptops.
# I used this online tool to help me find lat and lon points to get a
# rectangular area:
# https://www.findlatitudeandlongitude.com/l/Yorkshire%2C+England/5009414/
region_in_mid_uk = [(-3.0, -1.0), (52.0, 55.0)]  # lon then lat
use_orog = orog.subspace(
    longitude=cf.wi(*region_in_mid_uk[0]),
    latitude=cf.wi(*region_in_mid_uk[1])
)
# Subspace snow to same bounding box as orog
use_snow = snow_day.subspace(
    longitude=cf.wi(*region_in_mid_uk[0]),
    latitude=cf.wi(*region_in_mid_uk[1])
)

use_snow_normal = use_snow
"""
#Normalise the data
use_snow_normal = ((use_snow - use_snow.minimum())/ (use_snow.range()))*100 #This normalises to between 0 and 1 so multiply by 100 to get a percentage
print(use_snow_normal.data.stats())
# Resassign the units as are removed by cf-python after calculation
use_snow_normal.override_units("percentage", inplace=True) #only do this if you are certain the unist are convertible to %
"""


# Plot of Snowcover contour
print("SNOW IS", use_snow_normal)
cfp.gopen(file="snow-1.png")
###cfp.cscale("/home/natalia/cfplot_data/colour_scale.txt")
cfp.mapset(resolution="10m")
cfp.con(use_snow_normal, lines=False, title = "Snow Cover Contour Plot", xticklabels = ("3W", "2W", "1W"), yticklabels =("52N", "53N", "54N", "55N"), xticks = (-3, -2, -1), yticks= (52, 53, 54, 55))
cfp.gclose()
print("OROG IS", use_orog)
# Plot of 1km Resolution Orography Contour
cfp.gopen(file="orog-1.png")
cfp.cscale("wiki_2_0_reduced")
cfp.mapset(resolution="10m")
cfp.con(use_orog, lines=False, title = "1km resolution Orography Contour Plot", xticklabels = ("3W", "2W", "1W"), yticklabels =("52N", "53N", "54N", "55N"), xticks = (-3, -2, -1), yticks= (52, 53, 54, 55))
cfp.gclose()
# Note we don't need to colour out the ocean for the orog because when we
# regrid it it gets masked by the lack of data for the snow cover over the seas
# - would be good to mention this in your recipe.

#Plot of Vertical Orography Lineplot of 1km Resolution Elevation
lonz = use_orog.construct("longitude").data[0]
elevation_orog = use_orog.subspace(longitude = lonz)
xticks_elevation_orog = [52, 52.5, 53, 53.5, 54, 54.5, 55]

cfp.gopen(figsize=(12, 6), file ="orography_vertical_final.png")

cfp.lineplot(
    x=elevation_orog.coord('latitude').array,
    y=elevation_orog.array.squeeze(),
    color="black",
    title="Orography Profile over part of UK",
    ylabel="Elevation (m)",
    xlabel="Latitude",
    xticks=xticks_elevation_orog,
)

cfp.plotvars.plot.fill_between(
    elevation_orog.coord('latitude').array,
    0,
    elevation_orog.array.squeeze(),
    color='black',
    alpha=0.7
)
cfp.gclose()


# TODO NATALIA - use this code first, then once it has run and generated
# the regridded dataset, you can just read that in instead, as below currnetly.

# Now do the regridding to get the same grids, so we have comparable arrays.
# We regrid the orography onto the snow grid since the snow has higher res
# and it will preserve the snow cover which is the 
reg = use_orog.regrids(use_snow_normal, method="linear")
print("REGRIDDED IS", reg, type(reg))
cf.write(reg, "regridded_data.nc")
print("DONE WRITING OUT REGRID FILE")
cfp.gopen(file="regridded-1.png")
cfp.con(reg, lines=False)
cfp.gclose()

###reg = cf.read("~/cfplot_data/regridded_data.nc")[0]

# Now we compare te 'reg' field which is the elevation data on the same grid
# as the snow data, to the snow data itself i.e. compare 'reg' and 'use_snow'
reg_data = reg.data
snow_data = use_snow_normal.data
print("(REGRIDDED) OROG DATA IS", reg_data, reg_data.shape)
print("SNOW DATA IS", snow_data, snow_data.shape)

# Need to squeeze snow data to remove the size 1 axes
# TODO NATALIA - can/should we move this to the start of the recipe?
snow_data = snow_data.squeeze()

# NOw for the statistical caulcations
###sys.setrecursionlimit(1500)
print("ARRAY IS", reg_data.array)
coeff = mstats.pearsonr(reg_data.array, snow_data.array)
print(coeff)



# TODO NATALIA - find an appropriate point in your version of this code
# to include a plot of the orography profile - your lineplot code. Ideally
# you can show this for some data from the reg regidded orography and plot
# on top of that a lineplot with a separate axis to show the snow cover
# across that cross-section. But only if you have time! The plot just
# of the orography profile would be nice on its own if you don't have
# time to add the snow cover lineplot on that.
