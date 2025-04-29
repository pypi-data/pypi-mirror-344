>>> f = cf.read("~/recipes/northward.nc")
>>> f
[<CF Field: northward_wind(time(1980), latitude(144), longitude(192)) m s-1>]
>>>
>>> cfp.mapset(proj="ortho")
>>> cfp.con(f[0][1], lines=False)
>>> cfp.con(f[0][100], lines=False)
>>> cfp.con(f[0][300], lines=False)
>>> cfp.con(f[0][400], lines=False)
>>> cfp.cscale("amwg256")
>>> cfp.con(f[0][400], lines=False)
>>> cfp.cscale("BlueDarkOrange18")
>>> cfp.con(f[0][400], lines=False)
>>> cfp.cscale("GreenMagenta16")
>>> cfp.con(f[0][150], lines=False)
>>> cfp.con(f[0][250], lines=False)
>>> cfp.con(f[0][350], lines=False)
>>> cfp.con(f[0][360], lines=False)
>>>
