#kitchen ODE heat transfer solver.

# The idea of this script is to determine the alternate cooking times for different foods based on differing oven temperatures

# Example:
# Chicken Strips take 20 minutes to cook at 425 = 215 C
# Freezer is at about -15C

# The chicken should get cooked to about 75 C

# now if i'm lazy and don't want to wait for the oven to raise up to 215, and put my food in at 300f/150C how long should I cook it for.


# For radiation heat transfer
#dQ/dt = const * (Toven - T)^4
#dU = dQ/dt = Cv * dT/dt

# total heat requirement = Cv * (Tf - Ti)
# qqq * (Toven - T)^4 =  dT/dt
# how to solve DE....
# qqq* dt = dT/(T_oven - T)^4

# with T_oven = 215.
# T(t) = c1*exp(-qqq*t) + 215
# T(0) = -15
# T(20) = 75
# T(0) = c1 + 215 = -15 ==> c1 = -230
# T(t) = -230*exp(-qqq*t) + 215
# T(20) = 75 = -230*exp(-qqq*20) + 215
# ln(23/14)/20 = qqq = 0.02482184431

# with T_oven = 150
# T(t) = c1*exp(-0.0248218*t) + 150
# T(0) = -15
# For what t is T = 75?
# T(0) = -15 = c1 + 150 ==> c1 = -165
# T(t) = -165*exp(-0.024218*t) + 150
# T(x) = 75 = -165*exp(-0.024218*x) + 150
# ln(165/75)/(0.024218) = x = 32.5567 minutes
# ie: The chicken strips should take 33 minutes to cook instead.

# Now let's just automate this shit. And package it.
