This folder contains the code for the atmospheric extinction model we decided not to use.

testfile3.ipynb reads the data from ../datared/ , removes the bad data and selects the 20 stars with least variance and writes the resulting data to ../dataredred/
testfile4.ipynb reads the data from ../dataredred/ and applies the atmospheric extinction model to it with the gaia G and G_{rp} filters as the reference gp and rp magnitudes. 
