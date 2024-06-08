# BBWT reachability

This code computationally checks with exhaustive search for sufficiently small alphabet sizes and short strings the conjecture that two strings with the same Parikh vector can be mapped to each other using only a sequence of bijective Burrows-Wheeler transforms and cyclic rotations.

- `reachability.py` runs exhaustive search for given alphabet size and string length
- `computepath.py` computes a shortest path from a string to another with the same Parikh vector on a graph whose edges represent BBWT or cyclic shift operations, which label the edges
- `findlexsmaller.py` computes a shortest path from a string to a lexicographically smaller string
