import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Path to the GeoTIFF file
tiff_file = "/maps/hm708/combined_friction_map.tif"

# Sampling intervals
row_stride = 30  # Adjust based on desired downsampling
col_stride = 30  # Adjust based on desired downsampling

# Output image file path
output_image = "/maps/hm708/land_friction_map_downsampled.png"

# Open the GeoTIFF file
with rasterio.open(tiff_file) as src:
    # Read the first band
    data = src.read(1)
    print(f"Original dataset shape: {data.shape}")

    # Downsample by selecting every 'row_stride'th row and 'col_stride'th column
    downsampled_data = data[::row_stride, ::col_stride]

# Plot the downsampled data as a heatmap and save as image
plt.figure(figsize=(10, 8))
plt.imshow(downsampled_data, cmap='viridis', aspect='auto')
plt.colorbar()
plt.title("Downsampled Heatmap")
plt.xlabel("Columns")
plt.ylabel("Rows")

# Save the figure to a file instead of showing it
plt.savefig(output_image, dpi=300, bbox_inches='tight')
plt.close()

print(f"Downsampled heatmap saved as: {output_image}")



"""
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Path to the GeoTIFF file
tiff_file = "/maps/hm708/land_friction_map.tif"

# Sampling intervals
row_stride = 50  # Adjust based on desired downsampling
col_stride = 50  # Adjust based on desired downsampling

# Open the GeoTIFF file
with rasterio.open(tiff_file) as src:
    # Read the first band
    data = src.read(1)
    print(f"Original dataset shape: {data.shape}")

    # Downsample by selecting every 'row_stride'th row and 'col_stride'th column
    downsampled_data = data[::row_stride, ::col_stride]

# Plot the downsampled data as a heatmap
plt.imshow(downsampled_data, cmap='viridis', aspect='auto')
plt.colorbar()
plt.title("Downsampled Heatmap")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.show()
"""