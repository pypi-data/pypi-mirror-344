import cfplot as cfp
import cf
import numpy as np
import matplotlib.pyplot as plt

ddir = "~/summerstudents/datasets"
orog = cf.read(f"{ddir}/1km_elevation.nc")[0]
s = cf.read(f"{ddir}/snowcover")[0]

region = [(-6, 3), (50, 53)]
orog_region = orog.subspace(longitude=cf.wi(*region[0]), latitude=cf.wi(*region[1]))
regrided=s.regrids(orog_region, method="nearest_stod")
c = np.corrcoef(orog_region.data, regrided.data)
