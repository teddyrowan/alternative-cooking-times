# alternate_temp_solver.py (python3)
# Author: Teddy Rowan

import matplotlib.pyplot as plt

# Takes in the intial and final temperatures of the food, the original oven settings, the original cooking time, and the new oven settings and calculates cooking time based on the new settings. All temperatures in Kelvin. Output [time] in the same units as time input.
def calculate_cook_time(start_temp, end_temp, hot_oven_temp, cold_oven_temp, original_time):
    precision = 100

    c1 = (end_temp-start_temp)/(pow(hot_oven_temp,4) - pow(start_temp,4))/precision
    
    current_temp = start_temp
    temp_history = [current_temp]

    while current_temp < end_temp: # basic Euler's Method step-through. 
        next_temp = current_temp + c1*(pow(cold_oven_temp,4) - pow(current_temp,4))
        temp_history.append(next_temp)
        current_temp = next_temp
    
    interp = (TF - temp_history[-1])/(temp_history[-2] - temp_history[-1])
    steps = (len(temp_history) - 1) - interp

    # now figure out the length of the steps. ie: original cook time / precision  and then multiply by the step size
    time_total = steps*original_time/precision
    return time_total
    

# Example:
# Chicken Strips take 20 minutes to cook at 425 F = 215 C = 488 K
# Freezer is at about -15C ie: initial temp of the chicken = 258 K
# The chicken needs to get cooked to 75 C = 348 K
# If you decide to cook the chicken at 300 F = 150 C = 423 K, how long should it take
#T0         = -15 + k_convert;  # 258 K Initial Chicken Temperature
#TF         =  75 + k_convert;  # 348 K Final Chicken Tmeperature
#TSH        = 215 + k_convert;  # 488 K Hot version of the oven
#time_orig  = 20                # original cooking time. 
#TSC        = 150 + k_convert;  # 423 K Cold version of the oven

# Option to list safe internal temperatures of meats.
k_convert = 273.15;     # conversion from celcius to kelvin

T0          = float(input('Enter the intial temperature of the food (freezer ~ -15, fridge ~ 0C) [Celcius]: ')) + k_convert
TF          = float(input('Enter the final cooking temperature of the food [Celcius]: ')) + k_convert
TSH         = float(input('Enter the recommended cooking temperature for the food [Celcius]: ')) + k_convert
time_orig   = float(input('Enter the recommended cooking time @ previous temperature [minutes]: '))
TSC         = float(input('At what temperature would you like to cook the food [Celcius]: ')) + k_convert

new_time = calculate_cook_time(T0, TF, TSH, TSC, time_orig)
print("Cook time at alternate temperature: %02d mins." % new_time)


## Now let's loop through and plot a curve. 
low = 100 + k_convert;
high = 500 + k_convert;

temp_list = []
time_list = []

temp = low
while temp < high:
    tmp_time = calculate_cook_time(T0, TF, TSH, temp, time_orig)
    temp_list.append(temp)
    time_list.append(tmp_time)
    temp = temp + 5

temp_list = [x - k_convert for x in temp_list]

fig = plt.figure()
plt.plot(temp_list, time_list, 'ro-', markersize=3)
plt.xlabel("Oven Temperature [Celcius]")
plt.ylabel("Equivalent Cooking Time [minutes]")
plt.title("Alternative Cooking Times")
plt.grid()
plt.show()