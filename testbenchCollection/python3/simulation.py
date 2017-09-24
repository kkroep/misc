import sys
import numpy as np
import math

outputFile1 = open("outputFile1.txt", "w")
outputFile2 = open("outputFile2.txt", "w")
outputFile3 = open("outputFile3.txt", "w")


d_c = 25*10**-12 # delay of component

# component difference
for i in range(50):
    var = i/100*d_c # variance of signal
    N = var**2/(10**-12)**2 # var_tot = var/sqrt(N)
    N = math.ceil(N)
    if(N>0):
        outputFile1.write(str(i)+", "+str(N)+"\n")    


d_c = 50*10**-12 # delay of component

# component difference
for i in range(50):
    var = i/100*d_c # variance of signal
    N = var**2/(10**-12)**2 # var_tot = var/sqrt(N)
    N = math.ceil(N)
    if(N>0):
        outputFile2.write(str(i)+", "+str(N)+"\n")    

d_c = 100*10**-12 # delay of component


for i in range(50):
    var = i/100*d_c # variance of signal
    N = var**2/(10**-12)**2 # var_tot = var/sqrt(N)
    N = math.ceil(N)
    if(N>0):
        outputFile3.write(str(i)+", "+str(N)+"\n")    



# time difference
#for i in range(100):
#    var = i/100*d_c # variance of signal
#    N = var**2/(10**-12)**2 # var_tot = var/sqrt(N)
#    N = math.ceil(N)
#    outputFile2.write(str(i)+", "+str(N)+"\n")    








