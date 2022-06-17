from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

minorLocator = AutoMinorLocator()


def radial_profile(data, center):
    print(data.shape)
    x, y = np.indices((data.shape))
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    r = r.astype(np.int)

    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr
    return radialprofile 


fitsFile = fits.open('/Volumes/EVE/Lab_Data/MTF/20220520_031637_IFS_MTF_100X/analysis/wffftgt_20220520_031816_0010_corr.fit')
img = fitsFile[0].data
img[np.isnan(img)] = 0

center = np.unravel_index(img.argmax(), img.shape)
rad_profile = radial_profile(img, center)

fig, ax = plt.subplots()
plt.plot(rad_profile[0:22], 'x-')

ax.xaxis.set_minor_locator(minorLocator)

plt.tick_params(which='both', width=2)
plt.tick_params(which='major', length=7)
plt.tick_params(which='minor', length=4, color='r')
plt.grid()
ax.set_xlabel("Pixels")
plt.grid(which="minor")
plt.show()