#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This python script intends to look for localized MO near to atoms based on the
center of charges in order to perform later incremental calculations as stated
in H. Stoll, Chem. Phys. Lett., 1992, 19.

__author__ = "Muammar El Khatib"
__copyright__ = "Copyright 2013, Muammar El Khatib"
__credits__ = [""]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Muammar El Khatib"
__email__ = "muammarelkhatib@gmail.com"
__status__ = "Development"
"""
import csv

# The number of core orbitals is asked.

print 'Please enter the number of core orbitals in your localization calculation:'
co=raw_input()
print ('CORE ORBITALS: ' +co)
print 'Please enter the number of electronic orbitals in your calculation:'
tno=raw_input()
print ('CORE ORBITALS: ' +tno)

"""
In this part of the code, we take the coordinates of the molecule from the
MOLPRO output file and then we dump its content in outfile.
"""
with open('input') as infile, open('coord','w') as outfile:
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
with open('input') as infile, open('coc','w') as centersoc:
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
with open('coc') as infile, open('cocsv', 'w') as outfile:
    outfile.write(infile.read().replace("    ", ", "))

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
            wtr.writerow( (r[3], r[4], r[5]) )

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
print (sumlmonat)

"""
Printing the input file with the rotation of the orbitals
"""
for i in sumlmonat:
    print ('{merge,2104.2; orbital,2103.2; move; rotate,' + str(i[0]) + '.1,'+str(tno)+'.1; }')

"""
In this part, files are cleaned. If you want to let them, then you can comment
all this section.

os.remove()
"""
