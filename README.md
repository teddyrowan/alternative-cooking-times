# Alternative Cooking Times

This set of scripts aims to calculate alternative cooking times for people who want to use their oven at temperatures other than the recommended value in recipes. It assumes all heat transfer by radiation (note: the answers will not be accurate for convection ovens), that the change in blackbody coefficient for the oven between the two different cooking temperatures is negligible, and that the main value of interest is total heat transferred into the food that is being cooked. 

The package uses Euler's Method... 

### Usage Example

Blebber blab blob

== example inline equations w/ latex renderer: https://www.codecogs.com/latex/eqneditor.php



### Walking through the algorithm 

The Governing Equation:

<img src="https://latex.codecogs.com/gif.latex?dQ/dt=mC_vdT=A\sigma(Ts^4-T^4)" title="dQ/dt=mC_vdT=A\sigma(Ts^4-T^4)" />


This differential equation unfortunately doesn't have a particularly clean solution. So let's use Euler's Method and find a numerical approximation to the solution.

Grouping constants and re-arranging: 

<img src="https://latex.codecogs.com/gif.latex?%5Cbegin%7Balign*%7D%20T%28n&plus;1i%29%20%26%3D%20T%28n%29%20&plus;%20c1*%28Ts%5E4%20-%20T%28n%29%5E4%29%20%5C%5C%20T%28n&plus;2i%29%20%26%3D%20T%28n&plus;i%29%20&plus;%20c1*%28Ts%5E4%20-%20T%28n&plus;i%29%5E4%29%20%5C%5C%20%26%3D%20T%28n%29%20&plus;%202*c1*Ts%5E4%20-%20c1*T%28n%29%5E4%20-%20c1*%28T%28n%29%20&plus;%20c1*%28Ts%5E4%20-%20T%28n%29%5E4%29%29%5E4%20%5Cend%7B%7D" title="\begin{align*} T(n+i) &= T(n) + c1*(Ts^4 - T(n)^4) \\ T(n+2i) &= T(n+i) + c1*(Ts^4 - T(n+i)^4) \\ &= T(n) + 2*c1*Ts^4 - c1*T(n)^4 - c1*(T(n) + c1*(Ts^4 - T(n)^4))^4 \end{}" />

From experience, c1 will tend to be on the order of 10^-10, so rather than solving a 5th degree polynomial, we can eliminate higher power of c1 terms and find the following approximation:

<img src="https://latex.codecogs.com/gif.latex?c1\approx1/2*\frac{T(n&plus;2i)-T(n)}{Ts^4-T(n)^4}" title="c1\approx1/2*\frac{T(n+2i)-T(n)}{Ts^4-T(n)^4}" />

Now we can use this c1 value and plug in values for the new temperature settings and step through using Euler's Method until we reach the final temperature. This method will inevitably step past the desired temperature, but we can then interpolate between the final two steps to find an approximate new cooking time. 

### Author
* Teddy Rowan

