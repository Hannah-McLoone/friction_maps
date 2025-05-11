#change to use geotiff instead of h5

import matplotlib.pyplot as plt
import seaborn as sns
import rasterio
import matplotlib.pyplot as plt


tiff_file = "friction_map.tif"


#change this so i dont need to do w load of maths!!!!!!!!!!!!!!!!!!!! it just uses tiff referennceing 
min_lon, min_lat = -11.0, 50  # example lower-left corner
max_lon, max_lat = 2, 60  # example upper-right corner

with rasterio.open(tiff_file) as src:
    # Convert coordinates to row, col indices
    start_col, start_row = src.index(min_lon, max_lat)  # top-left
    end_col, end_row = src.index(max_lon, min_lat)      # bottom-right

    # Read the full first band
    data = src.read(1)

    # Sample the square section
    sampled_section = data[start_row:end_row, start_col:end_col]



rows, cols = sampled_section.shape

# Set figsize proportional to the array dimensions
aspect_ratio = cols / rows
base_size = 5  # Adjust this value as needed for better scaling
fig_width = base_size * aspect_ratio if aspect_ratio > 1 else base_size
fig_height = base_size / aspect_ratio if aspect_ratio < 1 else base_size

# Create the heatmap
plt.figure(figsize=(fig_width, fig_height))
sns.heatmap(sampled_section, cmap="viridis", annot=False, cbar=False)
plt.title("Heatmap of Sampled Data")
plt.show()