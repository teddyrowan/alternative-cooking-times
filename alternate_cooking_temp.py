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


#### original solution is wrong, i must be an idiot / transfered poorly to WA
# this is the actual solution.
# https://www.wolframalpha.com/input/?i=alpha*dt+%3D+dT%2F%28215+-+T%29%5E4
# T(t) = 215 - (2*qqq*c1*t + c1^2 + qqq^2*t^2)^(1/3) / (3^(1/3)*(c1 + qqq*t))
# Apply BCs
# T(0) = -15
# https://www.wolframalpha.com/input/?i=215+-+%28c1%5E2%29%5E%281%2F3%29+%2F+%283%5E%281%2F3%29*c1%29+%3D+-15
# T(0) = 215 - (c1^2)^(1/3) / (3^(1/3)*c1) = -15
# c1 = 2.73965096*10^-8
# T(20) = 75
# https://www.wolframalpha.com/input/?i=215+-+%282*x*%282.73965096*10%5E-8%29*20+%2B+%282.73965096*10%5E-8%29%5E2+%2B+x%5E2*20%5E2%29%5E%281%2F3%29+%2F+%283%5E%281%2F3%29*%28%282.73965096*10%5E-8%29+%2B+x*20%29%29+%3D+75
# qqq ≈ -1.36983×10^-9 or ≈ 4.70403×10^-9
# should be the positive root?

# now plug that back into solve for the lower temp


#### This shit is just plain fucking wrong dumbshit.

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
