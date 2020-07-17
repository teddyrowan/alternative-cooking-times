#alternate_temp_solver.py

# The actual solver accompagnying alternate_cooking_temp.py
# Author: Teddy Rowan

# For now I'm approximating 0C = 273K (dropping the .15)

# Example:
# Chicken Strips take 20 minutes to cook at 425 F = 215 C = 488 K
# Freezer is at about -15C ie: initial temp of the chicken = 258 K
# The chicken needs to get cooked to 75 C = 348 K
# If you decide to cook the chicken at 300 F = 150 C = 423 K, how long should it take

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

