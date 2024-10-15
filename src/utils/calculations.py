"""
Some calculations that are used for heat pump data analysis
"""

def power_from_flow(flow: float, temperature_difference: float):
    """
    Calculate the power from a given flow rate and temperature difference
    
    :param flow: The flow rate in litres per minute
    :param temperature_difference: The temperature difference in degrees Celsius
    """
    return (flow / 60.0) * 4.1868 * temperature_difference

def cop(power_in: float, power_out: float):
    """
    Calculate the Coefficient of Performance

    :param power_in: The power/energy in
    :param power_out: The power/energy out
    """
    return 0 if float(power_in) == 0.0 else float(power_out) / float(power_in)