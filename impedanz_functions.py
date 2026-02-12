import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_impedance(file_path):
    """
    Reads impedance data from a CSV file and returns frequency,
    impedance and theta values.

    Args:
            file_path (str): Path to the CSV file.

    Returns:
        tuple: A tuple containing frequency, impedance and theta values
    """

    with open(file_path, 'r') as f:
        # skip first 4 rows because data begins after that
        df = pd.read_csv(f, skiprows=4, header=0)

        # Access to columns
        f = pd.to_numeric(df['Frequency(Hz)'][0:-1])
        Z = pd.to_numeric(df[' |Z|(Ohm)-data'][0:-1])
        theta = pd.to_numeric(df[' theta-z(deg)-data'][0:-1])
        # -1 because the last value is "END"

    return f, Z, theta

def calculate_R_C(f, Z, theta_deg):
    """
    Calculates resistance and capacitance values from impedance and
    theta values.

    Args:
        frequency (np.ndarray): Frequency values
        impedance (np.ndarray): Impedance values
        theta_deg (np.ndarray): Theta values in degrees

    Returns:
        tuple: A tuple containing resistance and capacitance values
    """
    omega = 2*np.pi*f

    # Calculate the theta in radians
    theta = theta_deg * np.pi / 180

    R = Z * np.sqrt(1 + np.tan(theta)**2)
    C = - np.tan(theta)/(omega * R)

    return R, C

def Z_parallel(f, C, R):
    """
    Calculates the parallel impedance.

    Args:
        frequency (np.ndarray): Frequency values
        capacitance (float): Capacitance value
        resistance (float): Resistance value

    Returns:
        np.ndarray: Parallel impedance values
    """
    omega = 2*np.pi*f

    Z = R/(1 + omega * R * C*1j)

    return Z

if __name__ == "__main__":

    impendance_meas = r"/Users/marinaivankovic/Desktop/Master/4Semester/Labor Mikrosystemtechnik/Program 2/Measured Data/CABEL.CSV"
    f, Z, theta = read_impedance(impendance_meas)

    R_in, C_in = calculate_R_C(f, Z, theta)
    print(R_in)

    Z_cal = np.absolute(Z_parallel(f, C_in, R_in))

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(8, 6), facecolor="white")

    # set axis lables
    ax.set_xlabel("Frequency []")
    ax.set_ylabel("Impedance")

    # plot data
    ax.loglog(f, Z, label="Measured", color="red",
              linewidth="1")
    #ax.plot(f, theta, label="Measured", color="red",
    #          linewidth="1")
    ax.loglog(f, Z_cal, label="Calculated", color="blue",
              linewidth="1")

    #ax.set_xlim(1e2, 1e7)
    #ax.set_ylim(2e2, 2e7)


    # Configure grid
    ax.grid(visible='true', which='major', color='grey')
    ax.grid(visible='true', which='minor', color='lightgrey')

    # add legend
    ax.legend()

    plt.show()



