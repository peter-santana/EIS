# Function for EIS WAC EM picture frame correction 
# To be called prior to dark correction for 
# both dark images and illuminated images

# Last updated: Dec 11, 2021
# Verified update that included Frank's faster row processing 
# without shape manipulation. Deleted older pf_corr
# version that was slower due to shape manipulation.
# Updated to include FM instruments.

import numpy as np
    

def do_row_corr(imgdat, all_rows):

    rt1 = all_rows[0]
    rt2 = all_rows[1]
    rb1 = all_rows[2]
    rb2 = all_rows[3]

    bottom_rows = imgdat[rb1:rb2, :]
    top_rows = imgdat[rt1:rt2, :]

    median_bottom = np.median(bottom_rows, axis=0)
    median_top = np.median(top_rows, axis=0)
    median_row_tosub = 0.5*(median_bottom + median_top)
    row_pf_corr = imgdat - median_row_tosub
    
    return row_pf_corr


def do_col_corr(imgdat, all_cols):

    cl1 = all_cols[0]
    cl2 = all_cols[1]
    cr1 = all_cols[2]
    cr2 = all_cols[3]

    left_cols = imgdat[:, cl1:cl2]
    right_cols = imgdat[:, cr1:cr2]

    median_left = np.median(left_cols, axis=1)
    median_right = np.median(right_cols, axis=1)
    median_col_tosub = 0.5*(median_left + median_right)
    
    col_pf_corr = imgdat - median_col_tosub.reshape((2048, 1))

    return col_pf_corr


def pf_corr(imgdat, instrument):
    '''
    Apply picture frame correction to EIS WAC and NAC EM images.
    To be called prior to dark correction for both
    dark images and illuminated images.
    :param imgdat:
    :param instrument:
    :return:
    '''

    # ---------------------------------
    # For testing or running outside a script, 
    # uncomment this block to read in fits image
    # img_hdu = fits.open(image)
    # imgdat = img_hdu[0].data[0]
    # #print("Image size:",imgdat.shape)
    # hdr = img_hdu[0].header
    # imgdat = imgdat[:,6:]
    # ---------------------------------

    # Make sure that the shape is correct 
    # using assertion statements
    assert imgdat.shape[0] == 2048
    assert imgdat.shape[1] == 4096
    
    # Get indices to sum over for rows
    # This is instrument dependent
    # 1 and 2 are starting and ending indices,
    # respectively.
    if instrument == 'WAC_FM':
        # ROWS; top and bottom
        rt1 = 4
        rt2 = 15
        rb1 = 2030
        rb2 = 2039
        # COLS; left and right
        cl1 = 4
        cl2 = 20
        cr1 = 4082
        cr2 = 4089

    elif instrument == 'WAC_EM':
        # ROWS; top and bottom
        rt1 = 4
        rt2 = 14
        rb1 = 2018
        rb2 = 2038
        # COLS; left and right
        cl1 = 4
        cl2 = 19
        cr1 = 4076
        cr2 = 4091

    elif instrument == 'NAC_EM':
        # ROWS; top and bottom
        rt1 = 16
        rt2 = 36
        rb1 = 2040
        rb2 = 2043
        # COLS; left and right
        cl1 = 4
        cl2 = 24
        cr1 = 4071
        cr2 = 4091

    all_indices = [[rt1, rt2, rb1, rb2],
                   [cl1, cl2, cr1, cr2]]

    # Now do the corrections
    rowcorr = do_row_corr(imgdat, all_indices[0])
    finalcorr = do_col_corr(rowcorr, all_indices[1])

    return finalcorr
