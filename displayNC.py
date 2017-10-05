from netCDF4 import Dataset
import datetime
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.dates import DateFormatter
import plotly.plotly as py

def getArray(nc,name) :
    #nc = Dataset(filename, mode='r')
    myArray = nc.variables[name][:]
    myArray = np.flipud(np.transpose(np.squeeze(myArray)))
    #nc.close()
    return myArray

def getSingleArray(filename,name) :
    nc = Dataset(filename, mode='r')
    myArray = nc.variables[name][:]
    myArray = np.flipud(np.transpose(np.squeeze(myArray)))
    nc.close()
    return myArray 

def displayVariables(filename,variables,figname):
    print(filename,variables)
    nc = Dataset(filename, mode='r')
    #print('The variables contained in the output database are:')
    keys = nc.variables.keys()
    for i,j in zip(nc.variables,keys):
        a = nc.variables[i].shape
        b = nc.variables[i].units
        c = nc.variables[i].long_name
        #print(j, '\t', c, '\t', b, '\t', a)
    tt = nc.variables['time']
    startTime = datetime.datetime.strptime(tt.units,'seconds since %Y-%m-%d %H:%M:%S')
    timestamp = np.squeeze(np.array(tt[:]))
    timestamp = [(startTime + datetime.timedelta(seconds = x)) for x in timestamp]
    
    zz = np.flipud(np.array(nc.variables['z'][0]))
    
    #General settings for the plot
    cmap = matplotlib.cm.gist_ncar #jet #afmhot_r
    fig,axes = plt.subplots(nrows = len(variables), ncols = 1, figsize = (7.5, 3*(len(variables)+1)))
    for (aH, name) in zip(axes,variables) :
        mat = getArray(nc,name)
        im = aH.pcolormesh(timestamp, zz, mat, cmap = cmap)
        aH.xaxis_date()
        aH.set_ylabel('Depth (m)')
        #aH.pcolormesh(tt, zz, mat, cmap = cmap)
    cbar_ax = fig.add_axes([0.05, 0.075, 0.9, 0.025])
    plt.colorbar(im,orientation='horizontal', cax = cbar_ax, label =r'CDOM')
    plt.savefig(figname)
    plt.close("all")
    nc.close()
    return timestamp
    
class MidpointNormalize(colors.Normalize):
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))
    
def temperatureDisplay(filename,figname) :
    nc = Dataset(filename, mode='r')
    variables = ['tprof','temp','residuals'];
    arrayList = [getArray(nc,'tprof'),getArray(nc,'temp')]
    arrayList.append(arrayList[0] - arrayList[1])
    
    minVal = 50000
    maxVal = -50000    
    
    for i in arrayList :
        mini = np.amin(i)
        maxi = np.amax(i)
        if mini < minVal :
            minVal = mini
        if maxi > maxVal :
            maxVal = maxi
            
    print(minVal,maxVal)

    tt = nc.variables['time']
    startTime = datetime.datetime.strptime(tt.units,'seconds since %Y-%m-%d %H:%M:%S')
    timestamp = np.squeeze(np.array(tt[:]))
    timestamp = [(startTime + datetime.timedelta(seconds = x)) for x in timestamp]
    
    zz = np.flipud(np.array(nc.variables['z'][0]))
    
    #General settings for the plot
    cmap = matplotlib.cm.gist_ncar #jet #afmhot_r
    fig,axes = plt.subplots(nrows = len(variables), ncols = 1, figsize = (10, 3*(len(variables))))
    for (aH, mat) in zip(axes,arrayList) :
        im = aH.pcolormesh(timestamp, zz, mat, cmap = cmap, vmin = minVal, vmax = maxVal,norm=MidpointNormalize(midpoint=0.))
        aH.xaxis_date()
        aH.set_ylabel('Depth (m)')
    cbar_ax = fig.add_axes([0.05, 0.075, 0.9, 0.025])
    axes[0].set_title('Observed')
    axes[1].set_title('Simulated')
    axes[2].set_title('Observed - Simulated')
            
    plt.colorbar(im,orientation='horizontal', cax = cbar_ax, label =r'Temperature $\left(^{\circ}C\right)$')
    #fig.suptitle('Observed, simulated and residual temperature profiles', size = 'xx-large')
    #fig.tight_layout()
    plt.savefig(figname)
    plt.close()
    nc.close()
    

    

    


    