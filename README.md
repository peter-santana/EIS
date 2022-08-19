# EIS
Code Repo for Calibration of Europas Imaging System WAC Instrument work
Data to run analysis is located in the EIS Cloud


CODE: MeasureFilters.py was used to create the plots for the filters where the 3 columns were read
      WACFMax.py is used to stack images and create a max fits file of them all
      TrueProfileScanner was used for row dimming scans, here it takes 5 plots of different columns      accross the image to read the avg magnitude of the row dimming artifact
      FocalPlaneMap.py was used to read in the FocalPlaneMap.py
      SingleProfileScanner.py simply reads out 1 image instead of doing a whole directory
      
      
PROFILE: Row dimming data, including text files for values

FITS: Fits for Focal Plane Map and colored filters

Edges: FWHM data for edges frames, including values

Datanalysis: Original code to fix images
