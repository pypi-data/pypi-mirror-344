import matplotlib.pyplot as plt
import numpy as np

import matplotlib.animation as animation

import cfplot as cfp
import cf


mpl_fig, _ = plt.subplots()


f=cf.read('cfplot_data/ggap.nc')
f1 = f[1]
f2 = f[2]
print("f1 PRESSURES:", f1.construct("pressure").array)
print("f1 PRESSURE:", f1.construct("pressure").array)

pressure_vals = f1.construct("pressure").array


# Set smaller map
cfp.mapset(-2, 2, 50, 54, resolution='110m')

ims = []
cfp.gopen()
u = f1.subspace(pressure=pressure_vals[0])
cfp.con(u, blockfill=True, lines=False)

print("PLOTVARS ARE", cfp.plotvars)
fig = cfp.plotvars.plot.figure
###fig_2 = fig.copy()
mm = cfp.plotvars.mymap
plot = cfp.plotvars.plot
print("FIG IS", fig, type(fig))
print(dir(fig))
print("MM IS", mm, type(mm))
print(dir(mm))
###cfp.gclose(view=False)

###cfp.gclose(view=False)
ims.append([fig,])  # see below, need sequence
mpl_fig.add_artist(fig)


def update_animation(subspace_at):
    """TODO"""
    cfp.gopen()
    u = f1.subspace(pressure=subspace_at)
    ###v=f2.subspace(pressure=subspace_at)
    cfp.con(u, blockfill=True, lines=False)  #, v=v, key_length=10, scale=100, stride=5)
    mpl_fig.add_artist(cfp.plotvars.plot.figure)
    ###plot = cfp.plotvars.plot.figure  ###figure  ###mymap.figure
    #-#plot2 = plot  ###.copy()
    ###return fig
    ###cfp.gclose(view=False)
    #-#return plot



for v in pressure_vals[:5]:
    # Note need to add a SQUENCE of images each time, not just one!
    # Or get: TypeError: 'Figure' object is not iterable
    ims.append([update_animation(v)])


"""
# Create animation from the images
ani = animation.FuncAnimation(
    fig, update_animation, ###init=init,
    frames=pressure_vals[1:5],  # TODO all later
    ###init_func=init, blit=True
)
"""

print("IMS", ims)
ims1 = ims[-1][0]
print("IMS LAST IS", ims1, type(ims1), dir(ims1))
ani = animation.ArtistAnimation(
    mpl_fig, ims, interval=50, ###blit=True,
    ###repeat_delay=1000
)
cfp.gclose(view=False)


# Save or show
ani.save("movie.mp4")

###plt.show()
