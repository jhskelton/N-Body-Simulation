# N-body Simulation

How to use command line input

`python3 main.py PATH/SYSTEM.json`



## JSON File Input

- [ ] give an example
- [ ] which keywords are essential and which are optional?


### Key words


#### Bodies

- "name": the name of the body
- "mass"
- "colour": the colour used to plot / label the dynamical trajectory - uses matplotlib colours. See: [matplotlib colours](https://matplotlib.org/stable/gallery/color/named_colors.html)
- "x0": the initial position, as a d-dim vector. Eg [0,1,2]
- "v0": initial velocity, d-dim vector.
- "type": used to construct the body. See: "random" (no others implemented)
- "charge": electrostatic charge.



##### Ghosts & Statics

- "ghost": feels the 'force' from other particles, but does not exert any influence on others.  In newtonian gravity, this is the limiting behaviour of a 'massless' particle.
- "static": does not feel the 'force' of other particles but does exert a foce.  Think of this as a 'source' tern.

"static" & "ghost" terms are turned on by being `true`. They may be put into different classes & these are distinguished via string labels.
"static" objects in the same class do not interact with one another, but do interact with static objects in another class
"ghost" objects do not interact with ghosts in the same class, but interact with other ghosts in a different class.

"ghosts" allow for the dynamical system to be ray traced (if one wishes).


##### Random

Samples bodies uniformly randomly.

- "num": number of bodies to populate
- "r max": maximum radius
- "v max": maximum velocity
- "mass var": variance of mass +- about 'mass' value
- "charge var": variance of charge +- about 'charge' value


#### General

- "dim": number of dimensions of position/velocity/momentum vectors.
- "tfin": Simulation time duration. ie the ending time of the simulation


##### Visuals

- "frame": how to centre the plotting. Options: COM, zero, name of a body
	- "COM": centre of mass frame
- "trail len": length of trails behind the moving bodies.  If negative, then has infinite length.
- "dt": time between frames (using simulation time, not real time). Motion of particles from simulation output (generically) does not have equal spacing in time. This results in unphysical slow-down and speed up if (x,y) is naively plotting.  "dt" is the time spacing used to interpolate the dynamical coordinates, so to make the plotting smooth.
- "equal ratio": if true, make the coordinate ratio of xs & ys the same
- "max radius": maximum distance from the (frame) origin to plot. ie if bodies leave the ball with this radius, do not plot them.
- "plot Hamiltonian": if true, animate how the Hamiltonian changes over the duration of the simulation.

##### Numerical Solver

- "max dt": the maximum allowed time step to be used in the integrator
- "method": which numerical solver to use to solve the ODEs
- "atol": Default: 1e-6. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html for an explanation
- "rtol": Default: 1e-3



##### Physics

- "physics": says what hamiltonian to use. Implemented: Gravity, Electrostatics, & Gravity+Electrostatics
- "grav power law": the powerlaw of the gravitational force
- "electro power law": the powerlaw of the electrostatic force



## Reading & Exporting the Simulation



## Physics / Hamiltonian

The dynamical system is modelled by a set of (differential) equations of motion (EOM).
These EOM are generated from the Hamiltonian $`H`$ and are Hamilton's equations $`\frac{dx}{dt} = \frac{\partial H}{\partial p}`$ and $`\frac{dp}{dt} = -\frac{\partial H}{\partial x}`$.


The physics modelled is the Euclidean $`N`$-body central potential system.
This has Hamiltonian $`H = T+V`$, where $`T = p^2/(2m)`$ is the standard 'Euclidean' kinetic energy and $`V`$ is the central potential.

$$V = \sum_{i}^N\sum_{j>i} \frac{g_{ij}}{r_{ij}}$$

$`g_{ij}`$ is the coupling strength between bodies $`i`$ & $`j`$, and $`r_{ij} = \lVert x_{i}- x_j \rVert`$


## Simulation


The implemented Hamiltonins are `gravity`, `electrostatics`, and `gravity + electrostatics`. These are using standard 'euclidean' momentum ie .


Class Heirarchy in the code:
>- DynamicalSystem
>     - Hamiltonian
>		   - CentralPotential
>			   - Gravity
>			   - ElectroStatics
>			   - GravoElectro

In principle, the code may be extended to include non-hamiltonian systems.


The dynamics of the system is simulated by numerically solving the (differential) equations of motion.  
These equations are analytically generated from the Hamiltonian $`H`$ 


### Numerical Solvers


Currently, the equations are being solved using a higher order Runge-kutta integrator.  
Should change to a sympletic integrator.  I believe scipy does not have one, so many need to use an external package or manually code it.

###### Runge Kutta


###### Symplectic Integrators

[Geneva Lecture Notes](https://www.unige.ch/~hairer/poly_geoint/week2.pdf)



#### Numerical Accuracy



### Notes


Some trajectories look like bounces/collisions when two bodies come close together.  However, if one zooms in, they in fact do not touch but have orbits that pass through one another in a parabolic like shape.
Though, in the infinitessimal limit max_dt -> 0, the two bodies will collide.  Unclear how to make sense of this.
Scattering is thus a natural phenomenom and is not hard coded.





## Animation

Implemented using Matploblib.


###### How are the x,y limits chosen?
If one of the limits are zero, then set = 0.1 \* (x_\max-x_\min)



#### Reference Frames

The Centre of Momentum frame only makes sense for 'Euclidean' momentum conserving Hamiltonians.
x_com = (\sum_\i m_\i*\x_\i ) / (\sum_\i m_\i).
Since, the numerator is the sum of Euclidean momenta.

#### Error in Hamiltonian

The Hamiltonian of this system is a conserved quantity (call energy) - hence expect it to be constant throughout the simulation.
However, numerical errors means this is (generically) not so.

This plots the difference between the Hamiltonian H0 at t=0, and H(p(t),q(t)).

For systems with static or ghost bodies, energy not be conserved.
Total momentum is not conserved from scattering interactions - both bodies should recoil, but only one does.
In this case, this plots how the energy changes from (non-conserving) scattering.


## TODOS
- [ ] command line input for reading and writing
- [x] implement the Hamiltonian (energy) function for the (euclidean) central potential. Use to check how well/poorly energy is conserved over the timespan of the simulation.
- [ ] unit-test electrostatics
- [ ] Code in more exceptions / error cases.
- [ ] Speed up / optimise.  Will need to investigate where the bottlenecks are.
- [ ] Figure out how to speed up the flatten and bundle functions.
- [ ] Implement an alternate dp_dt central potential function - remove the bundle & flatten functions.
- [ ] Write the code to work with 1-dimensional bodies, and 1 body.
- [ ] Symplectic Integrator option


### Mid priority
- [ ] Spring law Hamiltonian
- [ ] Option to control animation speed.
- [ ] JSON: polar coordinates as a way to construct vectors  (distinguished from Cartessian vectors)
- [ ] Lattices (ie for loops)
- [ ] Test to ensure no two bodies are placed in the same location. Results in infinite force/energy


### Low priority
- [ ] polynomial gravity: sum of power-law gravities. Specify powers & coefficients as arrays. eg pows=[1,2], coeffs=[1,2] for V=1/r^1 + 2/r^2
- [ ] Have colour of `random`-type bodies correspond to the amount of charge & mass.
- [ ] Uniform gravitational field. eg electrostatics in a uniform down gravitational field
- [ ] (Hard) Boundaries. eg particles in a box.


## (Soft) Collisions
- [ ] 'Regularise' the dynamics for orbits that closely approach another (massive) body. See `close-encounter.json` file. This is a 2-body problem so orbit should be static ellipse, but it is not.

One idea is to give the bodies a finite size (ie radius), so that they do not come too close to one another.
However, this will require collisions (between the finite bodies) to be hard coded.
Will have to modify the equations of motion, and or use a custom integrator.


## Hard TODOS
- [ ] Toric (pacman) boundary conditions.  Important: geodesics may be connected by passing through the boundary - so will need to find the radial distance 3 times. Then take the minimum (?)
- [ ] Regularise head on collisions.  Unclear how to implement numerically without using different equations of motion.  Can this be achieved without compleletely rewriting the code?

