#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This python script intends to look for localized MO near to atoms based on the
center of charges in order to perform later incremental calculations as stated
in H. Stoll, Chem. Phys. Lett., 1992, 19.

__author__ = "Muammar El Khatib"
__copyright__ = "Copyright 2014, Muammar El Khatib"
__credits__ = [""]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Muammar El Khatib"
__email__ = "muammarelkhatib@gmail.com"
__status__ = "Development"
"""

"""
The name of the output is readed from the prompt
"""
import sys
len(sys.argv)
inputuser=str(sys.argv[1])
import csv

# We start asking information to do the input file

print 'Please enter the number of core orbitals in your localization calculation:'
co=raw_input()
print ('CORE ORBITALS: ' +co + '\n')
print 'Please enter the number of localized orbitals in your calculation:'
tno=raw_input()
print ('NUMBER OF ELECTRONIC ORBITALS: ' +tno + '\n')

print ('')
print ('')

# This is needed for the CASSCF section
print ('Would you like to build the CASSCF input file? [Default answer: no]')
yes = set(['yes','y', 'ye', 'Yes', 'Ye', 'Y'])
answer=raw_input()
if answer in yes:
    print ('')
    print ('')
    print ('Now you will be asked about information to build the CASSCF input')
    print ('Please enter the number of CLOSED MOs')
    corb=raw_input()
    print ('NUMBER OF CLOSED MOs: ' +corb + '\n')
    print ('Please enter the number of FROZEN MOs')
    frozorb=raw_input()
    print ('NUMBER OF FROZEN MOs: ' +frozorb + '\n')
    print ('Please enter the number of OCCUPIED MOs')
    occorb=raw_input()
    print ('NUMBER OF OCCUPIED MOs: ' +occorb + '\n')
    actorb=int(occorb)-int(corb)
    print ('Your requested number of active orbitals is: ' + str(actorb))
    print ('Please enter your wavefunction in the format: wf,#electrons,Sym,Multiplicity')
    print ('e.g.: wf,224,1,0')
    wf=raw_input()
    print ('The wavefunction: ' +wf + '\n')

"""
In this part of the code, we take the coordinates of the molecule from the
MOLPRO output file and then we dump its content in outfile.
"""
with open(inputuser) as infile, open('coord','w') as outfile:
    copy = False
    for line in infile:
        if line.strip() == "NR  ATOM    CHARGE       X              Y              Z":
            copy = True
        elif line.strip() == "Bond lengths in Bohr (Angstrom)":
            copy = False
        elif copy:
            outfile.write(line)

outfile.close()

"""
Now we create csv
"""
with open('coord') as fr, open('coordv', 'w') as fw:
    for line in fr:
        fw.write(','.join(line.strip().split()) + '\n')

# Unneeded columns are deleted from the csv
input = open('coordv', 'rb')
output = open('coordvout', 'wb')
writer = csv.writer(output)
for row in csv.reader(input):
    if row:
        writer.writerow(row)

input.close()
output.close()

with open('coordvout','rb') as source:
    rdr= csv.reader( source )
    with open('coordbarray','wb') as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow( (r[3], r[4], r[5]) )

"""
The same process is done now to take out the centers of charges from the MOLPRO
output file.
"""
with open(inputuser) as infile, open('coc','w') as centersoc:
    copy = False
    for line in infile:
            if line.strip() == "Sym.   Orb.            X            Y            Z":
                copy = True
            elif line.strip() == "Localized orbitals saved to record      2103.2  (orbital set 1)":
                copy = False
            elif copy:
                centersoc.write(line)

""" Here I convert center of chargers file to csv so that I can make use of the
csv module in python.
"""
# This code below used to work when files were fixed width
###with open('coc') as infile, open('cocsv', 'w') as outfile:
###    outfile.write(infile.read().replace("    ", ", "))

# This is a more general code for making it work when you don't have width.
with open('coc') as infile, open('cocsv', 'w') as outfile:
    for line in infile:
        outfile.write(" ".join(line.split()).replace(' ', ','))
        #outfile.write(",") # trailing comma shouldn't matter
        outfile.write("\n")

# Unneeded columns are deleted from the csv
input = open('cocsv', 'rb')
output = open('cocsvout', 'wb')
writer = csv.writer(output)
for row in csv.reader(input):
    if row:
        writer.writerow(row)

input.close()
output.close()

with open('cocsvout','rb') as source:
    rdr= csv.reader(source)
    with open('cocbarray','wb') as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow( (r[2], r[3], r[4]) )

# Now we strip the CORE ORBITALS from the center of charges
def skip_first(seq, n):
    for i,item in enumerate(seq):
        if i >= n:
            yield item

with open('cocbarray', 'rb') as total:
    csvreader = csv.reader(total)
    with open('cocbarrayr','wb') as result:
        wtr= csv.writer(result)
        for row in skip_first(csvreader, int(co)):
            wtr.writerow(row)

# Import csv files to matrices in numpy.
from numpy import genfromtxt
cocmatrix = genfromtxt('cocbarrayr', delimiter=',')
coordmatrix = genfromtxt('coordbarray', delimiter=',')

print ('')
print ('Coordinate array')
print ('')
print(coordmatrix)


"""
Now, the distances between two points in the 3D arrays are calculated using
scipy and cdists.
"""
import scipy.spatial as sp
import numpy as np
distances=sp.distance.cdist(coordmatrix,coordmatrix, 'euclidean')

print ('')
print ('Distances between atoms')
print ('')
print distances

atnearat=np.argwhere((distances > 2.3) & (distances < 2.7))
print (atnearat)
#print (np.argwhere((distances > 2.55) & (distances < 2.87)))

dcoordcoc=sp.distance.cdist(cocmatrix, coordmatrix, 'euclidean')

print ('')
print ('Distances between atoms and center of charges')
print ('')
print dcoordcoc

lmonat=np.argwhere((dcoordcoc > 0.5) & (dcoordcoc < 2.0))
adlmonat=[(int(co)+1),1]
sumlmonat=lmonat+adlmonat

print ('')
print ('List of atoms that are near to certain LMO')
print ('')
print (sumlmonat)

"""
Printing the input file with the rotation of the orbitals
"""
# It works but it prints everything
#for i1, i2 in zip(sumlmonat,sumlmonat[1:]):
#    print ('! Atom ' + str(i1[1]) + ' Atom ' + str(i2[1]))
#    print ('{merge,2104.2; orbital,2103.2; move; rotate,' + str(i1[0]) + '.1,' + str(tno) + '.1; }')

import itertools as it
molpro=open('molpro.in','w')
for r in it.izip_longest(sumlmonat[::2], sumlmonat[1::2]):
    # This is statement into the for loop is to avoid doing rotations between
    # LMO with higher energy with itself.
    if str(r[0][0]) !=  str(tno):
        # Uncomment these two lines for debugging
        # print ('! Localized MO between Atom ' + str(r[0][1]) + '    and Atom ' + str(r[1][1]))
        # print ('{merge,2104.2; orbital,2103.2; move; rotate,' + str(r[0][0]) + '.1,' + str(tno) + '.1; }')
        molpro.write('! Localized MO between Atom ' + str(r[0][1]) + ' and Atom ' + str(r[1][1]) + '\n')
        molpro.write('{merge,2104.2; orbital,2103.2; move; rotate,' + str(r[0][0]) + '.1,' + str(tno) + '.1;}' + '\n')
    else:
        molpro.write('! Localized MO between Atom ' + str(r[0][1]) + ' and Atom ' + str(r[1][1]) + '\n')
        molpro.write('{merge,2104.2; orbital,2103.2; move;}' + '\n')
        molpro.write('' + '\n')
    if answer in yes:
        molpro.write('{multi; orbital,2104.2; closed,' + corb + '; occ,'+ occorb +'; frozen,' + frozorb +',2104.2;' + wf + '; canorb,2105.2;}' + '\n')
        molpro.write('{ccsd(t); orbital,2105.2; occ,'+ occorb +'; core,' + frozorb + '; ' + wf + ';}' + '\n')

        molpro.write('einc_' + str(r[0][1]) + '-' + str(r[1][1]) + '=energy-ehf;' + '\n')
        molpro.write('' + '\n')
    else:
        molpro.write('' + '\n')

print('Input file written to molpro.in')

"""
In this part, files are cleaned. If you want to let them, then you can comment
all this section.
"""

import os
# Files related to the coordinates
os.popen('rm -f coordvout coordv coord coordbarray')

# Files related to the center of charges
os.popen('rm -f coc cocbarray cocsvout cocsv cocbarrayr cocbarraycoc')
