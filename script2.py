import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import wcs
from astropy.io import ascii
from astropy.table import Table, Column, MaskedColumn
from pathlib import Path

# Import coordinates from selected objects
standards = ascii.read("standards.txt", guess=False)
coord_world = np.array([standards['RA'],standards['Dec']]).transpose()
nr_stars = len(coord_world[:,0])
print('Number of stars = {}'.format(nr_stars))


def find_stars(xobj_list, yobj_list, xlist, ylist, f):
    # Make a matrix with each column the same xlist or ylist.
    # The number of columns is the number of objects in standards.txt
    xmatrix = np.array(list(xlist)*len(xobj_list)).reshape([len(xobj_list),len(xlist)]).transpose()
    ymatrix = np.array(list(ylist)*len(yobj_list)).reshape([len(yobj_list),len(ylist)]).transpose()
    
    distance_matrix = np.sqrt((xmatrix-xobj_list)**2 + (ymatrix-yobj_list)**2)
    
    indices = np.argmin(distance_matrix, axis=0)
    """
    # Make plot to check data
    plt.figure(figsize=(16,16))
    plt.scatter(xlist,ylist,c='b',)
    plt.scatter(xobj_list, yobj_list, c='red',marker='.')
    for i in range(nr_stars):
    	plt.plot([xobj_list[i],xlist[indices[i]]],[yobj_list[i],ylist[indices[i]]], linestyle='dashed',c='r')
    plt.title(f)
    plt.show()
    """
    return indices, np.diag(distance_matrix[indices])
    #the diagonal gives the distance from each selected object to the closest object

# Make one file with the image_name, epoch, filter and airmass
meta_data = [] #where each row is the meta-data from one file

#selects all names in ../data/
for filename in Path('..//data/').rglob('*e91.fits.fz'):
	filename = str(filename)
	print (filename)
	# Open the file & extract certain data
	hdu1 = fits.open(filename)
	imh = hdu1['SCI'].header
	phot = hdu1['cat'].data

	epoch = imh['MJD-OBS']
	obs_filter = imh['FILTER']
	airmass = imh['AIRMASS']
	obj = filename.replace('../data/','')
	meta_data.append([obj, epoch, obs_filter,airmass])
	
	# Transform the world coordinates for the selected stars into pixel coordinates
	w = wcs.WCS(hdu1['SCI'].header)
	coord = w.wcs_world2pix(coord_world,0)
	
	# Use the find_stars function to get the closest-star-indices for the selected stars
	stars_arg, d = find_stars(coord[:,0],coord[:,1], phot['x'], phot['y'], filename)
	print (d)
	
	# Use the indices to get the flux & fluxerr for all selected stars
	flux_stars = phot['flux'][stars_arg]
	fluxerr_stars = phot['fluxerr'][stars_arg]
	#if the distance is more than 25 pixels (~9.7"), it's too far away so it will write out NaN
	select_mask = d > 25
	flux_stars[d] = np.NaN
	fluxerr_stars[d] = np.NaN
	
	
	# Make a new file path to write to
	newfilename = 
	
	#VERY cheap fix for "ValueError: Inconsistent data column lengths: {1, 44}", must be a better way
	# maybe use 2 different files, maybe
	nanlist = [np.NaN]*(nr_stars-1)

	obj = [filename.replace('../data/','').replace('.fits.fz','')]
	obj.extend(nanlist)
	epoch = [imh['MJD-OBS']]
	epoch.extend(nanlist)
	obs_filter = [imh['FILTER']]
	obs_filter.extend(nanlist)
	airmass = [imh['AIRMASS']]
	airmass.extend(nanlist)


	# Write data to Table and then to file
	filecontent = Table([obj, epoch, obs_filter, airmass, flux_stars, fluxerr_stars], \
				names=['IMAGE','EPOCH','FILTER','AIRMASS','FLUX','FLUXERR'])
	ascii.write(filecontent, newfilename, overwrite=True)

# Write out the meta_data elements to a file
filecontent = Table([meta_data[0,:],meta_data[1,:],meta_data[2,:],meta_data[3,:]], \
				names=['IMAGE','EPOCH','FILTER','AIRMASS'])
filepath = "..//datared/J0600_meta-data.txt"
ascii.write(filecontent, filepath, overwrite=True)


