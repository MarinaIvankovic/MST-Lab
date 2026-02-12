import json
import matplotlib.pyplot as plt
import numpy as np

from impedanz_functions import *
from noises import *

# Define Noise Sources
u = 7.5e-9  # V/sqrt(Hz)
i = 3e-15  # A/sqrt(Hz)

# Define File Path
json_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Measured Data\Measured Data\3n3F\20241105_122914_SA1_MLA_P4_Tx_BW10_NAVG100_R1100101_PAGC1000_.json"
impedanz_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Measured Data\Measured Data\3n3F\3n3F.CSV"
cabel_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Measured Data\Measured Data\CABEL.CSV"

if __name__ == "__main__":

    # Read Measured Density
    with open(json_file_path, 'r') as f:
        data = json.load(f)

        frequency = data['mf']
        density = data['nd']
        density_np =  np.array(density[0])

    frequency_array = np.array(frequency[1:])

    # Calculate Input Capactance
    f_in, Z_in, theta_in = read_impedance(impedanz_file_path)
    R_in, C_in = calculate_R_C(f_in, Z_in, theta_in)
    #because Z_in is a abs value 
    Z_in = Z_in * (np.cos(theta_in) + 1j * np.sin(theta_in))

    # Calculate Cabel Parameters
    f_C, Z_C, theta_C = read_impedance(cabel_file_path)
    R_C, C_C = calculate_R_C(f_C, Z_C, theta_C)
    Z_C = Z_C * (np.cos(theta_C) + 1j * np.sin(theta_C))
    
    # Calculate Input Parameters (Cabel + Sample)
    C_inc = C_in + C_C
    R_inc = R_in * R_C / (R_in + R_C)
    Z_inc = 1/(2*np.pi*f_in*C_inc)
    #Z_in = Z_parallel(f_in, C_inc, R_inc)
    Z_in = Z_in * Z_C / (Z_in + Z_C)    

    # Define Charge Amplifier Parameters (Kistler type 5018)
    C = 33e-12 # F (from the block diagram)
    R = 1e9   # Ohm (from the diagram)
    Z_parallel = Z_parallel(f_in, C, R)
    Z_parallel_abs = np.absolute(Z_parallel)
    
    #print(f'frist: {1/(2*np.pi*R*C)}')
    #print(f'second: {1/(np.pi*R_inc * R * (C_inc + C)/ (2*np.pi*R_inc + R * (C_inc + C)))}')


    # Calculate Noise Density
    #v_out_Rin = noise_Rin(R_in, Z_parallel,f_in)
    v_out_u = noise_u(u, Z_in, Z_parallel, f_in)
    #v_out_u = noise_u(u, Z_parallel, Z_parallel)
    v_out_i = noise_i(i, Z_parallel, Z_in, f_in )
    #v_out_i = noise_i(i, Z_parallel, Z_parallel)
    #v_out_R = noise_R(f_in, R, C)
    #v_out = np.sqrt(v_out_Rin**2 + v_out_u**2 + v_out_i**2 + v_out_R**2)
    v_out = np.sqrt(v_out_u ** 2 + v_out_i ** 2)
    #v_out = np.sqrt(v_out_Rin**2 + v_out_u**2 + v_out_i**2)

    # Plot Data
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")

    ax.set_xlabel("Frequency []")
    ax.set_ylabel("Density (V/sqrt(Hz)")

    ax.loglog(frequency, density_np*165, label="Measured Data", color="red", linewidth="1")
    ax.loglog(f_in, v_out, label="Calculated Data", color="blue", linewidth="1")
    #ax.loglog(f_in, v_out_Rin, label="Rin Noise Source", color="green", linewidth="1")
    #ax.loglog(f_in, v_out_u, label="U Noise Source", color="yellow", linewidth="1")
    #ax.loglog(f_in, v_out_i, label="i Noise Source", color="black", linewidth="1")
    #ax.loglog(f_in, v_out_R, label="R Noise Source", color="orange", linewidth="1")
    #ax.loglog(f_in,Z_in, label="Z_in", linewidth="1")
    #ax.loglog(f_in,Z_parallel, label="Z_parallel", linewidth="1")

    ax.set_xlim(1e2, 1e6)
    #ax.set_ylim(1e-8, 1e-3)

    ax.grid(visible='true', which='major', color='grey')
    ax.grid(visible='true', which='minor', color='lightgrey')

    ax.legend()

    plt.show()
