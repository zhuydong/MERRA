# this script will read-in and plot 3-dimensional NetCDF data in python
from netCDF4 import Dataset

# Read in NetCDF4 file. Assign directory path if necessary.
data = Dataset('D:\wget\MERRA2_400.tavgM_2d_slv_Nx.202102.nc4', mode='r')

# Uncomment 'print data' line to print MERRA2 metadata. This line will print attribute and variable information.
# from the 'variables(dimensions)' list, choose which variable(s) to read in below.
# print data


# Read in 'T2M' 2-meter air temperature variable. Varible names can be printed by uncommenting 'print data' above.
lons = data.variables['lon'][:]
lats = data.variables['lat'][:]
T2M = data.variables['T2M'][:,:,:]

# If using MERRA-2 data with multiple time indices, line 19 will subset the first time dimension.
# Changing T2M[0,:,:] to T2M[10,:,:] will subset to the 11th time index.
T2M = T2M[0,:,:]

# Start Plotting Data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

map = Basemap(resolution='l', projection='eck4', lat_0=0, lon_0=0)

lon, lat = np.meshgrid(lons, lats)
xi, yi = map(lon, lat)

print(np.squeeze(T2M))
# Plot Data
cs = map.pcolor(xi,yi,np.squeeze(T2M), vmin=np.min(T2M), vmax=np.max(T2M), cmap=cm.jet)
cs.set_edgecolor('face')

# Add Grid Lines
map.drawparallels(np.arange(-90., 90., 15.), labels=[1,0,0,0], fontsize=5)
map.drawmeridians(np.arange(-180., 180., 30.), labels=[0,0,0,1], fontsize=4)

# Add Coastlines, States, and Country Boundaries
map.drawcoastlines()
map.drawstates()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs,location='bottom', pad="10%")
cbar.set_label('K')
cbar.ax.tick_params(labelsize=10)

# Add Title
plt.title('MERRA-2 2-meter air temperature (2021-02)')

# Save figure as PDF
# plt.savefig('MERRA2_2m_airTemp_TEST.pdf', format='pdf', dpi=360)
plt.show()