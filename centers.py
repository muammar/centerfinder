#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This python program intends to look for localized MO near to atoms based on the
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

print ('Please enter the number of core orbitals in your localization calculation:')
co=raw_input()
print ('CORE ORBITALS: ' +co + '\n')
print ('Please enter the number of localized orbitals in your calculation:')
tno=raw_input()
print ('NUMBER OF ELECTRONIC ORBITALS: ' +tno + '\n')

print ('')
print ('')

# This is needed for the CASSCF section
print ('Would you like to build the CASSCF input file? [Default answer: no]')
yes = set(['yes','y', 'ye', 'Yes', 'Ye', 'Y'])
casans=raw_input()
if casans in yes:
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
  # Here, we strip out atoms different from C
            if not r[1].startswith('H'):
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
print ('Shape of the matrix: '+str(distances.shape))
print (distances)

atnearat=np.argwhere((distances > 2.3) & (distances < 2.7))
print (atnearat)
#print (np.argwhere((distances > 2.55) & (distances < 2.87)))

dcoordcoc=sp.distance.cdist(cocmatrix, coordmatrix, 'euclidean')

print ('')
print ('Distances between atoms and center of charges')
print ('')
print (dcoordcoc)

lmonat=np.argwhere((dcoordcoc > 0.5) & (dcoordcoc < 2.0))
adlmonat=[(int(co)+1),1]
sumlmonat=lmonat+adlmonat

print ('')
print ('List of atoms that are near to certain LMO')
print ('')
print (sumlmonat)

# We take out pairs of atoms whose LMO are shared.
#
# http://stackoverflow.com/questions/22093001/comparing-and-discarding-two-consecutive-elements-not-complying-certain-conditio
"""
from collections import Counter
cnt = Counter(zip(*sumlmonat)[0])
sumlmonat = [p for p in sumlmonat if cnt[p[0]] > 1]
print sumlmonat
"""
prev = None
newp = []
length = len(sumlmonat) - 1
for i in range(length):
    if sumlmonat[i][0] == sumlmonat[i+1][0] or sumlmonat[i][0] == prev:
        newp.append(sumlmonat[i])
        prev = sumlmonat[i][0]

if sumlmonat[length][0] == sumlmonat[length-1][0]:
  newp.append(sumlmonat[length])
sumlmonat=newp
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

# The array for treating the two body interactions is initialized
onebody=[] #This array is needed to substract 1 body energies in the two-body interaction part
twobody=[]

# Below we write the one body interactions in molpro.in
listica=[]
print ('Would you like to discard atoms? [Default answer: no]')
yes = set(['yes','y', 'ye', 'Yes', 'Ye', 'Y'])
answer=raw_input()
if answer in yes:
    print ('Enter the atoms to be discarded as shown below:')
    print ('eg. 1,2,3,4')
    print ('Note: Only carbon atoms are taken into account')
    listica = raw_input().split(",")
    print (listica)

for idxob, r in enumerate(it.izip_longest(sumlmonat[::2], sumlmonat[1::2])):
    print ('el enumerate dentro ')
    print (idxob, r)
    # This is  into the for loop is to avoid doing rotations between a LMO
    # which is HOMO with itself.
    #
    #
    # Uncomment this line for debugging
    print ([str(r[0][1]), str(r[1][1])], str(r[0][0]), str(tno))
    #
    if str(r[0][1]) not in listica and str(r[1][1]) not in listica:
         if str(r[0][0]) !=  str(tno):
             # Uncomment these two lines for debugging
             # print ('! Localized MO between Atom ' + str(r[0][1]) + '    and Atom ' + str(r[1][1]))
             # print ('{merge,2104.2; orbital,2103.2; move; rotate,' + str(r[0][0]) + '.1,' + str(tno) + '.1; }')
             molpro.write('! Localized MO between Atom ' + str(r[0][1]) + ' and Atom ' + str(r[1][1]) + '\n')
             molpro.write('{merge,2104.2; orbital,2103.2; move; rotate,' + str(r[0][0]) + '.1,' + str(tno) + '.1;}' + '\n')
         else:
             molpro.write('! Localized MO between Atom ' + str(r[0][1]) + ' and Atom ' + str(r[1][1]) + '\n')
             molpro.write('{merge,2104.2; orbital,2103.2; move;}' + '\n')
             #molpro.write('' + '\n')
         if casans in yes:
             molpro.write('{multi; orbital,2104.2; closed,' + corb + '; occ,'+ occorb +'; frozen,' + frozorb +',2104.2;' + wf + '; canorb,2105.2;}' + '\n')
             molpro.write('{ccsd(t); orbital,2105.2; occ,'+ occorb +'; core,' + frozorb + '; ' + wf + ';}' + '\n')
             molpro.write('einc__' + str(idxob) + '__' + str(r[0][1]) + '_' + str(r[1][1]) + '=energy-ehf;' + '\n')
             molpro.write('' + '\n')
         else:
             molpro.write('' + '\n')

         # This is going to be an index
         #      iteraction  +   atom1    +    atom2  +  orbital
         onebody.append([str(idxob),str(r[0][1]),str(r[1][1]),str(r[0][0])])
         twobody.append(([r[0][1], r[1][1]], r[0][0]))

onebodytwo=onebody


print ('Index built for one body calculations')
print (onebody)

print('One body interactions have been written in file molpro.in')

"""
TWO BODY INTERACTIONS
"""
# This list is taken from the twobody.append()
print ('Printing two body')
print (twobody)

print ('')
print ('')
print ('')
print ('')
permuta=list(it.permutations(twobody,2)) # Permutations are in place as well.
combina=list(it.combinations(twobody,2))
print ('')
#print (permuta)
#print (len(permuta))

print ('Printing the two body combinations')
print (combina)
#print (len(combina))

print ('There are ' + str(len(combina)) + ' possible combinations')

"""
This section allows to discard atoms that by symmetry reason their energies are
equivalent. Please, see the README.md file for more information.
"""


atdiscard=[] # List of atoms to be discarded
combdel=[]   # List of items to be deleted from list combina are built from the
             # loop shown below. Initialization.

print ('Would you like to discard atoms by symmetry? [Default answer: no]')
yes = set(['yes','y', 'ye', 'Yes', 'Ye', 'Y'])
answer=raw_input()
if answer in yes:
    print ('Enter the atoms to be discarded as shown below:')
    print ('eg. 1,2,3,4')
    print ('Note: Only carbon atoms are taken into account')
    atdiscard = raw_input().split(",")
    print (atdiscard)
    atdiscard = map(int, atdiscard) # Convert list of strings to lists of integers
    print (atdiscard)

for idx,item in enumerate(combina):
    print combina[idx][0][0], combina[idx][1][0]
    for discad in atdiscard:
        if discad in combina[idx][0][0] or discad in combina[idx][1][0]:
            idx
            print idx
            print 'Element of the list to be deleted'
            print combina[idx]
            combdel.append(combina[idx])
            break
            #print ('Elemento eliminado')
            #print (combina.pop(final))

print ('combdel')
print combdel
print len(combdel)

"""
This is for deleting the atoms declared in atdiscard[]
"""
for i in combdel:
    combina.remove(i)
print ('New combina')

print combina
print len(combina)

"""
tno-1 to do rotations
"""
tnom=int(tno)-1


#print (tnom)
molpro2=open('molpro2.in','w')
molpro2.write('\n \n')
molpro2.write('!TWO BODY CALCULATIONS \n \n')

for i in combina:
#       if i[0][1] < i[1][1]:
#           print ('true')
#       else:
#           print ('false')

    if str(i[0][1]) !=  str(tnom) and str(i[1][1]) != str(tno):
        """
        Uncomment to debug  the if shown above
        """
        #molpro2.write('If first case \n')
        #molpro2.write('str(i[0][1]),str(tnom), str(i[1][1]), str(tno) \n')
        #print (i)
        molpro2.write('! first if LMO interactions between bond ' + str(i[0][0]) + ' and bond ' + str(i[1][0]) + '\n')
        molpro2.write('{merge,2104.2; orbital,2103.2; move; rotate,' + str(i[0][1]) + '.1,' + str(tnom) + '.1; rotate,'+str(i[1][1]) +'.1,'+ str(tno) +  '.1;}' '\n')

        print ('This is a test for the first if')
        print ('First bond')
        print ([str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])])
        idxfcfb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])) == (ss[1],ss[2],ss[3])]
        for ifcfb in idxfcfb:
            print (onebody[ifcfb])
            onebody1if1b=onebody[ifcfb]

        print ('Second bond')
        print ([str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])])
        idxfcsb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])) == (ss[1],ss[2],ss[3])]
        for ifcsb in idxfcsb:
            print (onebody[ifcsb])
            onebody1if2b=onebody[ifcsb]
    elif str(i[0][1]) ==  str(tnom) and str(i[1][1]) == str(tno):
        #print (i)
        #molpro2.write('If second case \n')
        molpro2.write('! second if LMO interactions between bond ' + str(i[0][0]) + ' and bond ' + str(i[1][0]) + '\n')
        molpro2.write('{merge,2104.2; orbital,2103.2; move; }' '\n')
        molpro2.write('' + '\n')

        print ('This is a test for the second if')
        print ('First bond')
        print ([str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])])
        idx2fcfb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])) == (ss[1],ss[2],ss[3])]
        for i2fcfb in idx2fcfb:
            print (onebody[i2fcfb])
            onebody1if1b=onebody[i2fcfb]

        print ('Second bond')
        print ([str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])])
        idx2fcsb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])) == (ss[1],ss[2],ss[3])]
        for i2fcsb in idx2fcsb:
            print (onebody[i2fcsb])
            onebody1if2b=onebody[i2fcsb]
    else:
        #molpro2.write('If third case \n')
        molpro2.write('! third if LMO interactions between bond ' + str(i[0][0]) + ' and bond ' + str(i[1][0]) + '\n')
        molpro2.write('' + '\n')
        molpro2.write('{merge,2104.2; orbital,2103.2; move; rotate,' + str(i[0][1]) + '.1,' + str(tnom) + '.1;}' '\n')

        print ('This is a test for the third if')
        print ('First bond')
        print ([str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])])
        idx3fcfb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[0][0][0]),str(i[0][0][1]),str(i[0][1])) == (ss[1],ss[2],ss[3])]
        for i3fcfb in idx3fcfb:
            print (onebody[i3fcfb])
            onebody1if1b=onebody[i3fcfb]

        print ('Second bond')
        print ([str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])])
        idx3fcsb = [zz for zz, ss in enumerate(onebodytwo) if (str(i[1][0][0]),str(i[1][0][1]),str(i[1][1])) == (ss[1],ss[2],ss[3])]
        for i3fcsb in idx3fcsb:
            print (onebody[i3fcsb])
            onebody1if2b=onebody[i3fcsb]

    # This is added to do the casscf part of the input
    if casans in yes:
        """
        corb-1 to do casscf input
        frozorb-1 to do casscf input
        """
        corbcas=int(corb)-1
        frozorbcas=int(frozorb)-1
        molpro2.write('{multi; orbital,2104.2; closed,' + str(corbcas) + '; occ,'+ str(occorb) +'; frozen,' + str(frozorbcas) +',2104.2;' + wf + '; canorb,2105.2;}' + '\n')
        molpro2.write('{ccsd(t); orbital,2105.2; occ,'+ str(occorb) +'; core,' + str(frozorbcas) + '; ' + wf + ';}' + '\n')

        molpro2.write('einc2b_' + str(i[0][0]) + '-' + str(i[1][0])
                + '=energy-ehf'
                + '-'
                + 'einc__'+str(onebody1if1b[0])+'__'+str(onebody1if1b[1])+'_'+str(onebody1if1b[2])
                + '-'
                + 'einc__'+str(onebody1if2b[0])+'__'+str(onebody1if2b[1])+'_'+str(onebody1if2b[2])
                + ';' + '\n')
        molpro2.write('' + '\n')
    else:
        molpro2.write('' + '\n')


print('Two body interactions written to file molpro2.in')

"""
In this part, files are cleaned. If you want to let them, then you can comment
all this section.
"""

import os
# Files related to the coordinates
os.popen('rm -f coordvout coordv coord coordbarray')

# Files related to the center of charges
os.popen('rm -f coc cocbarray cocsvout cocsv cocbarrayr cocbarraycoc')
