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
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import numpy.fft as fft
import os 



# Function Declarations:

def read_data(filepath, numrows):
    '''read_data(): Reads raw data from .xlsx or .csv file into a Pandas dataframe. 

    Args:
    - filePath (str): File path for .csv or .xlsx raw data file
    - numRows (int): Number of rows (zero-indexed) to be skipped at beginning of file

    Returns: 
    - dataFrame (dataframe): Pandas dataframe containing raw data from .csv or .xlsx raw data file
    '''

    # Open the file if it is a .csv format:
    if filepath.count(".csv") > 0:
        dataFrame = pd.read_csv(filepath, skiprows = numrows)
    
    # Open the file if it is a .xlsx format:
    elif filepath.count(".xlsx") > 0:
        dataFrame = pd.read_excel(filepath, skiprows = numrows)
    
    # Unrecognized file format:
    else:
        print("\nUNRECOGNIZED FILE FORMAT\n")
        exit()
    
    # Return the dataframe object:
    return dataFrame

def compute_fft(input_data, data_header, freq_header):
    """compute_fft(): Computes and returns the one-dimensional discrete FFT of the given input.

    Args:
    - input_data (Dataframe): Dataframe containing data to perform FFT
    - data_header (str): String indicating the column header for the data to be analyzed with FFT
    - freq_header (str): String indicating the column header for the frequency of the dataset


    Returns:
    - dataFFT (numpy array): Array containing the FFT of the input data.
    """

    # Convert the pandas series into a numpy array, then compute the fourier magnitude and phase
    signal = np.array(input_data[data_header])
    fourier_rectangular = fft.fft(signal)
    fourier_magnitude = np.absolute(fourier_rectangular)
    freq = np.array(input_data["frequency(Hz)"])

    # Initialize array of 1 column and the same number of rows as original signal to hold phase data
    fourier_phase = np.zeros(shape = (freq.size))

    # Compute phase for each element of the fft array (which is an array of complex rectangular form numbers):
    for n in range(freq.size):
        fourier_phase[n] = (np.arctan2(np.imag(fourier_rectangular[n]), np.real(fourier_rectangular[n])))
    
    print(f"\nFourier Magnitude: \n{fourier_magnitude}\n")
    print(f"\nFourier Phase: \n{fourier_phase}\n")

    print(f"\nSize of fourier_magnitude: \n{fourier_magnitude.size}\n")
    print(f"\nSize of fourier_phase \n{fourier_phase.size}\n")
    print(f"\nSize of freq: \n{freq.size}\n")

    # Initialize empty list:
    filter_list = []

    # Obtain list of entries with frequency greater than 11.5 GHz:
    for n in range(freq.size):
        if freq[n] > 1.15e+10:
            filter_list.append(n)
    
    # Remove all entries from magnitude, phase, and frequency arrays corresponding to frequency greater than 11.5 GHz    
    filtered_fourier_magnitude = np.delete(fourier_magnitude, filter_list)
    filtered_fourier_phase = np.delete(fourier_phase, filter_list)
    filtered_freq = np.delete(freq, filter_list)

    print(f"\nfiltered_fourier_magnitude: \n{filtered_fourier_magnitude}\n")
    print(f"\nfiltered_fourier_phase: \n{filtered_fourier_phase}\n")
    print(f"\nfiltered_freq: \n{filtered_freq}\n")

    # Initialize an array to contain the rectangular form of the filtered Fourier data:
    filtered_fourier_rectangular = np.zeros(shape = filtered_freq.size, dtype = 'complex_')


    # Convert the filtered data back to rectangular form:
    for n in range(filtered_freq.size):
        filtered_fourier_rectangular[n] = filtered_fourier_magnitude[n] * np.exp(1j * filtered_fourier_phase[n])
    
    print(f"\nfiltered_fourier_rectangular: \n{filtered_fourier_rectangular}\n")

    # Compute the inverse FFT using the filtered rectangular FFT data:
    inverse_filtered_fourier = fft.ifft(filtered_fourier_rectangular).real

    print(f"\ninverse_filtered_fourier: \n{inverse_filtered_fourier}\n")
    

    # Plot the FFT magnitude over the filtered frequency data:
    plt.figure(1)
    plt.plot(filtered_freq, filtered_fourier_magnitude)
    plt.title("FFT Magnitude versus Frequency (Post-Low Pass Filtering)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (in Fourier Domain, dB?)")
    plt.show()

    # Plot the FFT phase over the filtered frequency data:
    plt.figure(2)
    plt.plot(filtered_freq, filtered_fourier_phase)
    plt.title("FFT Phase versus Frequency (Post-Low Pass Filtering)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (in Fourier Domain, radians?)")
    plt.show()
    
    # Plot the Inverse FFT magnitude over the filtered frequency data:
    plt.figure(3)
    plt.plot(filtered_freq, inverse_filtered_fourier)
    plt.title("Final Inverse FFT Magnitude versus Frequency (Post-Low Pass Filtering)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB?)")
    plt.show()

    
    # Return the array containing the computed FFT:
    # return dataFFT



# Default Execution (DO NOT EDIT)
def main():
    # File path for directory containing desired data:
    filePath = r'C:\Users\tcece\OneDrive\Desktop\School\Senior Year 2023\Fall 2023\Honors Project\Waveguide Testing Data'

    # Number of leading rows to skip in raw data (generated by PNA Network Analyzer equipment):
    numRows = 14

    # List of desired column headers (for easier manipulation):
    # columnsToReplace = ["frequency(Hz)", "Tr 1  Data(e')", "Tr 2  Data(e''/e')", "Tr 3  S11(LogM)", "Tr 4  S21(LogM)"]
    
    # newColumnHeaders = ["Frequency (Hz)", "Epsilon", "Loss Tangent", "S11 (dB)", "S21 (dB)"]

    # Acquire list of all files at the filePath directory:
    fileList = os.listdir(filePath)

    # Iterate through each file in the directory:
    for file in fileList:

        # Concatenate file name to filePath string:
        filePath = filePath + "/" + file

        # ***** DEBUG MESSAGE ***** #
        # print(f"\nFull file path: {filePath}\n")

        # Call read data function:
        rawData = read_data(filePath, numRows)

        # Rename the column headers to match desired format:
        # rawData.rename(colHeaders, axis = 'columns', inplace = True)

        # ***** DEBUG MESSAGE ***** #
        print(f"\nRaw Dataframe for {file}:\n{rawData}\n")

        # Remove current file name from the file path before moving to next file in directory:
        filePath = filePath.replace("/" + file, '')

        freqHeader = "frequency(Hz)"
        # dataHeader = "Tr 1  Data(e')"
        # dataHeader = "Tr 2  Data(e''/e')"
        # dataHeader = "Tr 3  S11(LogM)"
        dataHeader = "Tr 4  S21(LogM)"
        
        compute_fft(rawData, dataHeader, freqHeader)

        

if __name__ == '__main__':
    main()