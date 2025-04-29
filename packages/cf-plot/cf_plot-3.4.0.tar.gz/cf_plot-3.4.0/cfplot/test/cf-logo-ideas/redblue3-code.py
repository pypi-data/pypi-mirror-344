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

...
etc., as before

cfp.cscale("WhiteBlueGreenYellowRed")
cfp.con(f[3][20, 50], lines=False)

