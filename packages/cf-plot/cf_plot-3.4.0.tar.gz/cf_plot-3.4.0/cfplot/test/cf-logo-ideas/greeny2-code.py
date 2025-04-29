╰─ python                                                                                 ─╯
Python 3.12.0 | packaged by conda-forge | (main, Oct  3 2023, 08:43:22) [GCC 12.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import cfplot as cfp
>>> import cf
>>> 
>>> f = cf.read("~/git-repos/vision-project-resources/data/2025-maria-um-hybrid/*.pp")
>>> 
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
>>> 
>>> cfp.mapset(proj="ortho")
>>> cfp.cscale("precip_diff_12lev")
>>> cfp.con(f[10][10, 61], lines=False)
