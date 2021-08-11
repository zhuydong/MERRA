import pandas as pd
import MySQLdb
import cartopy.crs as ccrs
sql_cmd = 'select lon,lat,AVG(TO3) as TO3 FROM t03_400 GROUP BY lon,lat;' # lon可以换成lat，l4b_010是ncco2数据库（其中之一）的表名

con = MySQLdb.connect(host='localhost',
                      user='root',
                      password='123456',
                      database='merra_400')
df = pd.read_sql(sql_cmd, con)
print(df)

lons = df['lon']
lats = df['lat']
TO3 = df['TO3']

# Start Plotting Data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.basemap import Basemap

map = Basemap(resolution='l', projection='eck4', lat_0=0, lon_0=0)

lon, lat = np.meshgrid(lons, lats)
xi, yi = map(lon, lat)
print(TO3)
print(yi)
df1 = pd.pivot_table(df, index='lon', columns='lat', values='TO3')
print(df1)

# Plot Data
cs = map.pcolor(xi,yi,df1,cmap=cm.jet)
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

# plt.show()
