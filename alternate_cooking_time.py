# alternate_cooking_time.py (python3)
# Author: Teddy Rowan
# Last Modified: July 19, 2020
# Description: Numerical PDE solver to calculate alternative cooking times (based on total heat transfer) for different oven temperatures.

import matplotlib.pyplot as plt
import numpy as np

# TODO: Option to list safe internal temperatures of meats.

# Takes in the intial and final temperatures of the food, the original oven settings, the original cooking time, and the new oven settings and calculates cooking time based on the new settings. All temperatures in Kelvin. Output [time] in the same units as time input.
def calculate_cook_time(start_temp, end_temp, hot_oven_temp, cold_oven_temp, original_time):
    step_precision = 100 # how many steps to use in c1 approximation

    c1 = (end_temp-start_temp)/(pow(hot_oven_temp,4) - pow(start_temp,4))/step_precision
    
    current_temp = start_temp
    temp_history = [current_temp]

    while current_temp < end_temp: # basic Euler's Method step-through. 
        next_temp = current_temp + c1*(pow(cold_oven_temp,4) - pow(current_temp,4))
        temp_history.append(next_temp)
        current_temp = next_temp
    
    interp = (end_temp - temp_history[-1])/(temp_history[-2] - temp_history[-1])
    steps = (len(temp_history) - 1) - interp

    time_total = steps*original_time/step_precision
    return time_total
    

# Example (chicken strips):
#temp_init  = -15 + k_convert;  # 258 K Initial Chicken Temperature
#temp_final =  75 + k_convert;  # 348 K Final Chicken Tmeperature
#oven_rec   = 215 + k_convert;  # 488 K Hot version of the oven
#time_rec   = 20                # original cooking time. 
#oven_new   = 150 + k_convert;  # 423 K Cold version of the oven

k_convert = 273.15;     # conversion from celcius to kelvin

print("Enter the following values: ")

# The initial temperature of the food. 
temp_init   = float(input('Intial temperature of the food (freezer ~ -15°C, fridge ~ 0°C) [°C]: ')) + k_convert
# The final temperature of the food when it's done in the oven.
temp_final  = float(input('Final temperature of the food [°C]: ')) + k_convert
# The recommended cooking temperature
oven_rec    = float(input('Recommended cooking temperature for the food [°C]: ')) + k_convert
# The recommended cooking time @ the recommended cooking temperature
time_rec    = float(input('Recommended cooking time @ previous temperature [minutes]: '))
# The new temperature that you want to cook the food at
oven_new    = float(input('At what temperature would you like to cook the food instead [°C]: ')) + k_convert


print("Now calculating new cooking times...")
new_time = calculate_cook_time(temp_init, temp_final, oven_rec, oven_new, time_rec)
print("Cook time at alternate temperature: %02d mins." % new_time)


## Now let's loop through and plot a curve. 
low             = 100 + k_convert
high            = 500 + k_convert
temp_interval   = 5

temp_list = np.array([])
time_list = np.array([])

for temp in range(int(low), int(high), temp_interval):
    tmp_time = calculate_cook_time(temp_init, temp_final, oven_rec, temp, time_rec)
    temp_list = np.append(temp_list, temp)
    time_list = np.append(time_list, tmp_time)

temp_list = [x - k_convert for x in temp_list]

fig = plt.figure()
plt.plot(temp_list, time_list, 'ro-', markersize=3)
plt.xlabel("Oven Temperature [Celcius]")
plt.ylabel("Equivalent Cooking Time [minutes]")
plt.title("Alternative Cooking Times")
plt.grid()
plt.show()