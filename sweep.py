#importing modules
import numpy as np 
import matplotlib.pyplot as plt 
import os 
import imp

#importing lumerical's python api
os.add_dll_directory("C:\\Program Files\\Lumerical\\v202\\api\\python")
lumapi = imp.load_source("lumapi", "C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py")
import lumapi


Radii = [10e-9,25e-9,50e-9]

for i in range(len(Radii)):
    #initialising fdtd simulation
    fdtd = lumapi.FDTD();
    #setting up simulation parameters

    x = 240e-9
    y = 240e-9
    z = 240e-9

    r = float(Radii[i]) #lumeical only works on float values, either it crashes

    wl_start = 200e-9
    wl_stop = 1000e-9

    time = 500e-15
    # adding simulation area 
    fdtd.addfdtd()

    #setting the dimensions of simulation area
    fdtd.set("x",0.0)
    fdtd.set("x span", x)

    fdtd.set("y",0.0)
    fdtd.set("y span", y)

    fdtd.set("z",0.0)
    fdtd.set("z span", z)

    #simulation dimension
    fdtd.set("dimension","3D")
    fdtd.set ("simulation time", time )

    #configuring boundary conditions 
    fdtd.set("mesh type", "uniform")

    #setting yee cell size 
    fdtd.set("dx",2.5e-9)
    fdtd.set("dy",2.5e-9)
    fdtd.set("dz",2.5e-9)
    
    #adding the total field scatter field source 
    fdtd.addtfsf()
    fdtd.set("x",0.0)
    fdtd.set("x span", x-40e-9) #decreasing the size of side by 40nm

    fdtd.set("y",0.0)
    fdtd.set("y span", y-40e-9)

    fdtd.set("z",0.0)
    fdtd.set("z span", z-40e-9)

    #setting direction 
    fdtd.set("injection axis","x")
    fdtd.set("wavelength start", wl_start)
    fdtd.set("wavelength stop", wl_stop)
    
    #adding a movie monitor
    fdtd.addmovie()

    #setting dimensions for the monitor 
    fdtd.set("x",0.0)
    fdtd.set("x span", x)

    fdtd.set("y",0.0)
    fdtd.set("y span", y)
    
    #adding a simulation object 
    fdtd.addsphere()

    #setting up dimensions 
    fdtd.set("radius", r)
    fdtd.set("x",0.0)
    fdtd.set("y",0.0)

    #adding material properties
    fdtd.set("material","Au (Gold) - Johnson and Christy")

    #adding detector
    fdtd.addpower()

    #calling the monitor by name
    fdtd.set("name","DFT")
    fdtd.set("monitor type","2D Z-normal")

    fdtd.set("x span", x-40e-9) #decreasing the size of side by 40nm

    fdtd.set("y",0.0)
    fdtd.set("y span", y-40e-9)



    fdtd.setglobalmonitor("frequency points",7)
    
    #save lumerical file and run the simulation
    fdtd.save("goldSphere.fsp")
    fdtd.run()
    # getting result data
    E = fdtd.getresult("DFT","E")
    Lambda = E["lambda"]
    Lambda = Lambda[:,0] 
    
    #extracting the data of the electric field in x and y direction
    x = E["x"]
    x = x[:,0]

    y = E["y"]
    y = y[:,0]
    
    #getting only electric field values
    E = E['E']

    # E[x_axis_points, y_axis_points, z_axis_points, all_wavelengths, x_comonent_of electric_field]
    Ex = E[:,:,0,:,0] 


    # E[x_axis_points, y_axis_points, z_axis_points, all_wavelengths, y_comonent_of electric_field]
    Ey = E[:,:,0,:,1] 


    # E[x_axis_points, y_axis_points, z_axis_points, all_wavelengths, z_comonent_of electric_field]
    Ez = E[:,:,0,:,2] 
    
    # the values of these electric fields are in form of complex numbers 
    #therefore we will be changing them into normal real values
    #np.abs(Ex) gives the absolute magnitude of the complex number.
    #taking the root of the squares of magnitudes of each electric field component gives the value of the total electric field at a point in the space with x and y coordinates.
    Emag = np.sqrt(np.abs(Ex)**2 + np.abs(Ey)**2 + np.abs(Ez)**2)
    
    
    #finding the index of particular wavelenght in the dataset
    lambda_want = 500e-9
    index = np.argmin(np.abs(Lambda-lambda_want))
    
    #plotting data for a single slice datapoint
    plt.contourf(y,x,Emag[:,:,index],100)
    plt.colorbar()
    plt.xlabel('y (nm)')
    plt.ylabel('x (nm)')
    plt.title("Electric field visualisation in the xy plane")
    
    fdtd.close()



