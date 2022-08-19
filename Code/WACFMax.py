#What is the exact positioning of the mask on the WAC FM detector?

#TD: CHANGE TO MAX

import numpy as np
from astropy.io import fits
from astropy.utils.data import download_file
import os
import sys
import glob



import numpy as np
    



def mediancombine(filelist):
  
    n = len(filelist)
    

    #Input size of fits, make sure that all fits to be stacked are of the same dimensions
    fits_stack = np.zeros((2048, 4096 , n)) 

    for ii in range(0, n):
        img_hdu = fits.open(filelist[ii], do_not_scale_image_data=True)
        imgdat = img_hdu[0].data
        # print(np.amax(imgdat))
        fits_stack[:,:,ii] = imgdat



    

    max_frame = np.amax(fits_stack, axis=2)


    return max_frame


if __name__ == '__main__':


    datadir = '/disks/deu01a/data/prelaunch/WAC_FM/20220509_calibration/20220524_225220_FLAT_FIELD_COLOR/analysis/Dark/'

	
    image_list = glob.glob(datadir + '*r.fit')


    max_stack = mediancombine(image_list)


    hdu = fits.PrimaryHDU(max_stack, do_not_scale_image_data=True)

    hdu.writeto('/homes/eissoccal/eis-cal-analysis/peter/FlatFieldColorMaxNUV.fit', overwrite=True)


    sys.exit(0)



	


