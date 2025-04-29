╰─ python                                                                                 ─╯
Python 3.12.0 | packaged by conda-forge | (main, Oct  3 2023, 08:43:22) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cfplot as cfp
>>> import cf
>>> 
>>> f = cf.read("~/git-repos/vision-project-resources/data/2025-maria-um-hybrid/*.pp")
>>> f
[<CF Field: surface_altitude(latitude(144), longitude(192)) m>,
 <CF Field: air_pressure(time(744), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) Pa>,
 <CF Field: surface_air_pressure(time(24), latitude(144), longitude(192)) Pa>,
 <CF Field: id%UM_m01s00i431_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s00i432_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s00i433_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s00i434_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s00i435_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s00i436_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: air_temperature(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) K>,
 <CF Field: id%UM_m01s34i001_vn1105(time(744), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i009_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i010_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i072_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i073_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i102_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i104_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i108_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i111_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i114_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>,
 <CF Field: id%UM_m01s34i117_vn1105(time(24), atmosphere_hybrid_height_coordinate(85), latitude(144), longitude(192)) 1>]
>>> a = f[-1][0, 0]
>>> a
<CF Field: id%UM_m01s34i117_vn1105(time(1), atmosphere_hybrid_height_coordinate(1), latitude(144), longitude(192)) 1>
>>> cfp.con(a, lines=False)
# Trying stuff out, like:
>>> cfp.con(f[3][0, 60], lines=False)
>>> cfp.con(f[3][0, 50], lines=False)
>>> cfp.con(f[3][0, 70], lines=False)
>>> cfp.con(f[3][0, 65], lines=False)
>>> cfp.cscale("rh_19lev")
>>> cfp.con(f[3][0, 65], lines=False)
>>> cfp.cscale("GreenYellow")
>>> cfp.con(f[3][0, 65], lines=False)
>>> cfp.cscale("thelix")
>>> cfp.con(f[3][0, 65], lines=False)
>>> cfp.cscale("BrBG")
>>> cfp.con(f[3][0, 65], lines=False)
/home/slb93/git-repos/cf-plot/cfplot/cfplot.py:6240: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`). Consider using `matplotlib.pyplot.close()`.
  plotvars.master_plot = plot.figure(figsize=(figsize[0], figsize[1]))
>>> cfp.cscale("BlueDarkOrange18")
>>> cfp.con(f[3][0, 64], lines=False)
>>> cfp.cscale("scale29")
>>> cfp.con(f[3][0, 64], lines=False)
>>> cfp.cscale("scale35")
>>> cfp.con(f[3][0, 66], lines=False)
>>> cfp.cscale("inferno")
>>> cfp.con(f[3][0, 66], lines=False)
>>> cfp.cscale("parula")
>>> cfp.con(f[3][0, 66], lines=False)
>>> cfp.con(f[3][0, 67], lines=False)
>>> cfp.con(f[3][0, 68], lines=False)
>>> cfp.con(f[3][0, 62], lines=False)
# Settle on this one for the swirl:
>>> cfp.con(f[13][0, 64], lines=False)
