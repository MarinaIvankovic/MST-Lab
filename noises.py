import numpy as np

# Physical Constants
kB = 1.380649e-23 # J/K
q = 1.601e-19 # C

# Operating Condition
T = 300  #K (room temperature)

def noise_Rin(R_in, Z_parallel, f_in):
    """
        Calculates the Johnson-Nyquist noise at the input.

        Args:
            R_in (float): Input resistance
            Z_parallel (complex): Parallel impedance

        Returns:
            float: Absolute value of the output noise voltage
    """

    u_Rin = np.sqrt(4 * kB * T * R_in)

    v_out = - u_Rin / R_in * Z_parallel 

    return np.absolute(v_out)

def noise_u(u, Z_in, Z_parallel, f_in):
    """
        Calculates the noise contribution from the u noise source.

        Args:
            u (float): u noise source amplitude
            R_in (float): Input resistance
            Z_in (complex): Input impedance
            Z_parallel (complex): Parallel impedance

        Returns:
            float: Absolute value of the output noise voltage.
    """

    v_out = u / Z_in * (Z_parallel + Z_in) 
    #v_out = u *Z_in / Z_in

    return np.absolute(v_out)

def noise_i(i, Z_parallel, Z_in, f_in):
    """
       Calculates the noise contribution from the i noise source.

       Args:
           i (float): i noise source amplitude
           Z_parallel (complex): Parallel impedance

       Returns:
           float: Absolute value of the output noise voltage
    """
    
    # new idea
    #i_1 = - i * Z_in / (Z_parallel + Z_in)
    #i_2 = i * Z_in / (Z_in + Z_parallel)
    #v_out = Z_parallel * i_2 + Z_in * i_1 

    #Z_all = Z_in * Z_parallel / (Z_in + Z_parallel)

    #v_out = - i * Z_in / Z_all * Z_parallel * 100
    
    v_out = Z_parallel * i 

    return np.absolute(v_out)

def noise_R(f, R, C):
    """
        Calculates the noise contribution from the resistor.

        Args:
            f (float): Frequency
            R (float): Resistance
            C (float): Capacitance

        Returns:
            float: Absolute value of the output noise voltage
        """

    u_R = np.sqrt(4 * kB * T * R)

    omega = 2*np.pi*f

    v_out = u_R/(1+omega*C*R*1j)

    return np.absolute(v_out)