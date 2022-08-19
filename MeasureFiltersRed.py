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

	file = open("Red.txt", "w")

	head, tail = os.path.split(fl)

	fitsFile = fits.open(fl)

	img = fitsFile[0].data

	right_start = (1786, 4013)

	right_end = (1822, 4013)

	left_start = (1786, 85)

	left_end = (1822, 85)

	center_start = (1786, 2110)

	center_end = (1822, 2110)

	right_profile = skimage.measure.profile_line(img, right_start, right_end, linewidth=1)

	left_profile = skimage.measure.profile_line(img, left_start, left_end, linewidth=1)

	center_profile = skimage.measure.profile_line(img, center_start, center_end, linewidth=1)

	left_x_array = np.arange(1786, 1822  + 1)

	right_x_array = np.arange(1786, 1822  + 1)

	center_x_array = np.arange(1786, 1822 + 1)






	ax1 = plt.subplot(2, 2, 4)
	ax1.imshow(img, cmap='gray')
	ax1.plot([left_start[1], left_end[1]], [left_start[0], left_end[0]], 'r', linewidth=(2))
	ax1.plot([right_start[1], right_end[1]], [right_start[0], right_end[0]], 'r', linewidth=(2))
	ax1.plot([center_start[1], center_end[1]], [center_start[0], center_end[0]], 'r', linewidth=(2))
	ax1.invert_yaxis()


	ax2 = plt.subplot(2, 2, 1)
	ax2.plot(left_x_array, left_profile, "-o")
	ax2.set_title('RED across 86(x)')
	ax2.plot(1787, 353, "o", label="Dark", color="black")
	ax2.plot(1788, 906, "s",label="Closest to Half Max", color="Gray")
	ax2.axhline(y= np.amax(left_profile) // 2, color='r', linestyle='--')
	ax2.plot(1821, 243, "o", label="Dark", color="black")
	ax2.plot(1819, 1297.5, "s",label="Closest to Half Max", color="Gray")
	ax2.legend(['Values from 1786 to 1822', 'Dark Edges (1787, 1821)' + "\n" + "(33 rows between them)", "Closest to Half Max (1788, 1819)" + "\n" + "(30 rows between them)", "Approximate half max for filter"])



	ax3 = plt.subplot(2, 2, 2)
	ax3.plot(right_x_array, right_profile, "-o")
	ax3.set_title('RED across 4014  (x)')
	ax3.plot(1787, 240, "o", label="Dark", color="black")
	ax3.plot(1788, 746, "s",label="Closest to Half Max", color="Gray")
	ax3.axhline(y= np.amax(right_profile) // 2, color='r', linestyle='--')
	ax3.plot(1821, 211, "o", label="Dark", color="black")
	ax3.plot(1820, 626, "s",label="Closest to Half Max", color="Gray")
	ax3.legend(['Values from 1786 to 1822', 'Dark Edges (1787, 1821)' + "\n" + "(33 rows between them)", "Closest to Half Max (1788, 1820)" + "\n" + "(31 rows between them)", "Approximate half max for filter"])
	

	ax4 = plt.subplot(2, 2, 3)
	ax4.plot(center_x_array, center_profile, "-o")
	ax4.set_title('RED across 2111  (x)')
	ax4.plot(1787, 364, "o", label="Dark", color="black")
	ax4.plot(1788, 1123, "s",label="Closest to Half Max", color="Gray")
	ax4.axhline(y= np.amax(center_profile) // 2, color='r', linestyle='--')
	ax4.plot(1821, 282.5, "o", label="Dark", color="black")
	ax4.plot(1819, 1491.5, "s",label="Closest to Half Max", color="Gray")
	ax4.legend(['Values from 1786 to 1822', 'Dark Edges (1787, 1821)' + "\n" + "(33 rows between them)", "Closest to Half Max (1788, 1819)" + "\n" + "(30 rows between them)", "Approximate half max for filter"])






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