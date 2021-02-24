import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import wcs
from astropy.io import ascii



def find_min(xobj,yobj, xlist, ylist):
    'find the index of the star closest to position xobj, yobj'
    dr = (xlist-xobj)**2 + (ylist-yobj)**2
    # find min dr 
    ind = np.argmin(dr)
    print(np.sqrt(dr[ind]))
    return ind


#for imname in Path('./').rglob('*e91.fits.fz'):

hdu1 = fits.open("cpt1m012-fa06-20210118-0059-e91.fits.fz")

# the image (if you want to see the picture...
imh = hdu1['SCI'].header

epoch = imh['MJD-OBS']
print('{:.5f} MJD'.format(epoch))
airmass = imh['AIRMASS']
print('AIRMASS = {:.5f}'.format(airmass))


phot = hdu1['CAT'].data
# calculate the flux of the star relative to the STD star

# read in the World Coordinate System (WCS) from the FITS file
# Parse the WCS keywords in the primary HDU
w = wcs.WCS(hdu1['SCI'].header)


# star coords in pix -  RA and Dec in decimal degrees
star_crd = w.wcs_world2pix([[90.0033, -31.0076]], 0) # star
# RA
        #90.0033 (06:00:00.792)
        #Dec
        #-31.0076 (-31:00:27.36)
        #Epoch
        #2000

# reference star UC4 296-009008
refe_crd = w.wcs_world2pix([[90.1409130, -30.9974700]], 0) # 296-009008
        #print(refe_crd)




star_arg = find_min(star_crd[0][0], star_crd[0][1], phot['x'], phot['y'])
        #print(star_arg)
refe_arg = find_min(refe_crd[0][0], refe_crd[0][1], phot['x'], phot['y'])
        #print(refe_arg)

        #column "flux" with row star_arg
targflux = phot['flux'][star_arg]
targfluxerr = phot['fluxerr'][star_arg]
print(phot)
refflux = phot['flux'][refe_arg]
reffluxerr = phot['fluxerr'][refe_arg]

print('star flux is {:.1f} +- {:.1f}'.format(targflux, targfluxerr))
print('refe flux is {:.1f} +- {:.1f}'.format(refflux, reffluxerr))

# convert flux to star magnitudes
dm = -2.5 * np.log10(targflux/refflux)

# convert errors on flux to errors on magnitudes
dmerr = np.sqrt( (targfluxerr/targflux)**2 + (reffluxerr/refflux)**2) * dm
print()
print('delta mag is {:.3f}+-{:.3f} mag'.format(dm, dmerr))

mag = dm + 13.054 # 13.054 is g' magnitude eyeballed from ASAS-SN

##t[-1]['Magnitude'] = mag
##t[-1]['Uncertainty'] = dmerr

# script 1 - find all the stars within radius r_max = 120 arcseconds (it's in decimal degrees in the table...)
# select all the stars within that radius and write to a file the RA and Dec of these stars
# call it standards.txt

# script 2 - takes in standards.txt and a list of FITS files
#
# write out for each image:
# loop throuhg the standards stars:
#     find the photometry from the current FITS image
#     IF star is not found (or bad data) write out NaN in the column
#
# write out for each image file:
#
# the name of the image file, the EPOCH, the FILTER, the AIRMASS, the FLUX and FLUXERR of J0600, (FLUX and FLUXERR for 20 stars)
# use and ECSV format (because it remembers the names of the columns and deals with 'Quantity' columns too....)


# make a plot of flux versus epoch (which is in MJD) for 

