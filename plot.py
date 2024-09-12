import numpy as np
from matplotlib import pyplot as plt
plt.style.use('K_PAPER')


eigen_data = np.load('eigen_press.npy')
pertu_data = np.load('perturbed_frequency.npy')
print(pertu_data)

fig, ax = plt.subplots(1,2, figsize = (10,5))
ax[0].scatter(np.arange(0,49,1), np.diff(eigen_data))
ax[0].scatter(np.arange(0,49,1), np.diff(pertu_data))

eigen_data = np.diff(eigen_data)
pertu_data = np.diff(pertu_data)

ax[1].hist(eigen_data-np.mean(eigen_data), bins = 15, histtype = 'step')
ax[1].hist(pertu_data-np.mean(pertu_data), bins = 15, histtype = 'step')
plt.show()
