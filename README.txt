# BRPJ0600
Git repository by Bart Ouwehand for Bachelor research project on ASASSN-V J060000.76-310027.83 (J0600 short), supervised by Dr. M.A. Kenworthy at Leiden University. Contact at ouwehand@strw.leidenuniv.nl & kenworthy@strw.leidenuniv.nl.


To run the code with the existing data, take the following steps.
*ASTEP lightcurve: run the 'ASTEP.ipynb' notebook.
*LCOGT & ASTEP lightcurve: run the following notebooks:
	1) First 'LCOGT_ZP_calc.ipynb'
	2) Then 'ASTEP.ipynb'
	3) Lastly 'LCOGT.ipynb'
*Dust-size calculation: run the following notebooks:
	1) First 'LCOGT_ZP_calc.ipynb'
	2) Then 'ASTEP.ipynb'
	3) Then 'LCOGT.ipynb'
	4) Lastly 'Dust-size.ipynb'



To run the code with new LCOGT data, follow these steps.
1) Have a folder structure like this
Main folder
-> "any_name"
	-> [GIT REPOSITORY]
-> data
	-> [FITS FILES]
2) Run 'script1.py' (which reads the file '..//data/coj1m003-fa19-20210112-0083-e91.fits.fz', extracts the coordinates from all stars within 400" of target and writes it to 'standards.txt')
3) Run 'script2.py' (which extracts the photometry of all stars from standards.txt from all .fits files inside '../data' which end in 'e91.fits.fz')
4) Take the steps from above
 

