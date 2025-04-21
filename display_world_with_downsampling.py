import h5py
import numpy as np
import matplotlib.pyplot as plt

h5_file = "uk2_roads_other.h5"
# Sampling intervals
row_stride = 11  # Adjust based on desired downsampling
col_stride = 11 # Adjust based on desired downsampling

with h5py.File(h5_file, "r") as f:
    # Automatically retrieve the first dataset
    dataset = next(iter(f.values()))
    
    # Display the original shape of the dataset
    print(f"Original dataset shape: {dataset.shape}")
    
    # Downsample by selecting every 'row_stride'th row and 'col_stride'th column
    downsampled_data = dataset[::row_stride, ::col_stride]

    downsampled_data = np.minimum(downsampled_data, 100)

# Plot the downsampled data as a heatmap
plt.imshow(downsampled_data, cmap='viridis', aspect='auto')
plt.colorbar()
plt.title("Downsampled Heatmap")
plt.xlabel("Columns")
plt.ylabel("Rows")
plt.show()
