#change to use geotiff instead of h5

import matplotlib.pyplot as plt
import seaborn as sns
import rasterio
import matplotlib.pyplot as plt


tiff_file = "/maps/hm708/please_work.tif"



#min_lon, min_lat =  50, -11.0, # example lower-left corner
#max_lon, max_lat = 60, 2  # example upper-right corner

with rasterio.open(tiff_file) as src:
    # Convert coordinates to row, col indices
    start_row, start_col = src.index(0, 10)  # top-left
    end_row, end_col = src.index(10, 0)      # bottom-right

    print(start_col, end_col)
    print(start_row, end_row)


    # Read the full first band
    data = src.read(1)

    # Sample the square section
    sampled_section = data[start_row:end_row, start_col:end_col]



rows, cols = sampled_section.shape
print(sampled_section.shape)
# Set figsize proportional to the array dimensions

"""
aspect_ratio = cols / rows
base_size = 5  # Adjust this value as needed for better scaling
fig_width = base_size * aspect_ratio if aspect_ratio > 1 else base_size
fig_height = base_size / aspect_ratio if aspect_ratio < 1 else base_size

# Create the heatmap
plt.figure(figsize=(fig_width, fig_height))
"""
plt.figure(figsize=(10,10))
sns.heatmap(sampled_section, cmap="viridis", annot=False, cbar=False)
plt.title("Heatmap of Sampled Data")


plt.savefig('map.png', dpi=300, bbox_inches='tight')
plt.close()
