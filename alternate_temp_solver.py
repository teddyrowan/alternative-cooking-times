#alternate_temp_solver.py
# The actual solver accompagnying alternate_cooking_temp.py
# Author: Teddy Rowan

# For now I'm approximating 0C = 273K (dropping the .15)

# Example:
# Chicken Strips take 20 minutes to cook at 425 F = 215 C = 488 K
# Freezer is at about -15C ie: initial temp of the chicken = 258 K
# The chicken needs to get cooked to 75 C = 348 K
# If you decide to cook the chicken at 300 F = 150 C = 423 K, how long should it take

T0  = -15 + 273;    # 258 K Initial Chicken Temperature
TF  =  75 + 273;    # 348 K Final Chicken Tmeperature
TSC = 150 + 273;    # 423 K Cold version of the oven
TSH = 215 + 273;    # 488 K Hot version of the oven
time_orig = 20;

c1 = (TF-T0)/(pow(TSH,4) - pow(T0,4))/2 # first power of c1 approximation
#print(c1) #8.60720 e-10

track = [T0]
temp = T0

while temp < TF: # basic Euler's Method step-through. 
    temp_n = temp + c1*(pow(TSC,4) - pow(temp,4))
    track.append(temp_n)
    temp = temp_n

#print(track)

# now interpolate. solve this.
# TF = x*track[len(track)-2] + (1-x)*track[len(track)-1]
interp = (TF - track[len(track)-1])/(track[len(track)-2] - track[len(track)-1])
steps = (len(track) - 1) - interp
#print(steps) #good. 

# now figure out the length of the steps. ie: original cook time / 2
# then multiply the step
time_total = steps*time_orig/2;
#print("Cook time at alternate temperature: " + str(time_total) + " minutes.")
print("Cook time at alternate temperature: %02d mins." % time_total)


# below this is explanations. 


# The Governing Equation:
# dQ/dt = m*Cv*(dT) = a*(Ts^4 - T^4)
# This differential equation unfortunately doesn't have a particularly clean solution

# Let's use the known values and use Euler's Method to approximate the solution
# dQ/dT(n) = m*Cv*(T(n+1) - T(n)) = a*(Ts^4 - T(n)^4)
# Grouping Constants:
# T(n+i)  = T(n) + c1*(Ts^4 - T(n)^4)
# T(n+2i) = T(n+i) + c1*(Ts^4 - T(n+i)^4)
#         = T(n) + c1*(Ts^4 - T(n)^4) + c1*(Ts^4 - (T(n) + c1*(Ts^4 - T(n)^4))^4)
#         = T(n) + 2*c1*Ts^4 - c1*T(n)^4 - c1*(T(n) + c1*(Ts^4 - T(n)^4))^4

#TF = T0 + 2*c1*TSH^4 - c1*T0^4 - c1*(T0 + c1*(TSH^4 - T0^4))^4
#TF - T0 = c1(2*TSH^4 - T0^4 - (T0 + c1*(TSH^4 - T0^4))^4)
#x = TF- T0 || y = 2*TSH^4 - T0^4 || z = T0 || r = (TSH^4 - T0^4)
#x = c1*(y - (z + c1*r)^4) # will need to do some root-finding for this to solve c1.  (x,y,z,r are just numbers)
#x = c1*(y - (z + c1*r)^4)
## ohhhhh since the numbers are so small, can probably taylor-approximate and clear out the first few terms
#x = c1*y - c1*(z^2 + 2*z*c1*r + c1^2*r^2)^2
#x ~ c1*y - c1*z^4 = c1*(2*TSH^4 - T0^4 - T0^4)
#c1 ~ = (TF-T0)/(2*TSH^4 - T0^4 - T0^4)
#c1 ~ = (90)/(2*488^4 - 2*258^4) = 8.60720 * 10^-10 # off by 4%  # good enough for now. worst case use as initial approx.


# hmmmm is it worth looking at another term? probably not. complex roots. i guess not then. 
# the next hanging terms would be...
#x = c1*y - c1*(z^2 + 2*z*c1*r + O(c1^2))^2
#x ~ c1*y - c1*(z^4 + 4*z^5*c1*r + O(c1^2))
#x ~ c1*y - c1*z^4 - 4*z^5*r*c1^2
#0 ~ c1(y-z^4) - c1^2*(4*z^5*r) - x
#0 ~ c1*((2*TSH^4 - T0^4)-T0^4) - c1^2*(4*T0^5*(TSH^4 - T0^4)) - (TF-T0)
#0 ~ c1*((2*488^4 - 258^4)-258^4) - c1^2*(4*258^5*(488^4 - 258^4)) - (90) #c1 is complex. 

# Example: (using 10 minute steps)
# T(2) = T(0) + 2*c1*Ts^4 - c1*T(0)^4 - c1*(T(0) + c1*(Ts^4 - T(0)^4))^4
# 348 = 258 + 2*c1*(488)^4 - c1*(258)^4 - c1*(258 + c1*(488^4 - 258^4))^4
# Solved on Wolfram: c1 = 8.9683E-10 or 5.6279E-9
# This is the one step that will be a pain to do programatically. Start off with just a binomial search between 0-1 and then after that move to NM or similar to converge faster. 



# Plug c1 into the colder temperature example and see what we get. 
#T(i+1) = T(i)      + c1*(T_s^4 - T(i)^4)
#T(i+1) = T(i)      + 8.9683*10^-10*(423^4 - T(i)^4)
#T(1)   = 258       + 8.9683*10^-10*(423^4 - 258.00^4) = 282.74 K = 9.74  C
#T(2)   = 282.74    + 8.9683*10^-10*(423^4 - 282.74^4) = 305.72 K = 32.72 C
#T(3)   = 305.72    + 8.9683*10^-10*(423^4 - 305.72^4) = 326.60 K = 53.00 C
#T(4)   = 326.00    + 8.9683*10^-10*(423^4 - 326.00^4) = 344.58 K = 71.58 C
#T(5)   = 344.58    + 8.9683*10^-10*(423^4 - 344.58^4) = 360.65 K = 87.65 C

# Interpolating between T(4) and T(5) to find T(x) = 75 C
# T(x) = 4.21 ==> It should take 42 minutes to cook the chicken strips @ 300 F instead of 425 F
# Euler's Method in this case is a faster than actual approximation due to the declining nature of the DE.

## What happens if we use the other root of c1?
#T(1)   = 258       + 5.6279*10^-9*(423^4 - 258.00^4) = 413.24 K = 140 C  --> basically already converged. 

## What happens if we use the approximate solution of c1?
#T(1)   = 258       + 8.5623*10^-10(423^4 - 258.00^4) = 281.62 K = 8.62  C
#T(2)   = 281.62    + 8.5623*10^-10(423^4 - 281.62^4) = 303.64 K = 30.64 C
#T(3)   = 303.64    + 8.5623*10^-10(423^4 - 303.64^4) = 323.77 K = 50.77 C
#T(4)   = 323.77    + 8.5623*10^-10(423^4 - 323.77^4) = 341.77 K = 68.77 C
#T(5)   = 341.77    + 8.5623*10^-10(423^4 - 341.77^4) = 357.50 K = 84.50 C
# Interpolating 4.39 ==> 44 minutes to cook the chicken @ 300 F instead of 425 F
# Close enough for an early run. My fear is that this might become an issue as I expand. 