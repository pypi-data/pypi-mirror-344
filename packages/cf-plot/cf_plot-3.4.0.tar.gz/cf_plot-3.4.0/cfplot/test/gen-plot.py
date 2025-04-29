import coverage
import faulthandler
import hashlib
import numpy as np
import unittest

from netCDF4 import Dataset as ncfile
from scipy.interpolate import griddata

import cfplot as cfp
import cf

NUM = "22other"
cfp.setvars(file=f"backup_ref_all/gen_fig{NUM}.png")
data_dir = "cfplot_data"
#  ...


f = cf.read(f"{data_dir}/rgp.nc")[0]

cfp.cscale("plasma")
cfp.mapset(proj="rotated")

cfp.con(f)
