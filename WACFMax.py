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
    print(n)


    fits_stack = np.zeros((2048, 4096 , n)) 

    for ii in range(0, n):
        img_hdu = fits.open(filelist[ii], do_not_scale_image_data=True)
        imgdat = img_hdu[0].data
        # print(np.amax(imgdat))
        fits_stack[:,:,ii] = imgdat

        print(np.amax(fits_stack))

    

    max_frame = np.amax(fits_stack, axis=2)


    return max_frame


if __name__ == '__main__':


    datadir = '/disks/deu01a/data/prelaunch/WAC_FM/20220509_calibration/20220524_174122_FLAT_FIELD_PAN_LOW_GAIN/analysis/Dark/'


	
    image_list = glob.glob(datadir + '*r.fit')

    # image_list = image_list[:50]

    max_stack = mediancombine(image_list)

    # print(max_stack)

    hdu = fits.PrimaryHDU(max_stack, do_not_scale_image_data=True)

    hdu.writeto('/homes/eissoccal/eis-cal-analysis/peter/Flat_Field_Pan_Low_Gain_Second_Run_Max.fit', overwrite=True)


    sys.exit(0)



	


