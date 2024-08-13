import imp
import os
os.add_dll_directory("C:\\Program Files\\Lumerical\\v202\\api\\python")
lumapi = imp.load_source("lumapi", "C:\\Program Files\\Lumerical\\v202\\api\\python\\lumapi.py")

import lumapi

import numpy as np 
fdtd = lumapi.FDTD();
