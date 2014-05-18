TODO
====

1. Make the program more general, because it only works for C-H structures with
   distance ranges between 2.3 and 2.7 Å. However, users can modify these
   values in the script if desired.
- Put a verbose argument to print every process done.
- Help to prepare input file to add electron correlation methods to the CASSCF
  calculation.
- Port it to Python 3.4.
- Avoid writing two body interactions between same bond (given that
  combinations are taken into account).
- Make the use of an input file instead of interactive mode.

### Done
- Strip atoms not desired. `Done`
- Allow deleting parts of the molecules. This is useful to avoid repeating the
  same calculations when exploiting the molecular symmetry `Done`.
