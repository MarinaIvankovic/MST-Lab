import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
from impedanz_functions import *
from noises import *

# Define Noise Sources
u = 8e-10  # V/sqrt(Hz)
i = 1e-12  # A/sqrt(Hz) 

# Define File Path
json_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Measured Data\Measured Data\3n3F\20241105_122914_SA1_MLA_P4_Tx_BW10_NAVG100_R1100101_PAGC1000_.json"
impedanz_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Measured Data\Measured Data\CABEL.CSV"
cabel_file_path = r"/Users/marinaivankovic/Desktop/Master/4Semester/Labor Mikrosystemtechnik/Program 2/Measured Data/CABEL.CSV"

if __name__ == '__main__':
    
    # Calculate Input Capactance
    f_in, Z_in, theta_in = read_impedance(impedanz_file_path)
  #  Z_mag_mean = savgol_filter(Z_mag, window_length=30, polyorder=3)
  #  theta_in_mean = savgol_filter(theta_in, window_length=200, polyorder=3)
    
    # Reconstruct complex impedance FIRST
   # Z_in = Z_mag_mean * (np.cos(theta_in_mean) + 1j * np.sin(theta_in_mean))
    
    # For calcualting the R and C we need the magnitude
    R_in, C_in = calculate_R_C(f_in, Z_in, theta_in)  
    
    # Define Charge Amplifier Parameters (Kistler type 5018)
    C              = 33e-12                          # F (from the block diagram)
    R              = 1e9                             # Ohm (from the diagram)
    Z_parallel     = Z_parallel(f_in, C, R)
    Z_parallel_abs = np.absolute(Z_parallel)
    
    
    # corner frequencies
    fp  = 1/(2*np.pi*R*C) 
    R_par = R*R_in[0]/(R+R_in[0])
    fz = 1/(2*np.pi*R_par*(C+C_in[0]))
    
    print(f'fp={fp} and fz={fz}')
    
    fig, ax = plt.subplots(2,2,figsize=(9, 8), facecolor="white")
    
    ax[0,0].semilogx(f_in, Z_in)
    ax[0,0].set_ylabel("|Zin|")
    ax[0,0].set_xlabel("f")
    ax[0,0].set_xlim(1e2,1e5)
    
    ax[0,1].semilogx(f_in, theta_in)
    ax[0,1].set_ylabel("theta")
    ax[0,1].set_xlabel("f")
    ax[0,1].set_xlim(1e2,1e5)
    ax[0,1].set_ylim(-95,-85)
    
    ax[1,0].semilogx(f_in, C_in)
    ax[1,0].set_ylabel("Cin")
    ax[1,0].set_xlabel("f")
    ax[1,0].set_xlim(1e2,1e5)
    #ax[1,0].set_ylim(0,5e-9)
    
    ax[1,1].semilogx(f_in, R_in)
    ax[1,1].set_ylabel("Rin")
    ax[1,1].set_xlabel("f")
    ax[1,1].set_xlim(1e2, 1e5)
plt.show()