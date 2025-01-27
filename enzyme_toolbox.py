from scipy.optimize import curve_fit
import numpy as np                       ## import the tools of NumPy but use a shorter name
from matplotlib import pyplot as plt

####################################
### Install UNCERTAINTIES package 
####################################

#!pip install uncertainties  # to install in Colab. Add it back to avoid installing again and again.

####################################
### Import versions of NumPy and Math that use uncertainty 
####################################

import uncertainties as un
from uncertainties import unumpy as unp
from uncertainties import umath as um

def linear(x, slope, intercept):  ### Take x values, slope and intercept and return the y values

    ####################################
    ### define a linear function
    ####################################

    y = slope * x + intercept
    return(y)

def MMplotFun(S, Vmax, KM):

    ####################################
    ### define a Michaelis-Menten function
    ####################################

    v = Vmax * S / (S + KM)
    return(v)
    
def MM_Make_Plot(x,y):
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           ### Reset default style - no needed but just in case.
    plt.figure(figsize=(5,4))  ### establish a figure with size 5x4
    
    ######################
    ### Plot the data
    #####################
    
    plt.plot(x, y, "ko")      ### 'k' is black, 'o' is 'circles', '-' is solid line. 
                              ### Try "g.", "ko-", "ro--", "b^-"
    
    ######################
    ### Add some style
    ######################
    
    plt.ylim(0, None)         ### y-axis limits are min = 0, max = whatever
    plt.xlim(0, None)         ### x-axis limits are min = 0, max = whatever
    
    plt.ylabel(r"$\nu\ \ /\,nM\: s^{-1}$")   ### The $ indicates "math typesetting language"
    plt.xlabel(r"$[S]\ \ /\,\mu M$")
    plt.title("Michaelis-Menten Plot")
    
    ######################
    ### Display and export the plot
    ######################
    
    plt.savefig("plot.pdf")    ### Save the image as a pdf file. Now you can use it in a document.
    plt.show()
    
def LB_Make_Plot(x,y):
    ######################
    ### reciprocol calculations
    #####################
    
    x = 1/x
    y = 1/y
    
    ####################################################
    ### Steal code above and re-use it
    ####################################################
    
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           ### Reset default style - no needed but just in case.
    plt.figure(figsize=(5,4))  ### establish a figure with size 5x4
    
    ######################
    ### Plot the data
    #####################
    
    plt.plot(x, y, "ko")
    
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(r"$1/(\nu\ /nM\; s^{-1})$")
    plt.xlabel(r"$1/([S]\ /\mu M)$")
    plt.title("Lineweaver-Burke Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    plt.savefig("plot.pdf")
    plt.show()

def Make_LB_Plot_With_Line(x,y):
    x = 1 / x
    y = 1 / y
    
    ### linear(x,slope, intercept) returns y
    params, stats = curve_fit(linear, x, y)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    slope, intercept = params   ### pull out the two values in the params object
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
    ################################
    ### Feed that list into the function for the line fit
    ################################
    
    y_fit = linear(x_fit,slope,intercept)
    
    ################################
    ### Steal the plot code from above and add a line to plot the calculated line fit
    ################################
    
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           
    plt.figure(figsize=(5,4))  
    
    ######################
    ### Plot the data
    #####################
    
    plt.plot(x, y, "ko")
                                   ###########################
    plt.plot(x_fit, y_fit, "k-")   ### This is the extra line
                                   ###########################
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(r"$1\,/\,(\nu\ /nM\; s^{-1})$")
    plt.xlabel(r"$1\,/\;([S]\ /\mu M)$")
    plt.title("Lineweaver-Burke Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    plt.savefig("plot.pdf")
    plt.show()

    return(slope, intercept)

def Make_MM_Plot_With_Line(x,y):

    params, stats = curve_fit(MMplotFun, x, y)   ## two objects are returned

    ####################################
    ### Interpret the results
    ####################################
    
    v_max, KM = params   ### pull out the two values in the params object
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
    ################################
    ### Feed that list into the function for the line fit
    ################################
    
    y_fit = MMplotFun(x_fit,v_max,KM)
    
    ################################
    ### Steal the plot code from above and add a line to plot the calculated line fit
    ################################
    
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
    
    plt.ylabel(r"$\nu\ \ /\,nM\: s^{-1}$")   ### The $ indicates "math typesetting language"
    plt.xlabel(r"$[S]\ \ /\,\mu M$")
    plt.title("Michaelis-Menten Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    #plt.savefig("MM_plot.pdf")
    plt.show()

    return(v_max, KM)

def Make_MM_Plot_with_Error(x, y, err, Vmax_list, KM_list, true_v_max, true_KM):
        
    ### We start with the x,y data entered at the top of this document
    ### Set an error range and then randomly add or subtract the error
    
    
    x2 = x   ## We want to copy the orginal data so that every time we rerun this
    y2 = y   ##  block of code we are starting agaion with the unchanged original data
    
    
    number_of_points = len(y2)
    random_values = np.random.randn(number_of_points) * err
    y2 = y2 + random_values
    
    ########################################################################
    ### Code for MM Plot from Above. Stolen and reused.
    ########################################################################
    
    ####################################
    ### Perform the curve fit
    ####################################
    
    params, stats = curve_fit(MMplotFun, x2, y2)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    v_max, KM = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_v_max, stdev_KM = perr          ### pull out the two stdev values 
    
    v_max_u = un.ufloat(v_max,stdev_v_max)  ## create a value with uncertainty built in
    KM_u = un.ufloat(KM,stdev_KM)  
    
    print(f"The Vmax is {v_max_u:0.3f}")
    print(f"The KM is {KM_u:0.3f}")
    print()
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x2), 100) 
    
    ################################
    ### Feed that list into the function for the line fit
    ################################
    
    y_fit = MMplotFun(x_fit,v_max,KM)
    
    ######################
    ### Create an empty plot
    #####################
    
    plt.rcdefaults()           
    plt.figure(figsize=(5,4))  
    
    ######################
    ### Plot the data and the curve fit line
    #####################
    
    plt.plot(x2, y2, "ko")
    plt.plot(x_fit, y_fit, "k-")   
                                                               ######################################
    plt.plot(x_fit, MMplotFun(x_fit, true_v_max, true_KM), "r-")  ### Add in "ghost line" for original data
                                                               ######################################
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, 1.3)
    plt.xlim(0, None)
    
    plt.ylabel(r"$\nu\ \ /\,nM\: s^{-1}$")  
    plt.xlabel(r"$[S]\ \ /\,\mu M$")
    plt.title("Michaelis-Menten Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    #plt.savefig("MM_plot_err.pdf")
    plt.show()

    return(v_max_u, KM_u)

def Make_LB_Plot_with_Error(x, y, err, Vmax_list, KM_list, true_slope, true_intercept):
    ### We start with the x,y data entered at the top of this document
    ### Set an error range and then randomly add or subtract the error
    
    x2 = x   ## We want to copy the orginal data so that every time we rerun this
    y2 = y   ##  block of code we are starting agaion with the unchanged original data    
    
    number_of_points = len(y)
    random_values = np.random.randn(number_of_points) * err
    y2 = y2 + random_values
    
    ########################################################################
    ### Code for MM Plot from Above. Stolen and reused.
    ########################################################################
    
    
    ####################################
    ### Perform the curve fit
    ####################################
    
    x2_lb = 1 / x2
    y2_lb = 1 / y2
    
    
    
    params, stats = curve_fit(linear, x2_lb, y2_lb)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    slope, intercept = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_slope, stdev_intercept = perr   ### pull out the two stdev values 
    
    slope_u = un.ufloat(slope,stdev_slope)               ## create a value with uncertainty built in
    intercept_u = un.ufloat(intercept,stdev_intercept)  
    
    v_max = 1 / intercept_u
    KM = v_max * slope_u
    
    print(f"The Vmax is {v_max:0.3f} uM/s")         ## Observe that the single variable now combines the value and the uncertainty
    print(f"The KM is {KM:0.3f} mM")
    print()
    
    #list_LB_Vmax.append(unp.nominal_values(v_max))
    #list_LB_KM.append(unp.nominal_values(KM))
    
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x2_lb), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
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
    
    plt.plot(x2_lb, y2_lb, "ko")
    plt.plot(x_fit, y_fit, "k-")   
                                                                      ######################################
    plt.plot(x_fit, linear(x_fit, true_slope, true_intercept), "r-")  ### Add in "ghost line" for original data
                                                                      ######################################
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(r"$1\,/\,(\nu\ /nM\; s^{-1})$")
    plt.xlabel(r"$1\,/\;([S]\ /\mu M)$")
    plt.title("Lineweaver-Burke Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    #plt.savefig("LB_plot_err.pdf")
    plt.show()

    return(v_max, KM)

def Make_EH_Plot_with_Error(x, y, err, Vmax_list, KM_list, true_v_max, true_KM):
    ### We start with the x,y data entered at the top of this document
    ### Set an error range and then randomly add or subtract the error
    
    experimental_error = 0.05   ### error will be +/- this value
    
    x2 = x   ## We want to copy the orginal data so that every time we rerun this
    y2 = y     ##  block of code we are starting agaion with the unchanged original data
    
    
    
    number_of_points = len(y)
    random_values = np.random.randn(number_of_points) * err
    y2 = y2 + random_values
    
    ########################################################################
    ### Code for MM Plot from Above. Stolen and reused.
    ########################################################################
    
    
    ####################################
    ### Perform the curve fit
    ####################################
    
    x2_eh = y2 / x2
    y2_eh = y2
    
    
    
    params, stats = curve_fit(linear, x2_eh, y2_eh)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    slope, intercept = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_slope, stdev_intercept = perr   ### pull out the two stdev values 
    
    slope_u = un.ufloat(slope,stdev_slope)               ## create a value with uncertainty built in
    intercept_u = un.ufloat(intercept,stdev_intercept)  
    
    v_max = intercept_u
    KM = - slope_u
    
    print(f"The Vmax is {v_max:0.3f} uM/s")         ## Observe that the single variable now combines the value and the uncertainty
    print(f"The KM is {KM:0.3f} mM")
    print()
    
    #list_EH_Vmax.append(unp.nominal_values(v_max))
    #list_EH_KM.append(unp.nominal_values(KM))
    
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x2_eh), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
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
    
    plt.plot(x2_eh, y2_eh, "ko")
    plt.plot(x_fit, y_fit, "k-")   
                                                                      ######################################
    plt.plot(x_fit, linear(x_fit, -true_KM, true_v_max), "r-")  ### Add in "ghost line" for original data
                                                                      ######################################
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, 1.3)
    plt.xlim(0, None)
    
    plt.ylabel(r"$\nu$")
    plt.xlabel(r"$\nu\,/\;[S]$")
    plt.title("Eadie-Hofstee Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    #plt.savefig("EH_plot_err.pdf")
    plt.show()

    return(v_max, KM)

def Make_HW_Plot_with_Error(x, y, err, Vmax_list, KM_list, true_v_max, true_KM):
    ### We start with the x,y data entered at the top of this document
    ### Set an error range and then randomly add or subtract the error
    
    
    x2 = x   ## We want to copy the orginal data so that every time we rerun this
    y2 = y     ##  block of code we are starting agaion with the unchanged original data
    
    true_v_max = 1.123   ### Results of MM curve fit
    true_KM = 5.002
    
    
    number_of_points = len(y)
    random_values = np.random.randn(number_of_points) * err
    y2 = y2 + random_values
    
    ########################################################################
    ### Code for MM Plot from Above. Stolen and reused.
    ########################################################################
    
    
    ####################################
    ### Perform the curve fit
    ####################################
    
    x2_hw = x2
    y2_hw = x2 / y2
    
    
    
    params, stats = curve_fit(linear, x2_hw, y2_hw)   ## two objects are returned
    
    ####################################
    ### Interpret the results
    ####################################
    
    slope, intercept = params   ### pull out the two values in the params object
    
    perr = np.sqrt(np.diag(stats))        ### convert covariance matrix to stdev values
    stdev_slope, stdev_intercept = perr   ### pull out the two stdev values 
    
    slope_u = un.ufloat(slope,stdev_slope)               ## create a value with uncertainty built in
    intercept_u = un.ufloat(intercept,stdev_intercept)  
    
    v_max = 1 / slope_u
    KM = intercept_u / slope_u
    
    print(f"The Vmax is {v_max:0.3f} uM/s")         ## Observe that the single variable now combines the value and the uncertainty
    print(f"The KM is {KM:0.3f} mM")
    print()
    
    #list_HW_Vmax.append(unp.nominal_values(v_max))
    #list_HW_KM.append(unp.nominal_values(KM))
    
    
    ################################
    ### make a list of x values from zero to the end of the line
    ################################
    
    x_fit = np.linspace(0, np.max(x2_hw), 100)  ## 100 points from 0 to the highest value on LB plot x-axis
    
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
    
    plt.plot(x2_hw, y2_hw, "ko")
    plt.plot(x_fit, y_fit, "k-")   
                                                                      ######################################
    plt.plot(x_fit, linear(x_fit, 1/true_v_max, true_KM/true_v_max), "r-")  ### Add in "ghost line" for original data
                                                                      ######################################
    ######################
    ### Add some style
    #####################
    
    plt.ylim(0, None)
    plt.xlim(0, None)
    
    plt.ylabel(r"$[S] \; / \; \nu$")
    plt.xlabel(r"$[S]$")
    plt.title("Hanes-Woolf Plot")
    
    ######################
    ### Display and export the plot
    #####################
    
    #plt.savefig("HW_plot_err.pdf")
    plt.show()


    return(v_max, KM)

def print_stats(params, stats):
    ####################################
    ### Print the two objects that are returned
    ####################################

    print(f"the params object contains...")
    display(params)
    print("which is the slope and the intercept")
    print()
    print(f"the stats object contains...")
    display(stats)
    print("which is the covariance matrix and can be used to calculate \nthe standard deviations in the parameters.")
    print()

