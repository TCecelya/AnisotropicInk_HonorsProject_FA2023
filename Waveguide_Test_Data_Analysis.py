# Thomas Cecelya
# Date Started: 20 Oct 2023
# Desc.: This script will be used to take excel format data from X-band waveguide testing of 
#       a sample of anisotropic ink and perform an FFT to isolate high frequency data from 
#       target data at the X-band midpoint of 10.65 GHz.


# Code Flow:
# - Import data into pandas dataframe
# - Plot each quantity over frequency (plot S11 and S21 on same plot)
# - Pass data for epsilon, loss tangent, S11, and S21 through numpy FFT
# - Display the results in a table (or plot the filtered data if necessary)


# Import Modules:
