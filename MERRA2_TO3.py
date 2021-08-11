from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
# 读取nc文件
dataset = Dataset('E:\PycharmProjects\yiyue\MERRA2_400.tavgM_2d_chm_Nx.202101.nc4', mode='r', format='NETCDF4')
# # 查看信息
# print(dataset)
# 查看变量
print('变量:',dataset.variables.keys())
# # 查看某个变量的信息
# print(dataset.variables['lon'])
# # 查看某个变量的属性
# print(dataset.variables['lon'].ncattrs())
# # 查看变量的值
# print(dataset.variables['lon'][:])
lons = dataset.variables['lon'][:]
lats = dataset.variables['lat'][:]
TO3 = dataset.variables['TO3'][0,:,:]
print(dataset.variables['TO3'][0,:,:])

# Start Plotting Data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

map = Basemap(resolution='l', projection='eck4', lat_0=0, lon_0=0)

lon, lat = np.meshgrid(lons, lats)
xi, yi = map(lon, lat)


# Plot Data
cs = map.pcolor(xi,yi,np.squeeze(TO3), vmin=np.min(TO3), vmax=np.max(TO3), cmap=cm.jet)
cs.set_edgecolor('face')

# Add Grid Lines
map.drawparallels(np.arange(-90., 90., 15.), labels=[1,0,0,0], fontsize=5)
map.drawmeridians(np.arange(-180., 180., 30.), labels=[0,0,0,1], fontsize=4)

# Add Coastlines, States, and Country Boundaries
map.drawcoastlines()
map.drawstates()
map.drawcountries()

# Add Colorbar
cbar = map.colorbar(cs, location='bottom', pad="10%")
# cbar.set_label('K')
cbar.ax.tick_params(labelsize=10)

# Add Title
plt.title('MERRA-2 Global total_column_ozone (2021-01)')

# Save figure as PDF
# plt.savefig('MERRA2_2m_airTemp_TEST.pdf', format='pdf', dpi=360)
plt.show()

# https://theonegis.blog.csdn.net/article/details/50805408?utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-15.control&dist_request_id=&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-15.control
