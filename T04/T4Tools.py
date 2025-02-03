############################################
###  Import packages and set up variables
############################################

from os import system                    ## import tools to access the file sytsem directly
from scipy.optimize import curve_fit
import numpy as np                       ## import the tools of NumPy but use a shorter name
import pandas as pd                      ## import tools for data handling
from matplotlib import pyplot as plt
import requests                          ## tools to access web content

## fancy plot style sheet
github_location_styles = "https://raw.githubusercontent.com/blinkletter/LFER-QSAR/main/styles/"
#plt.style.use(github_location_styles + "tufte.mplstyle")        

github_data_location= "https://raw.githubusercontent.com/blinkletter/3530Biochem/main/T04/data/"
#github_data_location= "./data/"


####################################
### Import versions of NumPy and Math that use uncertainty 
####################################

import uncertainties as un
from uncertainties import unumpy as unp
from uncertainties import umath as um


########################################################################
def trim_and_format_data(df):
    
    df.reset_index(inplace = True)             ### had to reset the index to give a first line with index '0'
    #display(df)                               ### uncomment to check whats happening to the dataframe
    df.drop(["index"], axis=1, inplace=True)   ### drop the former index column that was created by the reset 
    #display(df)
    

    df.loc[0,0] = "Time (min)"                 ### Put the word 'Time" in the top corner - you'll see why soon
    
    df.drop([1], inplace=True)                 ### drop the second row that is all text labels
    #display(df)
    
    ################################################################################
    ### We now have a dataframe with the data in rows labeled as 2 through 8.
    ### Row 0 is the concentrations of substrate. Let us uses these to index the dataframe
    ################################################################################
    
    df.columns = df.iloc[0]         ### Set the contents of the first row to be the column headers
    #display(df)
    
    df.drop([0], inplace=True)      ### drop the first row that is now set as the column headers

    df.reset_index(inplace = True)             ### again, had to reset the index to give a first line with index '0'
    #display(df)                               ### uncomment to check whats happening to the dataframe
    df.drop(["index"], axis=1, inplace=True)   ### drop the former index column that was created by the reset 
    
    return(df.copy())    ### copy the resulting editted dataframe to a more useful name

def get_slopes_and_plot_them_all(df, title ="Enter Title Here", xaxis = "x-axis", yaxis = "y-axis"):
    
    def linear_zero(x, slope):  ### Take x values, slope and intercept and return the y values
        y = slope * x
        return(y)
        
    plt.rcdefaults()           ### Reset default style - not needed, but just in case.
    plt.figure(figsize=(5,4))  ### Establish a figure with size 5x4
    
    x = df.pop("Time (min)")   ### Pop (remove) the 'time' column and assign it to x
    x = x.astype('float')      ### For some reason all data was text. x now converted to floating point.
    
    list_slopes = []                ### create an empty list for slopes at each concentration

    for i in df.columns:            ### Get each column name one-at-a-time in turn

        y = df[i].astype('float')                   ### Get each column of concentrations and convert to floating point
        slope, cov = curve_fit(linear_zero, x, y)   ### two objects are returned

        x_fit = np.linspace(0, np.max(x), 50)       ### Make line for curve fit
        
        perr = np.sqrt(np.diag(cov))            ### convert covariance matrix to stdev values
        stdev_slope = perr                      ### pull out the two stdev values 
        slope_u = un.ufloat(slope,stdev_slope)  ### create a value with uncertainty built in
        list_slopes.append(slope_u)             ### add slope value to the list
    
        plt.plot(x,y,".")                                ### Plot each column against time
        plt.plot(x_fit,linear_zero(x_fit, slope),"k-")   ### Plot the line   
        plt.text(np.max(x) + 0.6, np.max(y), i)          ### label each line on the plot
    
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    plt.ylabel(yaxis)
    plt.xlabel(xaxis)
    plt.title(title)

    plt.tight_layout()
    plt.savefig("MultiPlot.pdf")
    plt.show()

    concs = df.columns.astype('float')                ### Convert list of conc from column header to array of floating point
    list_slopes_n = unp.nominal_values(list_slopes)   ### Rates is a list of uncertainty values
    list_slopes_s = unp.std_devs(list_slopes)         ### separate them into lists of nominal values and std deviations                           
    rates = unp.uarray(list_slopes_n, list_slopes_s)  ### create an array of uncertainty values using Uncertainties.uNumPy.uarray()

    return(concs, rates)

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
    
    y_stdev = unp.std_devs(y)   ### y is a set of uncertainty values. Extract the two parts
    y       = unp.nominal_values(y)

    params, stats = curve_fit(MMplot, x, y,          ## two objects are returned
                              sigma = y_stdev,       ## include stdevs in curve fit
                              absolute_sigma = True) ## errors are values, not relative.
    
    ####################################
    ### Interpret the results
    ####################################
    
    v_max, KM = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))          ### convert covariance matrix to stdev values
    stdev_v_max, stdev_KM = perr            ### pull out the two stdev values 
    
    v_max_u = un.ufloat(v_max,stdev_v_max)  ### create a value with uncertainty built in
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
    
    plt.plot(x, y, "ko", markersize = 4)

    plt.errorbar(x, y, yerr = 2*y_stdev,
                 fmt="none", color = "black",
                 elinewidth =0.7, capsize = 4)

    plt.plot(x_fit, y_fit, "k-", linewidth = 1)   
                                                                                                     
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
    ######################
    
    plt.tight_layout()
    plt.savefig("MM_plot.pdf")
    plt.show()

    return v_max_u, KM_u

def Linear_Plot(x, y, title ="Enter Title Here", xaxis = "x-axis", yaxis = "y-axis"):

    def linear(x, slope, intercept):  ### Take x values, slope and intercept and return the y values
        y = slope * x + intercept
        return(y)



    y_stdev = unp.std_devs(y)   ### y is a set of uncertainty values. Extract the two parts
    y       = unp.nominal_values(y)

    params, stats = curve_fit(linear, x, y,          ## two objects are returned
                              sigma = y_stdev,       ## include stdevs in curve fit
                              absolute_sigma = True) ## errors are values, not relative.
    
 

### uncomment line below to fit without using errors

#    params, stats = curve_fit(linear, x, y)   ## two objects are returned
    
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
    
    plt.plot(x, y, "ko", markersize = 4)

    plt.errorbar(x, y, yerr = 2*y_stdev,
             fmt="none", color = "black",
             elinewidth =0.7, capsize = 4)

    plt.plot(x_fit, y_fit, "k-", linewidth = 1)   

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
    
    plt.tight_layout()
    plt.savefig("Linear_plot.pdf")
    plt.show()

    return slope_u, intercept_u

