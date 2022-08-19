#Measuring Stripes

from matplotlib import pyplot as plt
import skimage
from astropy.io import fits
import numpy as np
from matplotlib import colors
import sys
import os
import glob

def stripe_read(fl):

	file = open("IR.txt", "w")

	head, tail = os.path.split(fl)

	fitsFile = fits.open(fl)

	img = fitsFile[0].data

	right_start = (1850, 4013)

	right_end = (1886, 4013)

	left_start = (1850, 85)

	left_end = (1886, 85)

	center_start = (1850, 2110)

	center_end = (1886, 2110)

	right_profile = skimage.measure.profile_line(img, right_start, right_end, linewidth=1)

	left_profile = skimage.measure.profile_line(img, left_start, left_end, linewidth=1)

	center_profile = skimage.measure.profile_line(img, center_start, center_end, linewidth=1)

	left_x_array = np.arange(1850, 1886  + 1)

	right_x_array = np.arange(1850, 1886  + 1)

	center_x_array = np.arange(1850, 1886 + 1)






	ax1 = plt.subplot(2, 2, 4)
	ax1.imshow(img, cmap='gray')
	ax1.plot([left_start[1], left_end[1]], [left_start[0], left_end[0]], 'r', linewidth=(2))
	ax1.plot([right_start[1], right_end[1]], [right_start[0], right_end[0]], 'r', linewidth=(2))
	ax1.plot([center_start[1], center_end[1]], [center_start[0], center_end[0]], 'r', linewidth=(2))
	ax1.invert_yaxis()


	ax2 = plt.subplot(2, 2, 1)
	ax2.plot(left_x_array, left_profile, "-o")
	ax2.set_title('IR1 across 86(x)')
	ax2.plot(1851, 366.5, "o", label="Dark", color="black")
	ax2.plot(1852, 883.5, "s",label="Closest to Half Max", color="Gray")
	ax2.axhline(y= np.amax(left_profile) // 2, color='r', linestyle='--')
	ax2.plot(1885, 209, "o", label="Dark", color="black")
	ax2.plot(1884, 605, "s",label="Closest to Half Max", color="Gray")
	ax2.legend(['Values from 1850 to 1886', 'Dark Edges (1851, 1885)' + "\n" + "(33 rows between them)", "Closest to Half Max (1852, 1884)" + "\n" + "(31 rows between them)", "Approximate half max for filter"])



	ax3 = plt.subplot(2, 2, 2)
	ax3.plot(right_x_array, right_profile, "-o")
	ax3.set_title('IR1 across 4014  (x)')
	ax3.plot(1851, 281.5, "o", label="Dark", color="black")
	ax3.plot(1852, 783, "s",label="Closest to Half Max", color="Gray")
	ax3.axhline(y= np.amax(right_profile) // 2, color='r', linestyle='--')
	ax3.plot(1885, 170, "o", label="Dark", color="black")
	ax3.plot(1883, 1075, "s",label="Closest to Half Max", color="Gray")
	ax3.legend(['Values from 1850 to 1886', 'Dark Edges (1851, 1885)' + "\n" + "(33 rows between them)", "Closest to Half Max (1852, 1883)" + "\n" + "(30 rows between them)", "Approximate half max for filter"])
	

	ax4 = plt.subplot(2, 2, 3)
	ax4.plot(center_x_array, center_profile, "-o")
	ax4.set_title('IR1 across 2111  (x)')
	ax4.plot(1851, 391.5, "o", label="Dark", color="black")
	ax4.plot(1852, 1070, "s",label="Closest to Half Max", color="Gray")
	ax4.axhline(y= np.amax(center_profile) // 2, color='r', linestyle='--')
	ax4.plot(1885, 191, "o", label="Dark", color="black")
	ax4.plot(1883, 1346.5, "s",label="Closest to Half Max", color="Gray")
	ax4.legend(['Values from 1850 to 1886', 'Dark Edges (1851, 1885)' + "\n" + "(33 rows between them)", "Closest to Half Max (1852, 1883)" + "\n" + "(30 rows between them)", "Approximate half max for filter"])






	file.write("This is for the left side: " + str(left_profile) + "\n")
	file.write("This is for the right side: " + str(right_profile) + "\n")
	file.write("This is for the center: " + str(center_profile) + "\n")


	plt.show()
	




















if __name__ == '__main__':

	# Define data directory
    basedir = '/Users/santapl1/Desktop/MaxTest/'
    rawdir = basedir + 'FlatFieldColorMax.fit'



    stripe_read(rawdir)



    sys.exit(0)