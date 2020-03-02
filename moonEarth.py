import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.collections import LineCollection
import matplotlib.colors

#import scipy.integrate
class body():
    def __init__(self,mass, r, v, name, colour):
        self.mass = mass
        self.r = r
        self.v = v
        self.name = name
        self.colour = colour
#iterates one timestep for a single body
def RK4step(a, r, v, h):
    v = v + h*a
    r = r + v*h
    return r,v

def acceleration(r1,r2,mass):
    r = r1-r2
    a = G*mass*(r)/np.linalg.norm(r)**3
    
    return a

def RK4step2(moon, ship, earth, h):
    #k step one
    k1ShipV = acceleration(moon.r,ship.r,moon.mass)+acceleration(earth.r,ship.r,earth.mass)
    k1MoonV = acceleration(earth.r,moon.r,earth.mass)
    k1ShipR = ship.v
    k1MoonR = moon.v
    
    #k step two
    k2ShipV = acceleration(moon.r+h/2*k1MoonR,ship.r+h/2*k1ShipR,moon.mass)+acceleration(earth.r,ship.r+h/2*k1ShipR,earth.mass)
    k2MoonV = acceleration(earth.r,moon.r+h/2*k1MoonR,earth.mass)
    k2ShipR = ship.v+h/2*k1ShipV
    k2MoonR = moon.v+h/2*k1MoonV
    
    #k step three
    k3ShipV = acceleration(moon.r+h/2*k2MoonR,ship.r+h/2*k2ShipR,moon.mass)+acceleration(earth.r,ship.r+h/2*k2ShipR,earth.mass)
    k3MoonV = acceleration(earth.r,moon.r+h/2*k2MoonR,earth.mass)
    k3ShipR = ship.v+h/2*k1ShipV
    k3MoonR = moon.v+h/2*k1MoonV
    
    #k step four
    k4ShipV = acceleration(moon.r+h*k3MoonR,ship.r+h*k3ShipR,moon.mass)+acceleration(earth.r,ship.r+h*k3ShipR,earth.mass)
    k4MoonV = acceleration(earth.r,moon.r+h*k3MoonR,earth.mass)
    k4ShipR = ship.v+h*k1ShipV
    k4MoonR = moon.v+h*k1MoonV
    
    weights = np.array([1,2,2,1])
    #timestep
    ship.v = ship.v + h/6*(k1ShipV+2*k2ShipV+2*k3ShipV+k4ShipV)
    ship.r = ship.r + h/6*(k1ShipR+2*k2ShipR+2*k3ShipR+k4ShipR)
    
    moon.v = moon.v + h/6*(k1MoonV+2*k2MoonV+2*k3MoonV+k4MoonV)
    moon.r = moon.r + h/6*(k1MoonR+2*k2MoonR+2*k3MoonR+k4MoonR)
    return moon,ship

#finds CoM of two bodies
def CoM(bodyOne,bodyTwo):
    massTotal = bodyOne.mass + bodyTwo.mass
    CoM = (bodyOne.r*bodyOne.mass+bodyTwo.r*bodyTwo.mass)/massTotal
    return CoM

def moveRefFrame(centreBody,bodyTwo,bodyThree):
    newOrigin = centreBody
    bodyOne = np.array([0,0])
    bodyTwo = bodyTwo - newOrigin
    bodyThree = bodyThree - newOrigin
    return bodyOne, bodyTwo, bodyThree

def createColMap(colour):
    colOne = (matplotlib.colors.to_rgb(colour) + (0,0))[:4]
    colTwo = (matplotlib.colors.to_rgb(colour) + (1,0))[:4]
    return matplotlib.colors.LinearSegmentedColormap.from_list("Ship", [colOne,colTwo])

def setupPlot():
    fig, ax = plt.subplots()
    ax.set_xlim((-25,25))
    ax.set_ylim((-25,25))
    ax.set_aspect("equal")
    particles = np.empty([3,1])
    
    norm = plt.Normalize(0,150)
    
    cmapShip = createColMap(ship.colour)
    cmapMoon = createColMap(moon.colour)

    lcShip = LineCollection([], cmap=cmapShip, norm=norm)
    ax.add_collection(lcShip)

    lcMoon = LineCollection([], cmap=cmapMoon, norm=norm)
    ax.add_collection(lcMoon)
    
    shipLine, = ax.plot([],[], ship.colour)
    moonLine, = ax.plot([],[], moon.colour)
    plotsArray = []
    for i in bodies:
        piece, = ax.plot([], [], "{}o".format(i.colour), ms = i.mass**(1/3)*25, label = i.name)
        plotsArray.append(piece,)
    
    return fig, ax, plotsArray, shipLine, moonLine, lcShip, lcMoon,
def updateTail(lc,x,y,colMapArray):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    lc.set_segments(segments)
    lc.set_array(colMapArray)
    return lc,

#set up animation
def init():
    
    #particles.set_data([], [])
    shipLine.set_data([], [])
    moonLine.set_data([], [])
    
    lcShip.set_segments([])
    lcMoon.set_segments([])
    for i in plotsArray:
        i.set_data([], [])
    return plotsArray, shipLine, moonLine, lcShip, lcMoon,

#update plot
def animate(i):
    subSteps = 100
    #gross FIX!?
    global moon
    global earth
    global ship
    global movingBodyTails
    global lcShip
    global lcMoon
    for k in range(subSteps):
        moon, ship = RK4step2(moon, ship, earth, h)
    
    followCoM = False
    followMoon = False
    
    shipPosX.append(ship.r[0])
    shipPosY.append(ship.r[1])
    moonPosX.append(moon.r[0])
    moonPosY.append(moon.r[1])

    movingBodyTails = np.append(movingBodyTails, [[ship.r[0]], [ship.r[1]], [moon.r[0]], [moon.r[1]]], axis = 1)


    if len(movingBodyTails[1,:]) > 150:
        movingBodyTails = movingBodyTails[:,1:]
        colMapArray = np.arange(0,150)
    else:
        colMapArray = np.arange(0,150)[-i:]
    
    lcShip, = updateTail(lcShip,movingBodyTails[0,:], movingBodyTails[1,:],colMapArray)
    lcMoon, = updateTail(lcMoon,movingBodyTails[2,:], movingBodyTails[3,:],colMapArray)    
    """
    pointsMoon = np.array([movingBodyTails[2,:], movingBodyTails[3,:]]).T.reshape(-1, 1, 2)
    segmentsMoon = np.concatenate([pointsMoon[:-1], pointsMoon[1:]], axis=1)
    lcMoon.set_segments(segmentsMoon)
    lcMoon.set_array(colMapArray)
    """
    #moonLine.set_data(movingBodyTails[2,:], movingBodyTails[3,:])
    
    for j in range(len(bodies)):
        plotsArray[j].set_data(bodies[j].r[0], bodies[j].r[1])
    
    if followCoM == True:
        centre = CoM(earth,moon)
    else:
        centre = [0,0]
    ax.set_xlim(-25+centre[0],25+centre[0])
    ax.set_ylim(-25+centre[1],25+centre[1])
    return plotsArray, shipLine, moonLine, lcShip, lcMoon,
    

#gravitational system setup
earth = body(1,np.array([0,0]),np.array([0,0]),"Earth", "b")
ship = body(0.0001,np.array([0,10]),np.array([-0.2,0]),"Ship", "g")
moon = body(0.1,np.array([20,0]),np.array([0,0.2]),"Moon", "r")   
bodies = [earth,ship,moon]
h = 0.01
G = 1
ms = 10
movingBodyTails = np.array([[ship.r[0]], [ship.r[1]], [moon.r[0]], [moon.r[1]]])

shipPosX = []
shipPosY = []
moonPosX = []
moonPosY = []
fig, ax, plotsArray, shipLine, moonLine, lcShip, lcMoon, = setupPlot()
#call animation
ax.set_facecolor((0, 0, 0))
ani = animation.FuncAnimation(fig, animate, frames=600,
                              interval=1,  init_func=init)
plt.grid()
plt.show()
