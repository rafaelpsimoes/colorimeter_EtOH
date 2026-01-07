#************************************************************************************
# DATA PROCESSING FOR DETERMINATION OF THE CALIBRATION CURVE
#************************************************************************************

#************************************************************************************
# INPUT DATA
#************************************************************************************
nscan=10 # Number of scans (default value)
nconc=5 # Number of concentrations (default value)
path='C:/Users/rafae/Desktop/Artigos em Andamento/2021 - Paper Concentracao Etanol/05_experimento_jun_2021_5concentracoes' # Working directory
delta_lamb=301 # Reads for [400 - 700] nm
lamb_0=400 # Initial wavelength
raw_data=1 # Plot raw data? 0-No; 1-Yes
range_nm=100 # Whavelength range for the maximum absorvance peak (in nm)
#************************************************************************************

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#************************************************************************************
# READING DATA
#************************************************************************************

os.chdir(path) # Moving to working directory

# READING CONCENTRATION FILE
concentrations = []
with open('concentrations.txt') as conc_file: # File with concentrations
    concentrations = conc_file.readlines()
nconc=len(concentrations)
for i in range(nconc): # Converting data to real numbers
    concentrations[i]=float(concentrations[i])

# READING WHITE
nlines=0
file = open('ref.txt','r')
for line in file:
    nlines=nlines+1
file.close()
white=[0]*nlines
i=0
file = open('ref.txt','r')
for line in file:
    fields=line.split(',')
    field1=fields[1]
    white[i]=float(field1)
    i=i+1
file.close()

# READING ABSORBANCE FROM SAMPLES
c = np.zeros((nlines,nconc)) # Creating an array to store the values from files
for j in range(nconc):
    i=0
    file = open(('c' + str(j+1) + '.txt'),'r')
    for line in file:
        fields=line.split(',')
        field1=fields[1]
        c[i,j]=float(field1)
        i=i+1
    file.close()

#************************************************************************************
# CALCULATING THE AVERAGE VALUES
#************************************************************************************

# WHITE
w = np.zeros(delta_lamb) # Creating an array to store the values from files
for k in range(nscan):
    for i in range(delta_lamb):
        w[i]=w[i]+white[k*delta_lamb+i]*(1.0/nscan)

# SAMPES
y = np.zeros((delta_lamb,nconc)) # Creating an array to store the values from files
for j in range(nconc):
    for k in range(nscan):
        for i in range(delta_lamb):
            y[i,j]=y[i,j]+c[k*delta_lamb+i,j]*(1.0/nscan)

#************************************************************************************
# CALCULATING TRANSMITANCE FROM ABSORBANCE
#************************************************************************************

for j in range(nconc):
    for i in range(delta_lamb):
        y[i,j]=w[i]-y[i,j]

#************************************************************************************
# CREATING AN ARRAY FOR LAMBDA VALUES
#************************************************************************************

x = np.zeros((delta_lamb,nconc))
for j in range(nconc):
    for i in range(delta_lamb):
        x[i,j]=lamb_0+i

#************************************************************************************
# FITTING ABSORBANCE AND PLOTTING DATA
#************************************************************************************

# CREATING A ARRAY OF STRINGS TO LEGEND
strs1 = ['']*nconc
strs2 = ['']*nconc*2

# DETERMINING REFERENCE VALUES FOR GAUSSIAN PEAK AND FILTERING THE RESULTS- Automated Way
x_data = x[:,nconc-1]
y_data = y[:,nconc-1]
x_ref = x_data[np.argmax(y_data)] # To search automatically the maximum value of absorbance
y_ref = np.amax(y_data) # To search automatically the maximum value of absorbance
range_nm = int(range_nm/2)

# FILTERING DATA ARROUND THE MAX ABSORVANCE VALUE
if np.argmax(y_data) <= range_nm:
    x_f = x[(0):(2*range_nm),:]
    y_f = y[(0):(2*range_nm),:]
elif (np.argmax(y_data)+range_nm) >= delta_lamb:
    x_f = x[(delta_lamb-2*range_nm):(delta_lamb),:]
    y_f = y[(delta_lamb-2*range_nm):(delta_lamb),:]
else:
    x_f = x[(np.argmax(y_data)-range_nm):(np.argmax(y_data)+range_nm),:]
    y_f = y[(np.argmax(y_data)-range_nm):(np.argmax(y_data)+range_nm),:]

y_cali=np.zeros(nconc) # To store the max value for calibration curve

# DETERMINING AND PLOTTING GAUSSIAN CURVES
def g1(x, a1, b1, c1):
    return a1*np.exp(-((x-b1)/c1)**2) # Gaussian function (One Peak)

fig1 = plt.figure(0)

for j in range(nconc):
    x_data = x_f[:,j]
    y_data = y_f[:,j]

    init_vals = [np.amax(y_data), x_ref, (0.8*(range_nm*2))]  # for [amp, cen, wid] - The amp and cent gest is automatically obtaneid from data and wid = 80% of range
    par, par_conv = optimize.curve_fit(g1, x_data, y_data, p0=init_vals)

    strs1[j]=("Concentration " +str(j+1))
    strs2[j]=("Concentration " +str(j+1))
    strs2[j+nconc]=("Raw Data " +str(j+1))

    plt.plot(x_data, g1(x_data, *par))

    y_cali[j]=np.amax(g1(x_data, *par)) # Max absorbance for calibration curve

    if raw_data==1:
        plt.scatter(x_data, y_data)

# PLOT DETAILS
plt.title("Absorbance EtOH",fontsize=20)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance (a.u.)")
if raw_data==0:
    plt.legend(strs1)
else:
    plt.legend(strs2)
#plt.show()
plt.show(block=False)
plt.savefig("absorbance_concentrations.png")
plt.pause(5)
plt.close()

#************************************************************************************
# DETERMINING A CALIBRATION FUNCTION AND PLOTTING DATA
#************************************************************************************

# LINEAR REGRESSION COEFICIENTS
# These commands generate an order 2 polynomial, of type:
# p2 = coef[0]*x^1 + coef[1]*x^0
# Conc =  coef[0]*Abs + coef[1]
coef = np.polyfit(concentrations,y_cali,1) # Coeficients of regression
poly1d_fn = np.poly1d(coef) # Linear equation
correlation = np.corrcoef(concentrations,y_cali)[0,1]
r_squared = correlation**2 # Determination Coefficient
coef = np.polyfit(y_cali,concentrations,1) # Coeficients of regression: Concentration as a function of absorbance

# POSITION OF EQUATION ON GRAPH
x_posi=np.amin(concentrations)+0.3*(np.amax(concentrations)-np.amin(concentrations))
y_posi=np.amin(y_cali)

# PLOTING THE GRAPH
fig2 = plt.figure(1)
plt.scatter(concentrations,y_cali)
plt.plot(concentrations,poly1d_fn(concentrations), '--k')
plt.xlim(0.9*np.amin(concentrations), 1.1*np.amax(concentrations))
plt.ylim(0.9*np.amin(y_cali), 1.1*np.amax(y_cali))
plt.text(x_posi, y_posi, str("Conc = " + str(round(coef[1],3)) + " + " + str(round(coef[0],3))+"*Abs : " + "$R^2$ = " + str(round(r_squared,2))), {'color': 'k', 'fontsize': 9})
plt.legend(("Linear Regression","Experimental Data"))
plt.title("Calibration Curve",fontsize=20)
plt.xlabel("Concentration (mL/L)")
plt.ylabel("Absorbance Peak (a.u.)")
plt.show(block=False)
plt.savefig("calibration_curve.png")
plt.pause(5)
plt.close()

#************************************************************************************
# WRITING PARAMETERS IN FILES FOR THE NEXT STEPS
#************************************************************************************

# WRITE THE EQUATION COEFFICIENTS TO FILE (CALIBRATION CURVE)
file = open("coefficients.txt", "w")
file.write(str(coef[0])+","+str(coef[1]))
file. close()

# WRITE THE LAMBDA RANGE TO FILE
file = open("lambda.txt", "w")
file.write(str(int(x_data[0]))+","+str(int(x_data[2*range_nm-1])))
file. close() 
