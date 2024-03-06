from scipy.optimize import curve_fit
import numpy as np                       ## import the tools of NumPy but use a shorter name
from matplotlib import pyplot as plt



####################################
### Import versions of NumPy and Math that use uncertainty 
####################################

import uncertainties as un
from uncertainties import unumpy as unp
from uncertainties import umath as um

def MM_Plot(x, y):

    ####################################
    ### Define the MM equation for the curve fit as a function
    ####################################

    def MMplot(S, Vmax, KM):
        v = Vmax * S / (S + KM)
        return(v)
        
    ####################################
    ### Perform the curve fit
    ####################################
    
    params, stats = curve_fit(MMplot, x, y)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    v_max, KM = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_v_max, stdev_KM = perr          ### pull out the two stdev values 
    
    v_max_u = un.ufloat(v_max,stdev_v_max)  ## create a value with uncertainty built in
    KM_u = un.ufloat(KM,stdev_KM)      
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x), 100) 
    
    ################################
    ### Feed that list into the function for the line fit
    ################################
    
    y_fit = MMplot(x_fit,v_max,KM)
    
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           
    plt.figure(figsize=(5,4))  
    
    ######################
    ### Plot the data and the curve fit line
    #####################
    
    plt.plot(x, y, "ko")
    plt.plot(x_fit, y_fit, "k-")   
                                                                                                     
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(r"$\nu$")  
    plt.xlabel(r"$[S]$")
    plt.title("Michaelis-Menten Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    plt.savefig("MM_plot.pdf")
    plt.show()

    return v_max_u, KM_u

def Linear_Plot(x, y, title ="Enter Title Here", xaxis = "x-axis", yaxis = "y-axis"):

    def linear(x, slope, intercept):  ### Take x values, slope and intercept and return the y values
        y = slope * x + intercept
        return(y)

    params, stats = curve_fit(linear, x, y)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    slope, intercept = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_slope, stdev_intercept = perr   ### pull out the two stdev values 
    
    slope_u = un.ufloat(slope,stdev_slope)               ## create a value with uncertainty built in
    intercept_u = un.ufloat(intercept,stdev_intercept)  
    
        
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
    ################################
    ### Feed that list into the function for the line fit
    ################################
    
    y_fit = linear(x_fit, slope, intercept)
    
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           
    plt.figure(figsize=(5,4))  
    
    ######################
    ### Plot the data and the curve fit line
    #####################
    
    plt.plot(x, y, "ko")
    plt.plot(x_fit, y_fit, "k-")   

    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(yaxis)
    plt.xlabel(xaxis)
    plt.title(title)
    
    ######################
    ### Display and export the plot
    #####################
    
    plt.savefig("Linear_plot.pdf")
    plt.show()

    return slope_u, intercept_u