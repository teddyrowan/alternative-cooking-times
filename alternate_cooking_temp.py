#kitchen ODE heat transfer solver.

# The idea of this (to-be) script is to determine the alternate cooking times for different foods based on differing oven temperatures. Need to nail down the math/algorithm first though. 

# Example:
# Chicken Strips take 20 minutes to cook at 425 = 215 C
# Freezer is at about -15C

# The chicken should get cooked to about 75 C

# now if i'm lazy and don't want to wait for the oven to raise up to 215, and put my food in at 300f/150C how long should I cook it for.


# having issues w/ ordinary solutions having complex valued constants. 

##### hmmmmmmmm what if we approximate it as a big difference between Toven and Tchicken and say there is constant heat transfer... i like it. 
#q = const * (Ts^4 - T^4)
#qf/q0 = (Ts^4 - Tf^4)/(Ts^4 - T0^4) = (488^4 - 348^4)/(488^4-258^4) = 0.804
#hmmmm. hmmmmmmmmm. hmmmmmmmmmmmmmmmmmmmm. probably good enough. maybe do a interpolation to fix. bounded range. 
#ie: @ the end of the cook, there is still 78% of the initial heat flow. oh shit that was for the oven at 215 though. 

#lets do the math w/ the oven @ 150C
#qf/q0 = (Ts^4 - Tf^4)/(Ts^4 - T0^4) = (423^4 - 348^4)/(423^4-258^4) = 0.63
#ie: @ the end of the cook, the heat transfer has been reduced to only 63% of the initial heat flow. 
#hmmm. hmmmmmmm. is 63% close enough... i think we can use that to bound the range.

#need to figure out the shape of the curve. well its a constant - x^4 so a quickly falling steeper parabola
#dq/dt = const* (Ts^4 - T^4)


## need to think about this some more...
#okay so let's look at the original version.
dQ = Cv*(Tf-T0) = const*(Ts^4 - T^4)*t
Cv/const = c1  --> (Tf-T0)*c1 = (Ts^4 - T^4)*t
(90)*c1 = (488^4 - 258^4)*20
c1 = 1.1618 *10^10

(90)*c1 = (488^4 - 348^4)*20
c1 = 9.3436 *10^9

#Bounding Range for c1 (9.34, 11.62)*10^9

# let's look at the colder oven example. 
(Tf-T0)*c1 = 90*c1 = (Ts^4 - T^4)*t
t = 90*c1/(488^4 - T^4)
t1 = 90*9.34*10^9/(423^4 - 258^4) = 30.47
t2 = 90*9.34*10^9/(423^4 - 348^4) = 48.45
t3 = 90*11.62*10^9/(423^4 - 258^4) = 37.91
t4 = 90*11.62*10^9/(423^4 - 348^4) = 60.28

# So bounding cooking temp is from (30.5, 60.3) minutes. Need to narrow this down w/ interpolation. 
# Heat transfer is fastest at the start and then constantly falling, so initial approximation is to just cut the earlier ranges in half (keep second half). So for hot oven from 1 to 0.804, the net is going to be somewhere between 0.90 and 0.80. A decent guess might be 1/3 or halfway into this range so 0.85 to 0.87
# And for the cold oven is going to be somewhere between 0.82 and 0.63. A decent guess might be 1/3 or halfway into this range so 0.72 to 0.76

# let's redo the math with those approximations (0.86 and 0.74) below.
# okay so 0.86 of max heat transfer for case 1.
dQ*20 = Cv*(75+15) = const*((215+273)^4 - (-15+273)^4)*20*0.86
c1 = Cv/const = 9.9916E9 --- 1/c1 = 1.0008E-10 # this value does fall inside the bounds. good. 

# now plug that into the lower temp over w/ 0.74
dQ*t = Cv*(75+15) = const*((150+273)^4 - (-15+273)^4)*t*0.74
t = Cv/const*(90)/((150+273)^4 - (-15+273)^4)/0.74 = 44.05 #44 minutes. hmm. this seems about right. 



# What if we take a numerical DE solution approach instead? this should hopefully somewhat line up. 

#So let's Euler's Method this for now. Then swap to RK later on (RK is basically Trapezoidal Euler where Euler is like a LHS Riemman Sum but with derivative approximations)
dQi/dti = Cv*(T(i+1)-T(i)) = const*(T_s^4 - T(i)^4)

-- 
c1 = const/Cv
T(i+1) = T(i) + c1*(T_s^4 - T(i)^4)
T(i+2) = T(i+1) + c1*T_s^4 - c1*T(i+1)^4
       = T(i) + c1*T_s^4 - c1*T(i)^4 + c1*T_s^4 - c1*(T(i) + c1*T_s^4 - c1*T(i)^4)^4
       = T(i) + 2*c1*T_s^4 - 2*c1*T(i)^4 - c1^5*(T_s^4 - T(i)^4)^4
# how the fuck does one backsolve this?
# i mean i guess if we use large step sizes then it's easy. like if we consider +1 = 10 mins then we only need two steps and T(i+2) is our solution to backsolve from.
T(i+2) = (75+273) = (-15+273) + 2*c1*(215+273)^4 - 2*c1*(-15+273)^4 - c1^5*((215+273)^4 - (-15+273)^4)^4
#c1 = 8.60754x10^-10 or 1.06499x10^-8 (idk which root to pick?, why are there two?)
# the units of this c1 are "very" different then of the c1 above. still sketchy though. 
# ohhhh did i 1/c1 accidentally somewhere?

# ohhh but with big step sizes we lose the ability to find a precise temperature for the colder version.
# based on previous approximations we should hit in ther range of T(i+4.5)







#### Everything below this didn't work out. Mostly complex-valued solutions not worth the time. There used to be a lot more, but this bit seems fine. Did a bunch in Celcius *facepalm* but it still didn't work out in Kelvin. 

# For radiation heat transfer
dQ/dt = const * (Toven^4 - T^4)
dU = dQ/dt = Cv * dT/dt
Cv*dT/dt = const* (Toven^4 - T^4)
dT/(Toven^4 - T^4) = const * dt
integral(dT/(Toven^4 - T^4)) = c1*t + c2

let Toven^4 = r

#wolfram solve. alternate form w/ r > 0 and t > 0
#https://www.wolframalpha.com/input/?i=integral+of+dt%2F%28a+-+t%5E4%29

Then solve: 
(atan(T/r^(1/4)) + atanh(T/r^(1/4)))/(2*r^(3/4)) = c1*t + c2

Okay so plug in known values: T(0) = -15. T(r(215^4), t = 20) = 75
Then solve for c1 and c2. and we should be able to find the heating profile for the oven at r=150^4



okay so T(t=0) = -15, r = 215^4 ### oh but this solution was only good t > 0
(atan(-15/215) + atanh(-15/215))/(2*215^(3/4)) = c1*0 + c2 = c2
c2 ~ 0.001242585

okay so T(t=0) = 258, r = 473^4 # what if in kelvin. 
(atan(T/r^(1/4)) + atanh(T/r^(1/4)))/(2*r^(3/4)) = c1*t + c2
(atan(258/473^(1/4)) + atanh(258/473^(1/4)))/(2*473^(3/4)) = c2
c2 is complex-valued. 


okay so T(t=20) = 75, r = 215^4
(atan(75/215^(1/4)) + atanh(75/215^(1/4)))/(2*215^(3/4)) = c1*20 + 0.001242585
c1 is complex-valued... 0.000637319 - 0.000699409 i


## above couple lines are nonsense. screwed up approximation requirements. 
Then solve: 
(-log(r^(1/4) - T) + log(r^(1/4) + T) + 2*atan(T/(r^(1/4))))/(4*r^(3/4)) = c1*t + c2

okay so T(t=0) = -15, r = 215^4 ### oh but this solution was only good t > 0
(-log(215^(1/4) + 15) + log(215^(1/4) - 15) + 2*atan(-15/(215^(1/4))))/(4*215^(3/4)) = c2
c2 is complex. fack.

#switch to kelvin? 273.15K = 0C. dude. kelvin has always been a requirement. fack. 
okay so T(t=0) = 258 r = 473.
(-log(473^(1/4) - 258) + log(473^(1/4) + 258) + 2*atan(258/(473^(1/4))))/(4*473^(3/4)) = c2
c2 still imaginary. lolz. fuck. 


