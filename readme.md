# N-body Simulation

How to use command line input

`python3 main.py PATH/SYSTEM.json`


Package dependencies
- `matplotlib`
- `numpy`
- `scipy`

Note: closing the 'Error in Hamiltonian' window, speeds up the animation.


#### Interesting systems
- `sims/system-1.json`
- `sims/tests/ahhhh-shiny-asteroids.json`
- `sims/tests/classic4l-atom.json` (long time dynamics is unstable! [accumulation of numerical errors] )
- `sims/tests/pythagoras.json`
- `sims/3-body/triangle-2-3-crazy.json`
- `sims/3-body/figure-8.json` ([R Montgomery](#N-Body-Exact-Solutions))


#### Purpose of Simulation
- Compare the accuracy of different numerical integration schemes
- Chaotic nature of the 3-body problem
- Visualisation of non-integrable orbits
- Ray tracing the dynamical system using "ghost" (non-interacting) bodies
- Scattering from close encounter orbits
- Statistical/out-of-equilibirum behaviour of large $`N`$-body systems (ie structure formation)


#### To investigate
- Stability of orbits  (linear stability & non-linear stability)



---


## Reading & Exporting the Simulation

**Input**: .json file

**Output**: (optional) .csv of time series of the position of each body (separate file) in a new directory





## JSON File Input

###### Example
```json
{
	"bodies": [
			{
			"name": "earth",
			"x0": [100,0],
			"v0": [0,2],
			"mass": 1,
			"colour": "green"
		},
		{
			"name": "sun",
			"x0": [0,0],
			"v0": [0,0],
			"mass": 1000,
			"colour": "yellow"
		}
	],
	"dim": 2,
	"physics": "gravity",
	"tfin": 1000,
	"max dt": 0.1,
	"plot dt": 0.5,
}
```

- [ ] which keywords are essential and which are optional?



### Key words


#### Bodies

- `"name"`: the name of the body
- `"mass"`
- `"colour"`: the colour used to plot / label the dynamical trajectory - uses matplotlib colours. See: [matplotlib colours](https://matplotlib.org/stable/gallery/color/named_colors.html)
- `"x0"`: the initial position, as a d-dim vector. Eg [0,1,2]
- `"v0"`: initial velocity, d-dim vector.
- `"type"`: used to construct the body. Options: `"random"`
- `"charge"`: electrostatic charge.



##### Ghosts & Statics

- `"ghost"`: feels the 'force' from other particles, but does not exert any influence on others.  In newtonian gravity, this is the limiting behaviour of a 'massless' particle.
- `"static"`: does not feel the 'force' of other particles but does exert a foce.  Think of this as a 'source' tern.

"static" & "ghost" terms are turned on by being `true`. They may be put into different classes & these are distinguished via string labels.
"static" objects in the same class do not interact with one another, but do interact with static objects in another class
"ghost" objects do not interact with ghosts in the same class, but interact with other ghosts in a different class.

"ghosts" allow for the dynamical system to be ray traced (if one wishes).


##### Random

Samples bodies uniformly randomly.

- `"num"`: number of bodies to populate
- `"r max"`: maximum radius
- `"v max"`: maximum velocity
- `"mass var"`: variance of mass +- about 'mass' value
- `"charge var"`: variance of charge +- about 'charge' value


#### General

- `"dim"`: number of dimensions of position/velocity/momentum vectors.
- `"tfin"`: Simulation time duration. ie the ending time of the simulation
- `"citation"`: unused key-word.  Record of sources


##### Visuals

- `"frame"`: how to centre the plotting. Options: COM, zero, name of a body
	- `"COM"`: centre of mass frame
- `"trail len"`: length of trails behind the moving bodies.  If negative, then has infinite length.
- `"plot dt"`: time between frames (using simulation time, not real time). Motion of particles from simulation output (generically) does not have equal spacing in time. This results in unphysical slow-down and speed up if (x,y) is naively plotting.  "plot dt" is the time spacing used to interpolate the dynamical coordinates, so to make the plotting smooth.
- `"equal ratio"`: if true, make the coordinate ratio of xs & ys the same
- `"max plot radius"`: maximum distance from the (frame) origin to plot. ie if bodies leave the ball with this radius, do not plot them.
- `"plot Hamiltonian"`: if true, animate how the Hamiltonian changes over the duration of the simulation.

##### Numerical Solver

- `"max dt"`: the maximum allowed time step to be used in the integrator
- `"method"`: which numerical solver to use to solve the ODEs
- `"atol"`: Default: `1e-6`. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html for an explanation
- `"rtol"`: Default: `1e-3`



##### Physics

- `"physics"`: says what hamiltonian to use. Implemented: Gravity, Electrostatics, & Gravity+Electrostatics
- `"grav power law"`: the powerlaw of the gravitational force
- `"electro power law"`: the powerlaw of the electrostatic force


###### Types of Physics

- `"gravity"`
- `"electrostatics"`
- `"gravo-electro"`


## Physics / Hamiltonian

The dynamical system is modelled by a set of (differential) equations of motion (EOM).
These EOM are generated from the Hamiltonian $`H`$ and are Hamilton's equations $`\frac{dx}{dt} = \frac{\partial H}{\partial p}`$ and $`\frac{dp}{dt} = -\frac{\partial H}{\partial x}`$.


### N-Body Problem (central potential dynamics)

The physics modelled is the Euclidean $`N`$-body central potential system.
This has Hamiltonian $`H = T+V`$, where $`T = p^2/(2m)`$ is the standard 'Euclidean' kinetic energy and $`V`$ is the central potential.

$$V = \sum_{i=1}^N\sum_{j>i} \frac{g_{ij}}{r_{ij}}$$

Where, $`g_{ij}`$ is the coupling strength between bodies $`i`$ & $`j`$, and $`r_{ij} = \lVert x_{i}- x_j \rVert`$ is the distance.

###### Examples
- Newtonian gravity: $`g_{ij} = -Gm_im_j`$
- Electrostatics / Coloumb: $`g_{ij} = k_0 q_iq_j`$
- Hooke's Law / Spring: $`g_{ij} = \frac{1}{2}k_{ij}`$ (but power law $`r^{-2}`$).


#### 2-Body Dyanmics

The 2-body problem is completely integrable and hence allows for the direct comparison between the analytical solutions and numerical solutions.
The the system may be reduced to two independent 1-body problems, each orbitting about the centre of mass (COM) of the system (eg see [notes](https://www.physics.usu.edu/torre/6010_Fall_2016/Lectures/06.pdf)).
The four integrals of motion are the Hamiltonian (energy), the angular momenta of the 2-bodies and total linear momentum.

##### TODO:
- check (!) what are the four integrals?
- can any 2-body central potential system be redueced to two independent central potential systems about the COM.


##### Gravity
For gravity the 1-body problem (Kepler problem), the orbits form conic sections.
In systems with low eneough energy, this manifests as elliptic orbits (as evident in the solar system).


#### 3-Body Dyanmics

##### Planar initial Conditions

If the initial velocities/momenta are all zero, then the problem may be reduced to two dimensions - ie the motion all occurs on a plane.

[makes the problem more integrable?]


## Simulation


The implemented Hamiltonins are `gravity`, `electrostatics`, and `gravity + electrostatics`.


The dynamics of the system is simulated by numerically solving the (differential) equations of motion (Hamilton's equations).



### Numerical Solvers


The equations are solved using a higher order Runge-kutta integrator.  
Ideally, this should be changed to a sympletic integrator.  I believe scipy does not have one, so many need to use an external package or manually code it.


###### Runge Kutta

Solves the 1st order ODE
$` \frac{dy}{dt} = f(t,y) `$.
See [scipy implementations](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html)


###### Symplectic Integrators

[Geneva Lecture Notes](https://www.unige.ch/~hairer/poly_geoint/week2.pdf)

External Packages:
- [pyHamSys](https://pypi.org/project/pyhamsys/)
- [REBOUND](https://rebound.readthedocs.io/en/latest/ipython_examples/HighOrderSymplectic/)



### Algorithmic Complexity

Computing $`V_{ij}`$ for $`N`$ bodies scales as $`N(N-1)/2`$.



### Numerical Accuracy


##### Conserved Quantities

- The Hamiltonian should be conserved throughout the simulation, but it is (generically) not. In the 2-body problem (most) orbits do indeed form ellipses, and this naively suggests the simulation may be accurate. 
- However, during the simulation the Hamiltonian varies at an O(1)-O(100) order. In fact, the Hamiltonian is periodic (hence enabling the orbits to return to their initial positions). It is unclear why the variance is so large and why numerical errors cancel out and cause the Hamiltonian to be periodic.


##### Chaos

The chaotic nature of the $`N`$-body ($`N>2`$) problem manifests by even adjusting the (maximum) integration timestep.
Improving the time-step accuracy results in wildly different orbits.
Different time-steps results in different increments of positions, which will exponentially diverge.


##### Bounded Orbits

There exist configurations (initial velocities are zero) for which the orbits should be bounded for all time. This is imposed by conservation of the Hamiltonian (energy).
[which configurations are these?]
However, generically, the long time behaviour is that the bodies will 'shoot' off to infinity.  This occurs due to an accumulation of numerical errors, and that the Hamiltonian not being conserved.




###### Question:

As the integration time-step goes to zero (ie continuous limit) does the orbit of motion converge to the "true" orbit?
If the orbits do not converge, then we have an epistemic problem: can we know what the true (continuous) classical orbit is?



#### Notes

Some trajectories look like bounces/collisions when two bodies come close together.  However, if one zooms in, they in fact do not touch but have orbits that pass through one another in a parabolic like shape.
Though, in the infinitessimal limit `max dt` $`\to 0`$, the two bodies will collide.  Unclear how to make sense of this.
Scattering is thus a natural phenomenom and is not hard coded.





## Analysis

> Post simulation analysis.



## Animation

Implemented using Matploblib.


###### How are the x,y limits chosen?
If one of the limits are zero, then set `= 0.1 * (x_max-x_min)` [I've changed this - TODO: need to fix & unit test]



#### Reference Frames

The Centre of Momentum frame only makes sense for 'Euclidean' momentum conserving Hamiltonians.
$`x_{\text{com}} = (\sum_i m_i x_i ) / (\sum_i m_i)`$.
Since, the numerator is the sum of Euclidean momenta.


#### Error in Hamiltonian

The Hamiltonian of this system is a conserved quantity (call energy) - hence expect it to be constant throughout the simulation.
However, numerical errors means this is (generically) not so.

This plots the difference between the Hamiltonian H0 at t=0, and H(p(t),q(t)).

For systems with static or ghost bodies, energy may not be conserved.
Total momentum is not conserved from scattering interactions - both bodies should recoil, but only one does.
In this case, this plots how the energy changes from (non-conserving) scattering.


#### Interpolation of coordinates

The output of the numerical solver results in `(y,t)`. Generically, the time-step increments (of `t`) are not constant, ie $`t_{i+1}-t_{i} \neq t_{j+1}-t_{j}`$, where $`i\neq j`$.
Hence, in order for the elements in the coordinate array `y` to advance with constant time increments, `y` must be interpolated.
The `"plot dt"` parameter in the `.json` file sets the interpolated time increment step.
This enables the animation to appear more smooth (smaller dt), or sped up (larger dt).

Though, larger `"plot dt"` causes the animation to appear discontinuous/kinked.
This is apparent in close-encounter orbits. The planet may appear to NOT go around the sun - this is an artefact of interpolation.



## Automatic Generation of Bodies

### `"type": "random"`

Parameters are uniformly sampled between min & max values.



## Organisation of the Code


###### Sequence
>- Read input
>- pre-process
>- Simulation
>- post-process
>- animate
>- write output

Simulation depends on "physics" (Hamiltonian), "system", and "numerical integrator".


###### Class Heirarchy of the dynamical systems:
>- `DynamicalSystem`
>     - `Hamiltonian`
>		   - `CentralPotential`
>			   - `Gravity`
>			   - `ElectroStatics`
>			   - `GravoElectro`

In principle, the code may be extended to include non-hamiltonian systems.


###### Objects
> - `DynamicalSystem` - defines the EoM to solve.
> - `NumericalIntegrator` - defines the numerical scheme used to solve the EoM.
> - `System` - collection of `Body` objects, and variables used to input into the dynamical system.
> - `Body` - collection of parameters/constants defining the properties of a body (eg mass, charge)
> - `Graphics` - collection of parameters describing how to process & plot the data post simulation.


###### Misc helper functions
> - `arrays` - flattening and bundling lists (eg into vectors)
> - `vector` - computations such as inner-product and norm.  A 'vector' is just a numpy 1d array.



## TODOS
- [ ] command line input for reading and writing
- [x] implement the Hamiltonian (energy) function for the (euclidean) central potential. Use to check how well/poorly energy is conserved over the timespan of the simulation.
- [ ] Code in more exceptions / error cases.
- [ ] Speed up / optimise.  Will need to investigate where the bottlenecks are.
- [ ] Figure out how to speed up the flatten and bundle functions.
- [ ] Implement an alternate dp_dt central potential function - remove the bundle & flatten functions.
- [ ] Write the code to work with 1-dimensional bodies, and 1 body.
- [ ] Symplectic Integrator option
- [ ] `Simulation` object, which holds the DynamicalSystem, NumericalIntegrator, and System. [feels as if System and DynamicalSystem should be the same object]. Simulation should hold the dynamical time evolution of $`(x,p)`$.
- [ ] The orbit & Hamiltonian-error animations appear to be out of sync. (delay between close-encounter orbits & spikes in the Hamiltonian-error) Fix it!


#### Mid priority
- [ ] Spring law Hamiltonian
- [ ] Option to control animation speed.
- [ ] JSON: polar coordinates as a way to construct vectors  (distinguished from Cartessian vectors)
- [ ] Lattices (ie for loops)
- [ ] Test to ensure no two bodies are placed in the same location. Results in infinite force/energy


#### Low priority
- [ ] polynomial gravity: sum of power-law gravities. Specify powers & coefficients as arrays. eg pows=[1,2], coeffs=[1,2] for V=1/r^1 + 2/r^2
- [ ] Have colour of `random`-type bodies correspond to the amount of charge & mass.
- [ ] Uniform gravitational field. eg electrostatics in a uniform down gravitational field
- [ ] (Hard) Boundaries. eg particles in a box.


### Animations
- [ ] Allow `"plot dt"` to be large, but have smooth orbit curves. ie if `y = [0,1,2,3,4,5,6]` and `t = [0,0.5,1,1.5,2,2.5,3]` and `"plot dt"`=1, then plot `y0=[0]`, `y1=[0,1,2]`, `y2=[0,1,2,3,4]` etc as the discrete time steps.
- Currently: have that if `plot dt`=1, then plot `y0=[0]`, `y1=[0,2]`, `y2=[0,2,4]`, which clearly introduces 'sharp' discontinuous artefacts.
- [ ] Plot the lines as slightly more opaque than the circle markers
- [ ] Option to directly export the orbit animation to .mp4
- [ ] Thinner lines for faster velocities (?)



### (Soft) Collisions
- [ ] 'Regularise' the dynamics for orbits that closely approach another (massive) body. See `close-encounter.json` file. This is a 2-body problem so orbit should be static ellipse, but it is not.

One idea is to give the bodies a finite size (ie radius), so that they do not come too close to one another.
However, this will require collisions (between the finite bodies) to be hard coded.
Will have to modify the equations of motion, and or use a custom integrator.


### Speeding up the Simulation

???


### Speeding up the Animation

??? 

Plot less frames?


### Hard TODOS
- [ ] Toric (pacman) boundary conditions.  Important: geodesics may be connected by passing through the boundary - so will need to find the radial distance 3 times. Then take the minimum (?)
- [ ] Regularise head on collisions.  Unclear how to implement numerically without using different equations of motion.  Can this be achieved without compleletely rewriting the code?



## Related Projects
- [REBOUND](https://rebound.readthedocs.io/en/latest/)
- [Three-Body Problem Simulation](https://www.youtube.com/watch?v=cev3g826iIQ)
- [3 Body Problem - Periodic Solutions](https://github.com/mws262/MAE5730_examples/tree/master/3BodySolutions) (surprisingly very simple code)
	


## Further References: Related Videos, Essays, and Articles


### Webpages

- [Bob Jenkins](https://burtleburtle.net/bob/index.html)
	- [Toruses and Dyson Swarms](https://burtleburtle.net/bob/scifi/dyson.html)
	- [Multistep Methods for the N-Body Problem](https://burtleburtle.net/bob/math/multistep.html) (numerical methods for solving the ODE)
	- [Figure Eight Orbits](https://burtleburtle.net/bob/physics/eight.html)
	- [JavaScript Source Code](https://burtleburtle.net/bob/js/orbit.js)
	- [Klemperer Rosettes](https://burtleburtle.net/bob/physics/kempler.html)
	- [Orbits](https://burtleburtle.net/bob/physics/index.html)


### Videos

- [Chaos and Physics Simulations](https://www.youtube.com/watch?v=-nbTrPwQudo)
- [Chaos and the 3-Body Problem](https://www.youtube.com/watch?v=-nbTrPwQudo)
- [3 Body Problem - Periodic Solutions](https://www.youtube.com/watch?v=8_RRZcqBEAc) (beautiful solutions & orbits)
- [Physics Simulations](https://www.youtube.com/@physicssimulations7518/videos) (YouTube)
	- [N-Body Problem Simulation with 5 Free Masses | Gravity | Physics Simulations](https://www.youtube.com/watch?v=Lbkr5C1i4Uo)



### Articles

##### N-Body Exact Solutions
- [Figure Eight Obrit](https://webhomes.maths.ed.ac.uk/~ateckent/vacation_reports/Report_Faustino.pdf)
- [Braids in Classical Dynamics](https://sites.santafe.edu/~moore/braids-prl.pdf) (1993: Moore)
- [N-Body Choreography](https://en.wikipedia.org/wiki/N-body_choreography)
- [A remarkable periodic solution of the three-body problem in the case of equal masses](https://arxiv.org/abs/math/0011268) (2000: Chenciner, & Montgomery)



##### Relativistic N-body

- [Post-Minkowskian closed-form Hamiltonian for gravitating N-body systems](https://arxiv.org/abs/1003.0561) (N-body Hamiltonian of relativistic particles, post-Minkowsian limit of General Relativity)
- [Post-Minkowskian approximation](https://arxiv.org/pdf/0807.0214) (2008: Ledvinka, Schaefer, & Bicak)



### Lecture Notes

##### Numerical Integrators
- [Ernst Hairer's Numerical Integration book](https://www.unige.ch/~hairer/polycop.html)


## Literature

---
