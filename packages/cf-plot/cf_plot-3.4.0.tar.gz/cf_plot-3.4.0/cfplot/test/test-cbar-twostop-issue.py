import numpy as np
import cfplot as cfp
import cf

f = cf.read('cfplot_data/Geostropic_Adjustment.nc')[0]
r = f.subspace[9]

# ORIG CODE FROM USER
# r=cf.read(dwp+'praw_mon_OBS_*.nc')[0]
# cmix=[-3.5,-2.5,-1.5,-1,-0.5,0,0.5,1,1.5,2.5,3.5];
# cti='regression slope (mm day$^{-1}$ PW$^{-1}$)'
# cfp.cscale('scale1',ncols=len(cmix)+1, white=[5,6], reverse=True)
# cfp.levs(manual=cmix)
# cfp.con(r,lines=False,colorbar_title=cti,colorbar_label_skip=None)

cmix_1 = list(np.arange(-3.5, 3.5, 0.5))
cmix_2 = list(np.arange(-3.5, 3.5, 0.25))
cfp.levs(manual=cmix_1)
###cfp.cbar(labels=[str(i) for i in cmix_1])

cfp.con(r, lines=False, colorbar_labels=[str(i) for i in cmix_2])


