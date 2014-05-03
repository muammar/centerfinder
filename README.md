centerfinder
============

This python script intends to look for localized molecular orbitals (LMO) near
to atoms based on the center of charges and prepare a MOLPRO input file in
order to perform later incremental calculations as stated in _H. Stoll, Chem.
Phys. Lett., 1992, 19_. This is normally a very tedious work to be done by
hand, and it's there when centerfinder comes to help.

It reads your MOLPRO output file, and then it extracts coordinates and center
of charges to then print which LMO are in between which atoms in the molecule.
In your MOLPRO output file, a localization calculation must have been done
beforehand. Take into account that your calculation has to be done using the
`symmetry,nosym;` card in MOLPRO. On the other hand, you have to save your LMO
to the record `2103.2`. Below, an example of the `locali block` in MOLPRO to be
used to run this program:

```
{locali;
save,2103.2;
core,10;
group,28.1,31.1,-34.1;
group,11.1,-27.1,29.1,30.1;
}
```

*Note:* The script prepares two input files with the rotations needed to do
one- and two- body interactions, as well as the CASSCF and CCSD input. I will
generalize more this script in the coming time.

## Requirements

In order to run this script, you need to install in your system:

- Python 2.7 (I am porting this to work with Python >3)
- NumPy.
- SciPy.

You can use `pip` to install them or the package manager of your favorite Linux
distribution or Mac OS X.

## How to use it

### Installation and execution

Clone this git repository:

```bash
$ git clone https://github.com/muammar/centerfinder.git
```

Then you excute the program as follows:

```bash
$ python $PATH/centerfinder/centers.py $input
```
Where `$input` is the name of your MOLPRO output file. The program will ask you:

1. Number of CORE MOs used in your calculation for doing the localization.
- Number of Localized Molecular orbitals.

Then, for the CASSCF calculation section it will ask you:

3. Number of CLOSED MOs.
- Number of FROZEN MOs.
- Number of OCCUPIED MOs.
- The wavefunction in the format: `wf,#electrons,Sym,Multiplicity`.

Finally, a `molpro.in` and `molpro2.in` files will be created at the end of the
execution. Please *note* that in MOLPRO you can only run maximum of about `100`
calculations per input file.

### How to update it?

To update this program, just do a `git pull` in your `$PATH/centerfinder/`
folder.

## Feedback?

This is my first program, if it can be called like that, written in python. So,
I'm sure it is not optimal at all. However, you can send to me
[suggestions, and improvements](https://github.com/muammar/centerfinder/issues).
They are very welcome.
