# This code was written to apply picture frame
# and dark corrections to WAC EM images within any file
# structure.
# 3/17/2020
# Updated 5/20/2020 due to WAC EM mask offset

# Python Imports
from astropy.io import fits
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import os
import sys
import glob
from tqdm import tqdm

eiscal_dir = os.getcwd() + '/'

sys.path.append(eiscal_dir + 'utils/')
from pf_corr import pf_corr  # noqa
from preproc import preproc # noqa


def master_corr_old(rawdir):
    
    # Get all test case names
    for root, dirs, files in os.walk(rawdir):
        for test_case in dirs:

            # if "cold_infield_stray" in test_case:
            #     case1(root + test_case + "/")
            #     print("Done with test case: cold_infield_stray")
            #     print("\n")

            if "ambient_out_of_field_stray" in test_case:
                case2(root + test_case + "/")
                print("Done with test case: ambient_out_of_field_stray")
                print("\n")

            # if "cold_out_of_field_stray" in test_case:
            #     case3(root + test_case + "/")
            #     print("Done with test case: cold_out_of_field_stray")
            #     print("\n")

            # if "manual" in test_case:
            #    case4(root + test_case + "/")
            #    print("Done with test case: manual")
            #    print("\n")

            # if "stray_filter_one_column" in test_case:
            #     case3(root + test_case + "/")

        break

    return None


def plot_diagnostic(arr):

    # This function assumes that you've pf and dark corrected
    # the raw images. It will fail if the corrected files don't exist.

    # check that the supplied array has the correct dimensions
    assert arr.shape[0] == 2048
    assert arr.shape[1] == 4096

    # Now create the figure
    fig = plt.figure()

    gs = GridSpec(6, 12, left=0.05, right=0.95, wspace=2.5, hspace=2.5)
    ax1 = fig.add_subplot(gs[:, :6])
    ax2 = fig.add_subplot(gs[:3, 6:])
    ax3 = fig.add_subplot(gs[3:, 6:])

    max_idx_1d = np.argmax(arr)
    max_idx_2d = np.unravel_index(max_idx_1d, arr.shape)
    print(np.max(arr))
    print(max_idx_2d)

    # Only show the region around the source and 
    # stray NOT the entire detector field of view.
    padding = 75
    ax1.imshow(arr[max_idx_2d[0]-padding:max_idx_2d[0]+padding,
               max_idx_2d[1]-padding:max_idx_2d[1]+padding],
               cmap=plt.get_cmap('viridis'), vmin=0, vmax=3500,
               origin='lower')

    # Characterize the source
    # First get an average noise level
    noise_lvl = get_avg_noise_level(arr, max_idx_2d)
    print("Noise level is:", "{:.3e}".format(noise_lvl))

    # Now plot traces along the source
    x_trace = arr[max_idx_2d[0], max_idx_2d[1]-padding:max_idx_2d[1]+padding]
    y_trace = arr[max_idx_2d[0]-padding:max_idx_2d[0]+padding, max_idx_2d[1]]

    # Get the 10% cutoff limits
    # print(np.where(x_trace < 0.1*np.max(x_trace)))
    # print(np.max(x_trace), np.argmax(x_trace))
    # print(np.array_repr(x_trace, precision=2))
    # sys.exit(0)

    ax2.plot(np.arange(2*padding), x_trace, color='k')
    ax2.axhline(y=noise_lvl, color='dodgerblue') 

    ax3.plot(np.arange(2*padding), y_trace, color='k')
    ax3.axhline(y=noise_lvl, color='dodgerblue')

    plt.show()

    return None


def get_avg_noise_level(arr, source_loc):

    # Basically just taking the average of all pixels
    # in a 200x200 square 300 pixels away from the source.
    # Depending on where the source is you will have 
    # to decide where to put this box for averaging.

    pix_to_move = 500

    if (source_loc[0] > pix_to_move) and (source_loc[1] > pix_to_move):
        x_cen = source_loc[0] - pix_to_move
        y_cen = source_loc[1] - pix_to_move

    elif (source_loc[0] < pix_to_move) and (source_loc[1] > pix_to_move):
        x_cen = source_loc[0] + pix_to_move
        y_cen = source_loc[1] - pix_to_move

    elif (source_loc[0] > pix_to_move) and (source_loc[1] < pix_to_move):
        x_cen = source_loc[0] - pix_to_move
        y_cen = source_loc[1] + pix_to_move

    elif (source_loc[0] < pix_to_move) and (source_loc[1] < pix_to_move):
        x_cen = source_loc[0] + pix_to_move
        y_cen = source_loc[1] + pix_to_move

    box_width = 200
    noise_lvl = np.mean(arr[x_cen-box_width:x_cen+box_width,
                            y_cen-box_width:y_cen+box_width])

    return noise_lvl


def case1(casedir):
    """
    This is the cold infield stray case which
    involves interspersed darks.
    Look for files with the name *b.fit

    The first image in a stack of 6 files will 
    be a dark, i.e., a dark file precedes the 
    next 5 raw images associated with the dark.
    """

    print("Working on cold infield stray case.")

    for root, dirs, files in os.walk(casedir):
        """
        Loop over all files in this case directory.
        We know what the file structure is, and we 
        can now proceed with the processing.
        """
        for fl in files:
            if "b.fit" in fl:
                """
                This means a dark has been found.
                The next five images in the sequence 
                are raw images corresponding to this dark.
                """
                print("\n" + "Dark filename:", fl)

                if "." == fl[0]:
                    print("Skipping hidden file.")
                    continue

                # Apply picture frame correction to dark
                darkimg, darkhdr = fits_pipe(root + fl, remove_fg=True)
                dark_pfcorr = pf_corr(darkimg)

                dark_pfcorr = dark_pfcorr.astype(np.float32)

                # Save PF corrected dark image to new fits file
                dark_pfcorr_hdu = fits.PrimaryHDU(data=dark_pfcorr,
                                                  header=darkhdr)
                new_dark_filename = fl.replace("b.fit", "b_pf_corr.fit")
                dark_pfcorr_hdu.writeto(root + new_dark_filename,
                                        overwrite=True)

                # Now identify each image associated with this dark
                dark_num = fl.split('_')[-1]
                dark_num = dark_num.split('b.fit')[0]

                for i in range(5):

                    raw_num = int(dark_num) + i + 1
                    raw_num = str(raw_num)
                    
                    # Make sure raw num is a str with a length of 4
                    if len(raw_num) == 1:
                        raw_num = '000' + raw_num
                    elif len(raw_num) == 2:
                        raw_num = '00' + raw_num
                    elif len(raw_num) == 3:
                        raw_num = '0' + raw_num
                    elif len(raw_num) == 5:
                        raw_num = raw_num[1:]

                    assert len(raw_num) == 4

                    current_raw_filename = fl.replace(dark_num + "b.fit",
                                                      raw_num + "i.fit")
                    print("Working on:", current_raw_filename)
                            
                    # Apply picture frame correction and 
                    # dark correction to this stack
                    imgdat, imghdr = fits_pipe(root + current_raw_filename,
                                               remove_fg=True)
                    pf_corr_img = pf_corr(imgdat)
                    finaldata = dark_corr(pf_corr_img, dark_pfcorr)

                    finaldata = finaldata.astype(np.float32)

                    # Save dark corrected image to new fits file
                    pfcorr_hdu = fits.PrimaryHDU(data=finaldata, header=imghdr)
                    new_fits_filename = \
                        current_raw_filename.replace(".fit", "_drk_corr.fit")
                    pfcorr_hdu.writeto(root + new_fits_filename,
                                       overwrite=True)
                    print("Written PF and Dark corrected file:",
                          root + new_fits_filename)

    return None


def case2(casedir):
    """
    This is the case where the darks are stored in a different 
    folder. The case dir that is given is the directory for the
    raw images.
    """

    print("Working on ambient out of field stray case.")
    print("Case directory:", casedir)

    # if "line" in casedir:
    #     darkdir = casedir.replace("ambient_out_of_field_stray_line", "ambient_dark_out_of_field_stray_line")
    #     darkdir = darkdir.replace("145912", "142528")  # timestamp
    # elif "grid" in casedir:
    #     darkdir = casedir.replace("ambient_out_of_field_stray_grid", "ambient_dark_out_of_field_stray_grid")
    #     darkdir = darkdir.replace("1320", "124216")  # timestamp
    #     darkdir = darkdir.replace("1579815916", "1579815374")  # some other number??

    # print("Darks in a separate directory:", darkdir)

    darkdir = casedir + "Dark"
    print(darkdir)

    for root, dirs, files in os.walk(casedir):

        for current_raw_filename in files:

            if "." == current_raw_filename[0]:  # there are some hidden files in this folder, which we're skipping
                continue
            else:
                if "i.fit" in current_raw_filename:

                    dark_filename = current_raw_filename.replace("i.fit", "b.fit")

                    # Switch timestamps
                    if "line" in casedir:
                        dark_filename = dark_filename.replace("145912", "142528")
                    elif "grid" in casedir:
                        dark_filename = dark_filename.replace("132229", "124216")

                    print("\n" + "Dark filename:", dark_filename)

                    # First apply picture frame correction to dark
                    darkimg, darkhdr = fits_pipe(darkdir + dark_filename, remove_fg=True)
                    #dark_pfcorr = pf_corr(darkimg)

                    # Force it to be a 32 bit floating point datatype
                    # so it uses less space. Raw data is int16.
                    #dark_pfcorr = dark_pfcorr.astype(np.float32)

                    # Save PF corrected dark image to new fits file
                    #dark_pfcorr_hdu = fits.PrimaryHDU(data=dark_pfcorr, header=darkhdr)
                    #new_dark_filename = dark_filename.replace("b.fit", "b_pf_corr.fit")
                    #dark_pfcorr_hdu.writeto(darkdir + new_dark_filename, overwrite=True)

                    # Now start working on the raw image processing
                    print("Working on:", current_raw_filename)
                
                    # Apply picture frame correction and 
                    # dark correction to this stack
                    imgdat, imghdr = fits_pipe(root + current_raw_filename, remove_fg=True)
                    #pf_corr_img = pf_corr(imgdat)
                    #finaldata = dark_corr(pf_corr_img, dark_pfcorr)
                    finaldata = dark_corr_nopf(imgdat, darkimg)

                    # Force it to be a 32 bit floating point datatype
                    # so it uses less space. Raw data is int16.
                    finaldata = finaldata.astype(np.float32)

                    # Save dark corrected image to new fits file
                    #pfcorr_hdu = fits.PrimaryHDU(data=finaldata, header=imghdr)
                    nopfcorr_hdu = fits.PrimaryHDU(data=finaldata, header=imghdr)
                    #new_fits_filename = current_raw_filename.replace(".fit", "_drk_corr.fit")
                    new_fits_filename = current_raw_filename.replace(".fit", "_nopf_drk_corr.fit")
                    savedir = root + 'nopf_corr/'
                    nopfcorr_hdu.writeto(savedir + new_fits_filename, overwrite=True)
                    print("Written PF and Dark corrected file:", root + new_fits_filename)

    return None


def case3(casedir):
    """
    This is the case where there are no darks and the images are individual FITS
    files.

    Applies to the following tests:
    1. Cold out of field stray grid 
    2. Cold out of field stray line
    """

    print("Working on cold out of field stray case.")
    print("Case directory:", casedir)

    for root, dirs, files in os.walk(casedir):

        for current_raw_filename in files:

            if ("." == current_raw_filename[0]) or ('0056i.fit' in current_raw_filename):
                # there are some hidden files in this folder, which we're skipping
                # We're also skipping *0056i.fit for now. This seems to be an anomalous
                # image with shape (2, 2048, 4102)
                continue
            else:
                if "i.fit" in current_raw_filename:
                    # Now start working on the raw image processing
                    print("\n" + "Working on:", current_raw_filename)

                    # Apply picture frame correction 
                    # NO dark correction is required
                    imgdat, imghdr = fits_pipe(root + current_raw_filename, remove_fg=True)
                    pf_corr_img = pf_corr(imgdat)

                    # Force it to be a 32 bit floating point datatype
                    # so it uses less space. Raw data is int16.
                    pf_corr_img = pf_corr_img.astype(np.float32)

                    # Save PF corrected image to new fits file
                    pfcorr_hdu = fits.PrimaryHDU(data=pf_corr_img, header=imghdr)
                    new_fits_filename = current_raw_filename.replace(".fit", "_pf_corr.fit")
                    pfcorr_hdu.writeto(root + new_fits_filename, overwrite=True)
                    print("Written PF corrected file:", root + new_fits_filename)

    return None


def case4(casedir):
    """
    This is the case where the fits files are stacks of images.
    The shape of the array is (100, 2048, 4102)
    """

    print("Working on manual straylight field scans case.")
    print("Case directory:", casedir)

    for root, dirs, files in os.walk(casedir):

        for current_raw_filename in files:

            if ("." == current_raw_filename[0]):
                # there are some hidden files in this folder, which we're skipping
                continue
            else:
                if "i.fit" in current_raw_filename:
                    # Now start working on the raw image processing
                    print("\n" + "Working on:", current_raw_filename)
                    
                    hdu = fits.open(root + current_raw_filename)
                    imgdat = hdu[0].data
                    imghdr = hdu[0].header

                    # Make sure that it is a stack of 100 images
                    assert imgdat.shape[0] == 100

                    # Create an empty array to save the PF corrected stack
                    pf_corr_img = np.zeros((100, 2048, 4096), dtype=np.float32)
                    # this new array will NOT have the framegrabber columns

                    for i in range(imgdat.shape[0]):
                        current_img = imgdat[i]

                        # Remove framegrabber columns first
                        current_img = current_img[:, 6:]

                        # Apply picture frame correction 
                        # NO dark correction is required
                        pf_corr_img[i] = pf_corr(current_img)

                    # Save PF corrected image to new fits file
                    pfcorr_hdu = fits.PrimaryHDU(data=pf_corr_img, header=imghdr)
                    new_fits_filename = current_raw_filename.replace(".fit", "_pf_corr.fit")
                    pfcorr_hdu.writeto(root + new_fits_filename, overwrite=True)
                    print("Written PF corrected file:", root + new_fits_filename)

    return None


def dark_corr(pf_corr_img, dark):

    finaldata = pf_corr_img - dark

    return finaldata


def dark_corr_nopf(imgdat, darkimg):

    finaldata = imgdat - darkimg

    return finaldata


def fits_pipe(current_raw_filename, remove_fg=True):

    img_hdu = fits.open(current_raw_filename)
    imgdat = img_hdu[0].data
    hdr = img_hdu[0].header

    if imgdat.shape[0] == 1:  # i.e., if the array is "fake" 3D
        imgdat = imgdat[0]

    # By default the framegrabber columns will
    # be removed
    if remove_fg:
        # Remove framegrabber columns
        imgdat = imgdat[:, 6:]

    return imgdat, hdr


def get_darkbasename(flbase, darknum):

    # Get the serial num at the end of 
    # the file name and get serial num for dark
    flnum = int(flbase.split('i.fit')[0].split('_')[-1])
    darknum = flnum + darknum

    # construct the dark file name in 
    # two parts 
    basearr = flbase.split('_')[:-1]
    darkbase_pt1 = '_'.join(basearr)

    darknum_str = str(darknum)
    if len(darknum_str) == 1:
        leadzeros = '000'
    elif len(darknum_str) == 2:
        leadzeros = '00'
    elif len(darknum_str) == 3:
        leadzeros = '0'
    elif len(darknum_str) == 4:
        leadzeros = ''

    darkbase_pt2 = leadzeros + str(darknum) + 'b.fit'

    darkbase = darkbase_pt1 + '_' + darkbase_pt2

    return darkbase


def master_corr(datadir, outdir, flags, darksdir):




    file_list = glob.glob(datadir + '*i.fit')

    



    for fl in tqdm(file_list, desc='Processing', leave=False):



        flbase = os.path.basename(fl)        
        newflname = outdir + flbase.replace('i.fit', '_corr.fit')

        if not flags['reprocess']:
            if os.path.isfile(newflname):
                tqdm.write('\n' + newflname +
                           '  Corrected file exists. Moving to next.')
                continue


        # Preprocess image file
        img, hdr = fits.getdata(fl, header=True)
        img = preproc(img)

        if flags['pf_correct'] and flags['dark_correct']:


            # PF correct image
            pf_img = pf_corr(img, flags['instrument'])

            #Darks other folder case
            if flags['darks_other_folder']:
                dark_list = glob.glob(darksdir + '*.fit')
                dark_num = fl.split('_')[-1] 
                dark_num = dark_num.replace('i.fit', 'b.fit')

                print(dark_num)
                print(dark_list)


                for i in dark_list:
                    if dark_num in i:
                        dark_fl = i
                        break


                print(dark_fl)



            # Get dark file name
            else: 
                dark_fl = get_darkbasename(flbase, flags['dark_num'])
                dark_fl = datadir + dark_fl



            

            # Now pre-process dark
            dimg = fits.getdata(dark_fl)
            dimg = preproc(dimg)

            # PF correct dark
            pf_dimg = pf_corr(dimg, flags['instrument'])

            # Dark correct img
            img = dark_corr(pf_img, pf_dimg)

            # Update header
            hdr['PFCORR'] = 'True'
            hdr['DARKCORR'] = 'True'

        elif (not flags['pf_correct']) and flags['dark_correct']:

            # Get dark file name
            dark_fl = get_darkbasename(flbase, flags['dark_num'])
            dark_fl = datadir + dark_fl

            # Now pre-process dark
            dimg = fits.getdata(dark_fl)
            dimg = preproc(dimg)

            # Dark correct img
            img = dark_corr_nopf(img, dimg)

            # Update header
            hdr['PFCORR'] = 'False'
            hdr['DARKCORR'] = 'True'

        elif flags['pf_correct'] and (not flags['dark_correct']):

            # PF correct image
            img = pf_corr(img, flags['instrument'])

            # Update header
            hdr['PFCORR'] = 'True'
            hdr['DARKCORR'] = 'False'








        # Write processed file
        hdr['INSTRU'] = flags['instrument']
        nhdu = fits.PrimaryHDU(data=img, header=hdr)
        nhdu.writeto(newflname, overwrite=True)

        tqdm.write('\nWritten:' + newflname)

    return None


if __name__ == '__main__':

    # Define data directory
    basedir = '/Volumes/EIS_Cal/Lab_Data/WAC_FM/Final_Cal/OFS/'
    rawdir = basedir + '20220526_213330_OFS_SPHERE_1000X/'
    darksdir = '20220526_233813_OFS_SPHERE_1000X_BKG/'
    darkrawdir = basedir + darksdir

    # Define output directory
    outdir = rawdir + 'analysis/'

    if not os.path.isdir(outdir):
        os.mkdir(outdir)

    # Flags
    flags = {'pf_correct': True,
             'dark_correct': True,
             'instrument': 'WAC_FM',
             'reprocess': True,
             'dark_num': +1,
             'darks_other_folder': True}


    if 'darks_other_folder' == False:
        darkrawdir = rawdir



    master_corr(rawdir, outdir, flags, darkrawdir)


    sys.exit(0)
# END OF FILE
