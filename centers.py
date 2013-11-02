#!/usr/bin/env python

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

"""
Lists are created to be treated later.
"""
import simplejson
with open('coord') as inf, open('coordlst','w') as outfile:
    for line in inf:
        parts = line.split() # split line into parts
        if len(parts) > 1:   # if at least 2 parts/columns
            #print parts[3], parts[4], parts[5]
            coordvec=[parts[3],parts[4],parts[5]]
            #print coordvec
            simplejson.dump(coordvec, outfile)
            outfile.close


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

with open('coc') as inf, open('coclst', 'w') as outfile:
    for line in inf:
        parts = line.split() # split line into parts
        if len(parts) > 1:   # if at least 2 parts/columns
            #print parts[2], parts[3], parts[4]
            cocvec=[ parts[2], parts[3], parts[4]]
            print cocvec
            simplejson.dump(cocvec, outfile)
            outfile.close

