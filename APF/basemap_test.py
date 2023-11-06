from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

fig=plt.figure()
ax=fig.add_axes([0.1,0.1,0.8,0.8])
mymap = Basemap(llcrnrlon=-100.,llcrnrlat=20.,urcrnrlon=20.,urcrnrlat=60.,\
            rsphere=(6378137.00,6356752.3142),\
            resolution='l',projection='merc',\
            lat_0=40.,lon_0=-20.,lat_ts=20.)
# nylat, nylon are lat/lon of New York
nylat = 40.78; nylon = -73.98
# lonlat, lonlon are lat/lon of London.
lonlat = 51.53; lonlon = 0.08
mymap.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
mymap.plot([nylon,lonlon],[nylat,lonlat],linewidth=2,color='r',latlon='True')
mymap.drawcoastlines()
mymap.fillcontinents()
mymap.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
mymap.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.show()