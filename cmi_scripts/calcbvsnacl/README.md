# Calculate bond valence sums for NaCl

This example shows how to evaluate bond valence sums using the `diffpy.srreal`
module in DiffPy-CMI.  BVS calculator uses a standard set of bond valence
parameters obtained from a lookup table.  Bond valence parameters can be
set to custom values.  Multiple BVS calculator objects can be created,
where each one has separate lookup table and optionally different valence
parameters.
