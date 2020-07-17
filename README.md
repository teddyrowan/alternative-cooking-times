# Alternative Cooking Times

This set of scripts aims to calculate alternative cooking times for people who want to use their oven at temperatures other than the recommended value in recipes. It assumes all heat transfer by radiation (note: the answers will not be accurate for convection ovens), that the change in blackbody coefficient for the oven between the two different cooking temperatures is negligible, and that the main value of interest is total heat transferred into the food that is being cooked. 

The package uses Euler's Method... 

### Usage Example

Blebber blab blob


### Walking through the algorithm 

The Governing Equation:

```
dQ/dt = m*Cv*(dT) = a*(Ts^4 - T^4)
```

This differential equation unfortunately doesn't have a particularly clean solution. So let's use Euler's Method and find a numerical approximation to the solution.


```
dQ/dT(n) = m*Cv*(T(n+1) - T(n)) = a*(Ts^4 - T(n)^4)
```

Grouping constants and re-arranging: 

```
T(n+i)  = T(n) + c1*(Ts^4 - T(n)^4)
T(n+2i) = T(n+i) + c1*(Ts^4 - T(n+i)^4)
        = T(n) + c1*(Ts^4 - T(n)^4) + c1*(Ts^4 - (T(n) + c1*(Ts^4 - T(n)^4))^4)
        = T(n) + 2*c1*Ts^4 - c1*T(n)^4 - c1*(T(n) + c1*(Ts^4 - T(n)^4))^4
```



### Author
* Teddy Rowan

