from matplotlib import pyplot as plt
import skimage
from astropy.io import fits
import numpy as np
from matplotlib import colors
import sys
import os
import glob
from tqdm import tqdm


def edge_read(fl):

	file = open("Upper_left_filter_corner.txt", "w")

	head, tail = os.path.split(fl)

	fitsFile = fits.open(fl)

	img = fitsFile[0].data
	
	#change values here to mark where you want your column read line to start and end
	column_start = (2030, 50)

	column_end = (1980, 50)

	#change values here to mark where you want your row read line to start and end
	row_start = (2000, 0)

	row_end = (2000, 50)
	
	
	#linewidth here is how many lines you want to read at a time
	row_profile = skimage.measure.profile_line(img, row_start, row_end, linewidth=10)

	column_profile = skimage.measure.profile_line(img, column_start, column_end, linewidth=10)
	
	#row_x_Array and column_x_array is to mark the plot X values
	#It may be required to inverse the column array, same thing with rows
	row_x_array = np.arange(img.shape[1]-50, img.shape[1]+1)

	column_x_array = np.arange(1980, 2031)

	column_x_array = column_x_array[::-1]
	# print(column_x_array)
	# row_x_array = row_x_array[::-1]




	ax1 = plt.subplot(212)
	ax1.imshow(img, cmap='gray')
	ax1.plot([column_start[1], column_end[1]], [column_start[0], column_end[0]], 'r', linewidth=(2))
	ax1.plot([row_start[1], row_end[1]], [row_start[0], row_end[0]], 'r', linewidth=(2))
	ax1.invert_yaxis()

	ax2 = plt.subplot(221)
	ax2.plot(row_x_array, row_profile)
	ax2.set_title('Across Rows')
	# ax2.invert_xaxis()

	ax3 = plt.subplot(222)
	ax3.plot(column_x_array, column_profile)
	ax3.set_title('Across Columns')
	ax3.invert_xaxis()


	# max_y = np.max(row_profile)  # Find the maximum y value
	# xs = [x for x in range(50) if row_profile[x] > max_y/2.0]

	# print(xs)

	file.write("This is for the rows " + str(row_profile) + "\n")
	file.write("This is for the columns " + str(column_profile) + "\n")



	
	plt.savefig("/Users/santapl1/Desktop/Edges/UpperLeftFilterCorner" + ".png")


if __name__ == '__main__':

	# Define data directory
    basedir = '/Users/santapl1/Desktop/MaxTest/'
    rawdir = basedir + 'Flat_Field_Pan_Low_Gain_Second_Run_Max.fit'



    edge_read(rawdir)



    sys.exit(0)
