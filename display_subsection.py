#change to use geotiff instead of h5

import matplotlib.pyplot as plt
import seaborn as sns
import rasterio
import matplotlib.pyplot as plt


tiff_file = "friction_map.tif"
# goes down and right (east and south) from point x,y
y = 60
x = -5



start_row =  int((90-y) / 0.008333333333333333333 )
end_row = start_row + 1200
start_col =  int((180+x) / 0.008333333333333333333 )
end_col = start_col + 800


# Open the existing HDF5 file in read mode

with rasterio.open(tiff_file) as src:
    # Read the full first band
    data = src.read(1)

    # Sample the square section
    sampled_section = data[start_row:end_row, start_col:end_col]
    #sampled_section = np.minimum(sampled_section, 113)


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