import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

cost_map = np.load('cost_map2.npy')
#cost_map = cost_map[1050:2600,900:4000]

cost_map = cost_map[::10, ::10]
cost_map = np.minimum(cost_map, 1000)

from matplotlib.colors import LogNorm
#plt.imshow(cost_map, norm=LogNorm(vmin=0.1, vmax=1000), cmap='viridis_r')  # Adjust vmin/vmax as needed

from matplotlib.colors import PowerNorm

plt.imshow(cost_map, norm=PowerNorm(gamma=0.2), cmap='viridis_r')


#--------display-------------
#sns.heatmap(cost_map, cmap="viridis_r", annot=False, cbar=False)
plt.title("Heatmap of Sampled Data")
plt.show()