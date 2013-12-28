centerfinder
============

This python script intends to look for localized molecular orbitals (LMO) near
to atoms based on the center of charges in order to perform later incremental
calculations as stated in _H. Stoll, Chem. Phys. Lett., 1992, 19_.

It reads your MOLPRO output file, and then it extracts coordinates and center
of charges to then print which LMO are in between which atoms in the molecule.
In your MOLPRO output file, a localization calculation must have been done
beforehand. The script will ask you two questions:

- Number of CORE MOs used in your calculation for doing the localization.
- Number of Localized Molecular orbitals.


*Note:* As for now, the script only prints the rotations needed to do one body
interactions. In any time soon, it will do more than one body interactions and
prepare the CASSCF input file.

## Requirements

In order to run this script, you need to install in your system:

    * NumPy.
    * SciPy.

You can use `pip` to install them or the package manager of your favorite Linux
distribution or Mac OS X.

## How to use it

```bash

$ git clone https://github.com/muammar/centerfinder.git
$ cd centerfinder
$ python centers.py
```

The program will also ask you how many *core* molecular orbitals you have used
in your MOLPRO input file.

## Feedback?

This is my first program, if it can be called like that, written in python. So,
I'm sure it is not optimal at all. However, you can send to me
[suggestions, and improvements](https://github.com/muammar/centerfinder/issues).
They are very welcome.
