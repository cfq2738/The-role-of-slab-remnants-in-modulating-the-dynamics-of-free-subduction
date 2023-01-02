#!/usr/bin/env python3

import math

##############################
### Parameters of the Mesh ###
##############################

outer_radius = 2.22
inner_radius = 1.22
theta = math.pi/2.0
theta_centre = 0.0 #math.pi/6.0
phi = math.pi/2.0

#################################
### NonDimensional Parameters ###
#################################

d_nondim = 2.89e6
rho_nondim = 3300
mu_nondim = 2.0e20

########################
### Fixed Parameters ###
########################

# nondimensional gravitational acceleration
g = 3982.698885

# Depth of upper mantle
D_um = 660.0e3/d_nondim

# Upper Mantle Viscosity
mu_um = 2.0e20/mu_nondim

# Lower Mantle Viscosity
mu_lm = 50 * mu_um

# Initial Visco-Plastic Plate Viscosity
mu_plate = 100 * mu_um

# Side Plate Viscosity
mu_sp = 2.0e23/mu_nondim

# reference mantle density (not provided in Stegman)
rho_mantle = 3300/rho_nondim

# 2222km slab length
lon_degs = 19.8

# Dip Angle in degrees
SlabTipAlpha = 45.0

# Slab tip length
SlabTipLength = 150.0e3/d_nondim #equivalent of a 100km slab tip length

# Radius of Curvature
Roc = 250.0e3/d_nondim

# Angle of Curvature
beta = 77

# Yield Stress
tau_yield = 100e6

###########################
### Variable Parameters ###
###########################

# Slab width
lat_degs = 43.2 #4800 km at equator

# Side Plate Start
lat_sp = 21.8 # 2422km from equator, 22km from edge of 4800km plate

# Plate Thickness
h = 70.0e3/d_nondim

# Core plate Thickness
hc = 30.0e3/d_nondim

# Base radii of different layers
up_radius = outer_radius - (h - hc)/2.0
cp_radius = up_radius - hc
lp_radius = outer_radius - h

# Plate/mantle density difference
delta_rho = 80.0/rho_nondim

# Core Plate Viscosity
mu_core = 100*mu_um

# Blob Width
blob_width = 2400.0e3/d_nondim

# Blob thickness
blob_thickness = 400.0e3/d_nondim # blob_thickness = plate thickness for a vertical case, blob length for a horizontal case

# Blob distance E/W from trench
blob_dist = 500.0e3/d_nondim

# Blob Top Depth
blob_top = 590.0e3/d_nondim

# Blob Bottom Depth
blob_bottom = 660.0e3/d_nondim


##########################################
### Slab tip based on coords and depth ###
##########################################

### Depth of the slab tip
###SlabTipDepth = 0.13841 * thickness_scale

# Distance of slab tip in latitude in degrees
#slab_dist = 0.0
#SlabTipPhi = math.radians(90 - lat_degs/2.0 - slab_dist)

########################################
### Slab tip based on dip and length ###
########################################



