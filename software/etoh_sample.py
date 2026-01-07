#************************************************************************************
# DATA PROCESSING FOR DETERMINATION OF THE CALIBRATION CURVE
#************************************************************************************

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from scipy import optimize

#************************************************************************************
# INPUT DATA
#************************************************************************************
nscan=10 # Number of scans (default value)
path=pathlib.Path(__file__).parent.resolve() # Working directory
delta_lamb=301 # Reads for [400 - 700] nm
lamb_0=400 # Initial wavelength
raw_data=0 # Plot raw data? 0-No; 1-Yes
#************************************************************************************

#************************************************************************************
# READING DATA
#************************************************************************************

os.chdir(path) # Moving to working directory

# READING LAMBDA INTERVAL FOR EVALUATION
lamb = np.loadtxt("lambda.txt", comments="#", delimiter=",", unpack=False)
range_nm=lamb[1]-lamb[0]

# READING THE EQUATION COEFFICIENTS FROM CALIBRATION CURVE
coef = np.loadtxt("coefficients.txt", comments="#", delimiter=",", unpack=False)

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

# READING ABSORBANCE FROM SAMPLE
c = np.zeros(nlines) # Creating an array to store the values from files
i=0
file = open(('sample.txt'),'r')
for line in file:
    fields=line.split(',')
    field1=fields[1]
    c[i]=float(field1)
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
y = np.zeros(delta_lamb) # Creating an array to store the values from files
for k in range(nscan):
    for i in range(delta_lamb):
        y[i]=y[i]+c[k*delta_lamb+i]*(1.0/nscan)

#************************************************************************************
# CALCULATING TRANSMITANCE FROM ABSORBANCE
#************************************************************************************

for i in range(delta_lamb):
    y[i]=w[i]-y[i]

#************************************************************************************
# CREATING AN ARRAY FOR LAMBDA VALUES
#************************************************************************************

x = np.zeros(delta_lamb)
for i in range(delta_lamb):
    x[i]=lamb_0+i

#************************************************************************************
# FITTING ABSORBANCE AND PLOTTING DATA
#************************************************************************************

# AUXILIAR VARIABLES
range_nm = int(range_nm/2)
strs1 = ['']*1
strs2 = ['']*2

# FILTERING DATA IN THE REGION WITH THE PEAK OF ABSORBANCE
x_f = x[(int(lamb[0])-lamb_0):(int(lamb[1])-lamb_0)]
y_f = y[(int(lamb[0])-lamb_0):(int(lamb[1])-lamb_0)]

x_ref = x_f[np.argmax(y_f)] # To search automatically the maximum value of absorbance
y_ref = np.amax(y_f) # To search automatically the maximum value of absorbance

# DETERMINING AND PLOTTING GAUSSIAN CURVES
def g1(x, a1, b1, c1):
    return a1*np.exp(-((x-b1)/c1)**2) # Gaussian function (One Peak)

fig1 = plt.figure(0)

init_vals = [np.amax(y_f), x_ref, (0.8*(range_nm*2))]  # for [amp, cen, wid] - The amp and cent gest is automatically obtaneid from data and wid = 80% of range
par, par_conv = optimize.curve_fit(g1, x_f, y_f, p0=init_vals)

strs1[0]=str("Sample Absorbance")
strs2[0]=str("Sample Absorbance")
strs2[1]=str("Raw Data")

x_posi=np.amin(x_f)+0.3*(np.amax(x_f)-np.amin(x_f))
y_posi=np.amin(y_f)+0.2*(np.amax(y_f)-np.amin(y_f))

plt.plot(x_f, g1(x_f, *par))

if raw_data==1:
    plt.scatter(x_f, y_f)

# PLOT details
plt.title("Absorbance EtOH in Sample",fontsize=20)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Absorbance (a.u.)")
if raw_data==0:
    plt.legend(strs1)
else:
    plt.legend(strs2)
plt.text(x_posi, y_posi, str("Concentration = " +str(round(coef[1]+coef[0]*np.amax(g1(x_f, *par)),3))+" mL/L"), {'color': 'k', 'fontsize': 9})
plt.show(block=False)
plt.savefig("absorbance_sample.png")
plt.pause(5)
plt.close()
