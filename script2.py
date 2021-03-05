import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy import wcs
from astropy.io import ascii
from astropy.table import Table, Column, MaskedColumn
from pathlib import Path
from math import trunc

# Import coordinates from selected objects
standards = ascii.read("standards.txt", guess=False)
coord_world = np.array([standards['RA'],standards['Dec']]).transpose()
nr_stars = len(coord_world[:,0])
#print('Number of stars = {}'.format(nr_stars))


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
    plt.scatter(xlist,ylist,c='b',s=4)
    plt.scatter(xobj_list, yobj_list, c='red', s=2)
    plt.plot([2000,2025],[0,0],c='r')
    for i in range(nr_stars):
    	plt.plot([xobj_list[i],xlist[indices[i]]],[yobj_list[i],ylist[indices[i]]], linestyle='dashed',c='r',linewidth=1)
    plt.title(f)
    plt.show()
    """
    return indices, np.diag(distance_matrix[indices])
    #the diagonal gives the distance from each selected object to the closest object

# Make one file with the image_name, epoch, filter and airmass
t_image, t_newimg, t_epoch, t_filter, t_airmass = [], [], [], [], []

#selects all names in ../data/
for filename in Path('..//data/').rglob('*e91.fits.fz'):
	filename = str(filename)
#	print (filename)
	# Open the file & extract certain data
	hdu1 = fits.open(filename)
	imh = hdu1['SCI'].header
	phot = hdu1['cat'].data
	
	# Getting the meta-data from the .fits file and writing it to lists
	epoch = imh['MJD-OBS']
	obs_filter = imh['FILTER']
	t_image.append(filename.replace('../data/',''))
	t_epoch.append(epoch)
	t_filter.append(obs_filter)
	t_airmass.append(imh['AIRMASS'])
	
	# Transform the world coordinates for the selected stars into pixel coordinates
	w = wcs.WCS(hdu1['SCI'].header)
	coord = w.wcs_world2pix(coord_world,0)
	
	# Make a new file path to write to with name= str( [EPOCH to 5 decimals (~1s)]_[FILTER])
	newfilename = '../datared/'+str(round(trunc(epoch*1e5)*1e-5,6)) + '_' + obs_filter + '.txt'
	t_newimg.append(newfilename)
	# Use the find_stars function to get the closest-star-indices for the selected stars
	stars_arg, d = find_stars(coord[:,0],coord[:,1], phot['x'], phot['y'], newfilename)
	
	# Use the indices to get the flux & fluxerr for all selected stars
	flux_stars = phot['flux'][stars_arg]
	fluxerr_stars = phot['fluxerr'][stars_arg]
	#if the distance is more than 25 pixels (~9.7"), it's too far away so it will write out NaN
	select_mask = d > 25
	flux_stars[select_mask] = np.NaN
	fluxerr_stars[select_mask] = np.NaN

	# Write data to Table and then to file
	filecontent = Table([range(1,nr_stars+1),flux_stars, fluxerr_stars], \
				names=['STARNR','FLUX','FLUXERR'])
	ascii.write(filecontent, newfilename, overwrite=True)

# Write out the meta_data elements to a file
filecontent = Table([t_image,t_newimg, t_epoch, t_filter, t_airmass], \
				names=['IMAGE','NEWIMG','EPOCH','FILTER','AIRMASS'])
filepath = "..//datared/J0600_meta-data.txt"
ascii.write(filecontent, filepath, overwrite=True)










