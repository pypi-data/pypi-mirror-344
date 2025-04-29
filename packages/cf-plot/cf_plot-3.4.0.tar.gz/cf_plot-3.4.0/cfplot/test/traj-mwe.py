import cfplot as cfp
import cf

DATA_PATH = "/home/slb93/git-repos/cf-python/cf/test/dsg_trajectory.nc"

f = cf.read(DATA_PATH)[0]
print(f)

###cfp.traj(f)
cfp.lineplot(f)
print("Success - check plot for a plotted trajectory")
