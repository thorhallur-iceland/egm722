import geopandas as gpd
from geopandas import GeoDataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd



# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


plt.ion()

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
counties = gpd.read_file('data_files/Counties.shp')
wards = gpd.read_file('data_files/NI_Wards.shp')
max_area = counties['Area_SqKM'].max()
min_area = counties['Area_SqKM'].min()
mean_area = counties['Area_SqKM'].mean()
sum_area = counties['Area_SqKM'].sum()
print(counties[counties['Area_SqKM'] > 10])
print("max area: {0} km2".format(max_area))
print("min area: {0} km2".format(min_area))
print("mean area: {0} km2".format(mean_area))
print("sum area: {0} km2".format(counties['Area_SqKM'].sum()))
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection
# create a scale bar of length 20 km in the upper right corner of the map
def scale_bar(ax, location=(0.92, 0.95)):
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]

    tmc = ccrs.TransverseMercator(sbllx, sblly)
    x0, x1, y0, y1 = ax.get_extent(tmc)
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    plt.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=tmc)
    plt.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=tmc)
    plt.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=tmc)

    plt.text(sbx, sby-4500, '20 km', transform=tmc, fontsize=8)
    plt.text(sbx-12500, sby-4500, '10 km', transform=tmc, fontsize=8)
    plt.text(sbx-24500, sby-4500, '0 km', transform=tmc, fontsize=8)



# your analysis goes here...

# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
myCRS = ccrs.UTM(29)
# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False


# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(county_outlines)
county_handles = generate_handles([''], ['none'], edge='r')

ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

print(myCRS)
plt.show()

# save the figure
# fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')
fig.savefig('mapex3.png', dpi=300, bbox_inches='tight')