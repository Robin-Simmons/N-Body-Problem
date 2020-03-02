# N-Body-Problem
A Python N-Body solution

## Implementation
The method implemented so far is RK4, however leapfrog integration is planned as well. The simulation works by specifying creating objects with the "body" class, which have attributes such as inital velocity, position and mass. The animation function then passes those values to a RK4 integrator which calculates the forces on each body and integrates one timestep. Multiple timesteps can be done per animation step, to allow better precision.

## TODO
The RK4 integrator only calculates forces on the "ship" due to the Moon and Earth, but not the converse. While these forces are idenital in magitude to the forces already calculated, they lead to small accelerations and so are ommited. The same is true for Moon-Earth interactions. While these are fine approximations for the report this program was written for, they are not acceptable for systems with more equal massed bodies, or for more accurate long term predicitions. Hence, the capacity for all accelerations to be calculated should be added, as well as a way to specify a "small body" attritbute when calling "body", so that its contributions to the gravitational field can be ignored for faster calculations. 


So far the program is fixed at 3 bodies. This can be increased with a rewritten integrator.
