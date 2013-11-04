#!/usr/bin/env python
"""
This python script intends to look for MO near to atoms based on the center of
charges in order to perform later incremental calculations.

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
    rdr= csv.reader( source )
    with open('cocbarray','wb') as result:
        wtr= csv.writer(result)
        for r in rdr:
            wtr.writerow( (r[3], r[4], r[5]) )


# Import csv to matrix in numpy.
from numpy import genfromtxt
cocmatrix = genfromtxt('cocbarray', delimiter=',')
coordmatrix = genfromtxt('coordbarray', delimiter=',')
