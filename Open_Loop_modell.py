import json
import matplotlib.pyplot as plt
import numpy as np

from impedanz_functions import *
from noises import *

# Define Noise Sources
u = 7.5e-9  # V/sqrt(Hz)
i = 3e-15  # A/sqrt(Hz) 

# Define File Path
json_file_path = r"/Users/marinaivankovic/Desktop/Master/4Semester/Labor Mikrosystemtechnik/Program 2/Measured Data/Open Circuit/20241029_102716_SA1_MLA_P4_Tx_BW10_NAVG100_R1100101_PAGC1000_.json"
cabel_file_path = r"/Users/marinaivankovic/Desktop/Master/4Semester/Labor Mikrosystemtechnik/Program 2/Measured Data/CABEL.CSV"

if __name__ == "__main__":

    # Read Measured Density
    with open(json_file_path, 'r') as f:
        data = json.load(f)

        frequency = data['mf']
        density = data['nd']
        density_np =  np.array(density[0])

    frequency_array = np.array(frequency[1:])

    # Define Charge Amplifier Parameters (Kistler type 5018)
    C = 33e-12 # F (from the block diagram)
    R = 1e9   # Ohm (from the diagram)
    Z_parallel = Z_parallel(frequency_array, C, R)
    
    # calculating the corner frequency 
    f_p = 1/(2*np.pi*C*R)
    
    A = R / (1 + 1j * 2* frequency_array * np.pi*C*R)
    
    fig,ax = plt.subplots(figsize=(8, 6), facecolor="white")
    #ax[0].loglog(frequency_array,A)
    
    v_out_u = u * frequency_array/frequency_array
    v_out_i = i*A
    v_out_R = noise_R(frequency_array, R, C)
    
    v_out = np.sqrt(v_out_u**2 + np.abs(v_out_i)**2 + v_out_R**2)
    
    ax.loglog(frequency_array, v_out, label='Calculated values')
    ax.loglog(frequency, density_np*165, label="Measured values")
    
    #ax.loglog(frequency_array, v_out_u, label="u part")
    #ax.loglog(frequency_array, v_out_i, label="i part")
    #ax.loglog(frequency_array, v_out_R, label="R part")
    ax.legend()
    ax.set_xlim(1e2,1e6)
    ax.set_ylabel("Noise Density (V/sqrt(Hz))")
    ax.set_xlabel("f (Hz)")    
