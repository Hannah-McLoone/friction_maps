import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Path to the GeoTIFF file
tiff_file = "friction_map.tif"

# Sampling intervals
row_stride = 11  # Adjust based on desired downsampling
col_stride = 11  # Adjust based on desired downsampling

# Open the GeoTIFF file
with rasterio.open(tiff_file) as src:
    # Read the first band
    data = src.read(1)

    # Display the original shape of the dataset
    print(f"Original dataset shape: {data.shape}")

    # Downsample by selecting every 'row_stride'th row and 'col_stride'th column
    downsampled_data = data[::row_stride, ::col_stride]

    # Clip values to a maximum of 100 (if desired)
    downsampled_data = np.minimum(downsampled_data, 100)

# Plot the downsampled data as a heatmap
plt.imshow(downsampled_data, cmap='viridis', aspect='auto')
plt.colorbar()
plt.title("Downsampled Heatmap")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.show()
