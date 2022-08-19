from matplotlib import pyplot as plt
import skimage
from astropy.io import fits
import numpy as np
from matplotlib import colors
import sys
import os
import glob
from tqdm import tqdm


def single_pic_profile_analysis(column, fl):

	starting_column = column

	Readout_ports = np.arange(0, 4097, 256)

	head, tail = os.path.split(fl)

	file = open("wffftgt_20220520_030913_0006i.fit_magnitudes.txt", "w")

	fitsFile = fits.open(fl)
	img = fitsFile[0].data

	offset = fitsFile[0].header['OFFSET']
	rowtmprm = fitsFile[0].header['ROWTMPRM']
	exposure_time = fitsFile[0].header['EXPTM_MS'] #in miliseconds
	name = fitsFile[0].header['TESTNAME']

	increase = 5
	scan_count = 0

	column = starting_column

	magnitude = 0


	while scan_count < 5:

	
		start = (0, column)

		end = (img.shape[0] - 1, column)

		read_columns = np.arange(start[1] - 5, start[1] + 5, 1)
	

		if read_columns in Readout_ports:
			start[1] += 10
			end[1] += 10


		profile = skimage.measure.profile_line(img, start, end, linewidth=10)

		magnitude = np.max(profile)



		fig, ax = plt.subplots(1, 2, figsize=(12,4))
		ax[0].set_title('Image')
		ax[0].imshow(img, cmap="Greys_r", norm=colors.LogNorm())
		ax[0].plot([start[1], end[1]], [start[0], end[0]], 'r', linewidth=(10 * 72 / fig.dpi))
		ax[0].invert_yaxis()
		ax[1].set_title('Profile')
		ax[1].plot(profile)
		ax[1].invert_xaxis()
		fig.text(.15, .9, "Magnitude: " + str(magnitude))
		fig.text(.15, .86, "Exposure Time: " + str(exposure_time))
		fig.text(.15, .82, "Rowtmprm: " + str(rowtmprm))
		fig.text(.15, .94, name)



		plt.savefig("/Users/santapl1/Desktop/accross/" + tail + str(scan_count) + ".png")
	



		file.write(tail + str(scan_count) + "  magnitude is: " + str(magnitude) + "\n")

		scan_count += 1
		column += increase





if __name__ == '__main__':

	# Define data directory
    basedir = '/Users/santapl1/Desktop/20220518_194535_WAC_MTF_TARGET_3X3_WHITE_0.5X/analysis/dark+row_col/'
    rawdir = basedir + 'wffftgt_20220518_194651_0016_corr.fit'


    starting_column = 2150

    single_pic_profile_analysis(starting_column, rawdir)



    sys.exit(0)