import numpy as np
from astropy.io import fits
from astropy import wcs
from astropy.io import ascii
from astropy.table import Table, Column, MaskedColumn

# Opening the datafile and extracting the relevant header
hdu1 = fits.open('..//data/coj1m003-fa19-20210112-0083-e91.fits.fz')

imh = hdu1['SCI'].header
phot = hdu1['cat'].data
#epoch = imh['MJD-OBS']
#airmass = imh['AIRMASS'] 
pix_asec = imh['PIXSCALE'] # Nominal pixel scale on sky [arcsec/pixel]

def find_min(xobj,yobj, xlist, ylist):
    'find the index of the star closest to position xobj, yobj'
    dr = (xlist-xobj)**2 + (ylist-yobj)**2
    # find min dr 
    ind = np.argmin(dr)
    print(np.sqrt(dr[ind]))
    return ind

def distance(xobj,yobj, xlist,ylist):
    'find the distance between target & objects round it, returns list with distances in pixels'
    d = (xobj-xlist)**2 + (yobj-ylist)**2
    return np.sqrt(d)

# read in the World Coordinate System (WCS) from the FITS file
# Parse the WCS keywords in the primary HDU
w = wcs.WCS(hdu1['SCI'].header)

# star coords in pix -  RA and Dec in decimal degrees
target_crd = w.wcs_world2pix([[90.0033, -31.0076]], 0)[0] #wcs_wordl2pix returns 2d array so [0] to make it 1d
# Coords of J0600: RA 90.0033 (06:00:00.792) Dec -31.0076 (-31:00:27.36)


#calculate the distance of all stars to coordinates of J0600
dis = distance(target_crd[0], target_crd[1], phot['x'], phot['y'])
dis_asec = dis * pix_asec # convert distances in pixels to distances in arcseconds

# Select stars upto certain radial distance from J0600
radial_dis = 200 #arcsec
mask = dis_asec < radial_dis
print ("Nr of stars slected:",np.sum(mask))


# transforming the selected stars from the pixel coordinates to the RA & Dec coordinates
select_coords_pix = np.zeros((np.sum(mask),2))
select_coords_pix[:,0] = phot['x'][mask]
select_coords_pix[:,1] = phot['y'][mask]

select_coords = w.wcs_pix2world(select_coords_pix,0)

# Sort this list according to the radial distance to target (0'th element is target (-1)'th element is furthest star)
sort_i = np.argsort(dis_asec[mask])
select_coords_sort = select_coords[sort_i]

# Write out the coordinates of the selected stars to a file
filecontent = Table([select_coords_sort[:,0],select_coords_sort[:,1]], names=['RA','Dec'])
ascii.write(filecontent, 'standards.txt', overwrite=True)
