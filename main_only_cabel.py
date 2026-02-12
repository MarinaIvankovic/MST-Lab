import json
import matplotlib.pyplot as plt
import numpy as np

from impedanz_functions import *
from noises import *

# Define Noise Sources
u = 7e-5  # V/sqrt(Hz)
i = 3e-10  # A/sqrt(Hz)

# Define File Path
json_file_path = r"C:\Users\IvankoviMari\Documents\The Lab on the University\Cable_meas\2025_05\20250310_134854_SA1_MLA_P4_Tx_BW10_NAVG1000_R1100101_PAGC1_.json"

if __name__ == "__main__":
    # Read Measured Density
    with open(json_file_path, 'r') as f:
        data = json.load(f)

        frequency = data['mf']
        density = data['nd']
        density_np = np.array(density[0])

    frequency_array = np.array(frequency[1:])

    # Calculate Input Capactance
    C_in = 300e-12
    Z_in = 1/(2*np.pi*frequency_array*C_in*1j)

    # Define Charge Amplifier Parameters (Kistler type 5018)
    C = 33e-12  # F (from the block diagram)
    R = 1e9  # Ohm (from the diagram)
    Z_parallel = Z_parallel(frequency_array, C, R)
    Z_parallel_abs = np.absolute(Z_parallel)

    # print(f'frist: {1/(2*np.pi*R*C)}')
    # print(f'second: {1/(np.pi*R_inc * R * (C_inc + C)/ (2*np.pi*R_inc + R * (C_inc + C)))}')

    # Calculate Noise Density
    # v_out_Rin = noise_Rin(R_in, Z_parallel,f_in)
    v_out_u = noise_u(u, Z_in, Z_parallel, frequency_array)
    # v_out_u = noise_u(u, Z_parallel, Z_parallel)
    v_out_i = noise_i(i, Z_parallel, Z_in, frequency_array)
    # v_out_i = noise_i(i, Z_parallel, Z_parallel)
    # v_out_R = noise_R(f_in, R, C)
    # v_out = np.sqrt(v_out_Rin**2 + v_out_u**2 + v_out_i**2 + v_out_R**2)
    v_out = np.sqrt(v_out_u ** 2 + v_out_i ** 2)
    # v_out = np.sqrt(v_out_Rin**2 + v_out_u**2 + v_out_i**2)

    # Plot Data
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")

    ax.set_xlabel("Frequency []")
    ax.set_ylabel("Density (V/sqrt(Hz)")

    ax.loglog(frequency, density_np * 165, label="Measured Data",
              color="red", linewidth="1")
    ax.loglog(frequency_array, v_out, label="Calculated Data", color="blue",
              linewidth="1")
    # ax.loglog(f_in, v_out_Rin, label="Rin Noise Source", color="green", linewidth="1")
    # ax.loglog(f_in, v_out_u, label="U Noise Source", color="yellow", linewidth="1")
    # ax.loglog(f_in, v_out_i, label="i Noise Source", color="black", linewidth="1")
    # ax.loglog(f_in, v_out_R, label="R Noise Source", color="orange", linewidth="1")
    # ax.loglog(f_in,Z_in, label="Z_in", linewidth="1")
    # ax.loglog(f_in,Z_parallel, label="Z_parallel", linewidth="1")

    ax.set_xlim(1e2, 1e6)
    # ax.set_ylim(1e-8, 1e-3)

    ax.grid(visible='true', which='major', color='grey')
    ax.grid(visible='true', which='minor', color='lightgrey')

    ax.legend()

    plt.show()
