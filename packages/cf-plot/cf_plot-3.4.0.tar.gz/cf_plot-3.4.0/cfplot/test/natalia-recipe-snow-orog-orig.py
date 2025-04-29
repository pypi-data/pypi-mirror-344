import cfplot as cfp
import cf
import numpy as np
import matplotlib.pyplot as plt

# Read in our data - note we are investigating the influence of the
# land height on the snow cover, so snow cover is the dependent variable
# TODO NATALIA - update these paths to your data
ddir = "~/summerstudents/datasets"
orog = cf.read(f"{ddir}/1km_elevation.nc")[0]
snow = cf.read(f"{ddir}/snowcover")[0]

snow_day = snow[0]  # first day, Jan 1st of this year (2024)

# Choose this region since it is mostly land, to avoid places where the snow
# cover isn't relevant e.g. on the sea.
# TODO NATALIA - choose whatever region you like, but make sure it is n the
# UK-Ireland area since the snow datasets only cover that, and don't make it
# too big - over the whole dataset might crash the regridding on our laptops.
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

# Plot to see what we have so far:
print("SNOW IS", use_snow)
cfp.gopen(file="snow-1.png")
cfp.con(use_snow, lines=False)
cfp.gclose()
print("OROG IS", use_orog)
cfp.gopen(file="orog-1.png")
cfp.con(use_orog, lines=False)
cfp.gclose()


# Now do the regridding to get the same grids, so we have comparable arrays.
# We regrid the orography onto the snow grid since the snow has higher res
# and it will preserve the snow cover which is the 
reg = use_orog.regrids(use_snow, method="linear")
print("REGRIDDED IS", reg, type(reg))
###orog_region, c  # the orography over the UK and the snow cover on the same grid
#a = np.corrcoef(orog_region.data, c.data)
cf.write(reg, "regridded_data.nc")
print("DONE")
cfp.gopen(file="regridded-1.png")
cfp.con(reg, lines=False)
cfp.gclose()


"""
a = np.corrcoef(orog_regridded.data, day_1_snow_cover.data)
np.set_printoptions(threshold=2000)
print(a[0])
"""


"""
elevation = orog_region.subspace(longitude = 2.9875)
# xticks = numpy.linspace(50, 53, num=10)
xticks = [50, 50.5, 51, 51.5, 52, 52.5, 53]


cfp.gopen(figsize=(12, 6), file ="orography_vertical5")

cfp.lineplot(
    x=elevation.coord('latitude').array,
    y=elevation.array.squeeze(),
    color="black",
    title="Orography Profile over part of UK",
    ylabel="Elevation (m)",
    xlabel="Latitude",
    xticks=xticks,
    # xticklabels=xticklabels,
    # yticks=yticks,
    # yticklabels=yticklabels
)

cfp.plotvars.plot.fill_between(
    elevation.coord('latitude').array,
    0,
    elevation.array.squeeze(),
    color='black',
    alpha=0.7
)

cfp.gclose()
"""
