import cfplot as cfp
import cf
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import scipy.mstats

# Allows us to see more of an array when we print them
np.set_printoptions(threshold=5000)

# Read in our data - note we are investigating the influence of the
# land height on the snow cover, so snow cover is the dependent variable
# TODO NATALIA - update these paths to your data
ddir = "~/summerstudents/datasets"
orog = cf.read(f"{ddir}/1km_elevation.nc")[0]
snow = cf.read(f"{ddir}/snowcover")[0]

# TODO SADIE we can change day to see different results
snow_day = snow[0]  # first day, Jan 1st of this year (2024)

snow_day.dump()

#print(snow_day.data[0].array)
#print(snow_day.data.statistics())

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
# Normalise snow data
norm_s = (use_snow - use_snow.minimum())/use_snow.range()
norm_s_2 = (use_snow - use_snow.minimum())/(
    use_snow.maximum()-use_snow.minimum())

print(norm_s.count_masked(), norm_s.size - norm_s.count_masked())
# This print out confirms that the data has max of 1, min of 0 i.e. has been
# normalised properly as we wanted!
print("STATS ARE:", norm_s.data.stats())

# Because the units are prcentages, we want between 0 and 100 not 0 and 1:
percentage_s = norm_s * 100



# Plot to see what we have so far:
print("SNOW IS", use_snow)
# TODO NATALIA - Change snow plot to use a nice colour map where the
# highest parts
# are white like snow (or whatever colour map you think is suitable)!
cfp.gopen(file="snow-2.png")
cfp.con(use_snow, lines=False)
cfp.gclose()
print("OROG IS", use_orog)
# TODO NATALIA - Change orog plot to use a suitable different colour map to
# the snow one, to make it clear which is which.
# TODO NATALIA - add titles and axes labels etc. to these plots
cfp.gopen(file="orog-2.png")
cfp.con(use_orog, lines=False)
cfp.gclose()
# Note we don't need to colour out the ocean for the orog because when we
# regrid it it gets masked by the lack of data for the snow cover over the seas
# - would be good to mention this in your recipe.


# TODO NATALIA - use this code first, then once it has run and generated
# the regridded dataset, you can just read that in instead, as below currnetly.

# Now do the regridding to get the same grids, so we have comparable arrays.
# We regrid the orography onto the snow grid since the snow has higher res
# and it will preserve the snow cover which is the 
reg = use_orog.regrids(use_snow, method="linear")
print("REGRIDDED IS", reg, type(reg))
cf.write(reg, "regridded_data.nc")
print("DONE WRITING OUT REGRID FILE")
cfp.gopen(file="regridded-2.png")
cfp.con(reg, lines=False)
cfp.gclose()

###reg = cf.read("regridded_data.nc")[0]

# Now we compare te 'reg' field which is the elevation data on the same grid
# as the snow data, to the snow data itself i.e. compare 'reg' and 'use_snow'
reg_data = reg.data
snow_data = use_snow.data
print("(REGRIDDED) OROG DATA IS", reg_data, reg_data.array)
print("SNOW DATA IS", snow_data, snow_data.array)

# Need to squeeze snow data to remove the size 1 axes
# TODO NATALIA - can/should we move this to the start of the recipe?
snow_data = snow_data.squeeze()

# NOw for the statistical caulcations

# NOte on the stats here:
# "The Pearson product-moment correlation coefficient (np.corrcoef) is
# simply a normalized version of a cross-correlation (np.correlate)"
# See e.g.: https://stackoverflow.com/a/74544488

"""
# We can calulate a whole array of the correlation matrix like so:
# (see https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html)
matrix_of_coef = np.corrcoef(reg_data, snow_data)
print("COEF MATRIX IS", matrix_of_coef, matrix_of_coef.shape)

# But really want a single value to describe the Pearon coefficient across
# the two arrays, for this you flatten them down like so and we need to take
# element C[0, 1] which corresponds to the 
scalar_repr_coef = np.corrcoef(
    reg_data.flatten(), snow_data.flatten())[0, 1]

print("FINAL COEFFICIENT IS:", scalar_repr_coef)
"""
# OKAY the above gives a stupid value, -0.47 implying higher means less
# snow coverage! But the reason is that the masked data is not accounting
# for preoperly, numpy is treating it as a feature of the data.
# Since masking is causing issue, so we need to use numpy.ma module instead.
# See: https://numpy.org/doc/stable/reference/generated/numpy.ma.corrcoef.html
# "Except for the handling of missing data this function does the same as
# numpy.corrcoef. For more details and examples, see numpy.corrcoef."
"""
ma_matrix_of_coef = ma.corrcoef(reg_data, snow_data)
print("COEF MATRIX IS", ma_matrix_of_coef, ma_matrix_of_coef.shape)
"""

"""
# But really want a single value to describe the Pearon coefficient across
# the two arrays, for this you flatten them down like so and we need to take
# element C[0, 1] which corresponds to the 
ma_scalar_repr_coef = ma.corrcoef(
    np.ravel(reg_data), np.ravel(snow_data))[0, 1]

print("FINAL COEFFICIENT IS:", ma_scalar_repr_coef)
# I got:
# COEF MATRIX IS [[-- -- -- ... -- -- --]
#  [-- 1.0 0.9848885835264989 ... 0.06950057927585655 -0.2069363180554349
#   --]
#  [-- 0.9848885835264989 1.0 ... 0.10663913541236082 -0.25166350213217803
#   --]
#  ...
#  [-- 0.06950057927585655 0.10663913541236082 ... 1.0 0.5952636247243812
#   --]
#  [-- -0.2069363180554349 -0.25166350213217803 ... 0.5952636247243812 1.0
#   --]
#  [-- -- -- ... -- -- --]] (1200, 1200)
# FINAL COEFFICIENT IS: 0.35867270467640366
"""

print("CALC PEARSONR", reg_data, snow_data, reg_data.size, snow_data.size)
p = scipy.mstats.pearsonr(reg_data, snow_data)
print("PEARSONR IS:", p)

# TOO NATALIA - find an appropriate point in your version of this code
# to include a plot of the orography profile - your lineplot code. Ideally
# you can show this for some data from the reg regidded orography and plot
# on top of that a lineplot with a separate axis to show the snow cover
# across that cross-section. But only if you have time! The plot just
# of the orography profile would be nice on its own if you don't have
# time to add the snow cover lineplot on that.
