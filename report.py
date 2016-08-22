import numpy as np
import pint
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import sc_check

un = pint.UnitRegistry()

# Report related functions ..
# .... used for plotting and extracting info 
# .... from the a source object
#  Author: Leonel Morejon
#  Date: 22/08/2016

def dircosines_surf(sourcefileobject,**kwargs):
	''' Returns the surface plot of the source
		takes all kwargs needed for the plot_surface
	'''
	x = 2*np.random.rand(14) - 1
	y = 2*np.random.rand(14) - 1
	z = 2*np.random.rand(14) - 1

	x = sourcefileobject.data['tx'].magnitude
	y = sourcefileobject.data['ty'].magnitude
	z = sourcefileobject.data['tz'].magnitude

	grid_x, grid_y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

	grid_z = griddata((x, y), z, (grid_x, grid_y), method='cubic')

	fig = plt.figure()
	ax = fig.gca(projection='3d',**kwargs)
	ax.plot_surface(grid_x, grid_y, grid_z, cmap=plt.cm.Spectral,**kwargs)

	return ax


def plot_spatial_distribution(source):
    f, axarr = plt.subplots(1,3,sharey=True, figsize=(18,5));    
    for i,m in zip(range(3),['x','y','z']):
        axarr[i].hist(source.data[m].magnitude);
        axarr[i].locator_params(axis='x',nbins=7);
        axarr[i].set_xlabel(m+" in "+str(source.data[m].u))


def plot_phase_spaces(source):
    f, axarr = plt.subplots(1,3, figsize=(20,5));    
    for i,m,mp in zip(range(3),['x','y','z'],['tx','ty','tz']):
        X = source.data[m].m
        Y = source.data[mp].m
            
        axarr[i].scatter(X,Y);
        # reducing number of tics in x axis
        axarr[i].locator_params(axis='x',nbins=7);
        
        # rescaling to fit size of plot to the data        
        xlims = (1.05*min(X), 1.05*max(X))
        if xlims[0] == xlims[1]:
            xlims = (.95*min(X), 1.05*max(X))            

        ylims = (1.05*min(Y), 1.05*max(Y))
        if ylims[0] == ylims[1]:
            ylims = (.95*min(Y), 1.01*max(Y))
            
        axarr[i].set_xlim( xlims )
        axarr[i].set_ylim( ylims )
        # labeling axes and title        
        axarr[i].set_title("Phase space: " + m + " versus " + mp)
        axarr[i].set_xlabel(m  +" in " + str(source.data[m].u))
        axarr[i].set_ylabel(mp +" in " + str(source.data[mp].u))
        

def plot_energy_distribution(source):
    plt.hist(source.data['E'].m);
    plt.xlabel('E in '+str(source.data['E'].u))