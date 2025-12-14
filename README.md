# AoC 2025

## Summary

### -- Day 1: Secret Entrance ---
Tw way dial, count passing zero. Tricky corner cases in part B for a day 1 puzzle. 
Zero to zero not in example and could easily put people in the horrible place of example passes, but my data fails

### --- Day 2: Gift Shop ---
If string == repeated tokens then invalid: 

### --- Day 3: Lobby ---
Largest jolt: find the largest n-digit number.
Early show of a recursion problem

### --- Day 4: Printing Department ---
2D grid simulation, reduce until no more @ can be removed

### --- Day 5: Cafeteria ---
Interval ranges over large space 1D. Find the union.

### --- Day 6: Trash Compactor ---
Fiddly parsing problem, values written vertically, read from the right

### --- Day 7: Laboratories ---
Process each row to know where beams are and how many splitters are hit
Nice double recursion in part B using memoise for performance

### --- Day 8: Playground ---
Union-find approach merge circuit as connections are addd

### --- Day 9: Movie Theater ---
Find the largest rectangle within the boundary, since the corners would always be on the boundary there were no corner cases
Just test for overlapping boundary excluding limits

### --- Day 10: Factory ---
Joltages!! a) Powerset b) Reduce equations using row echelon form to form a narrower set of possibilities 

### --- Day 11: Reactor ---
DAG: a) total paths b) Refine recursion to accumulate and with and without totals

### --- Day 12: Christmas Tree Farm ---
Taskmaster packing problem - not a problem if you so some basic checks first (slap face)
But the DFS will work if need be :-)
