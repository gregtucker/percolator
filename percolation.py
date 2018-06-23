#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 17 15:08:09 2018

@author: gtucker
"""

import sys
import numpy as np
from weighted_quick_union import WeightedQuickUnion


class Percolator(object):
    """Implements percolation algorithm in Algorithms Week1."""
    
    def __init__(self, n):
        """Set up an n x n grid of sites, initially all closed.
        
        Parameters
        ----------
        n : int
            length of one side of grid
        
        Examples
        --------
        >>> p = Percolator(2)
        >>> p.n
        2
        >>> p.cell_state.size
        4
        
        Notes
        -----
        Make array (n x n) + 2, with the extra two sites representing the 
        'master' points below (n*n) and above (n*n+1) the grid.
             Create two WeightedQuickUnion objects: one will connect open cells
        along the bottom row to the extra bottom cell. This one is used to 
        test for percolation. The other will not connect to the extra bottom
        cell; this one will be used to establish whether cells are full or not.
        This strategy prevents "backwash" through the extra bottom cell.
        """
        if n <= 0:
            raise ValueError
        self.n = n
        self.cell_state = np.zeros(n*n, dtype=bool)
        self.wqu = WeightedQuickUnion(n*n+2)
        self.wqu_connected = WeightedQuickUnion(n*n+2)
        self.extra_bottom_cell = n * n
        self.extra_top_cell = self.extra_bottom_cell + 1

    def _row_col_to_id(self, row, col):
        """Return array ID equivalent to given row, col.
        
        Examples
        --------
        >>> p = Percolator(2)
        >>> p._row_col_to_id(1, 1)
        0
        >>> p._row_col_to_id(1, 2)
        1
        >>> p._row_col_to_id(2, 1)
        2
        >>> p._row_col_to_id(2, 2)
        3
        """
        return (row - 1) * self.n + col - 1 

    def open(self, row, col):
        """Convert cell (row, col) to Open state and connect to neighbors.

        Examples
        --------
        >>> p = Percolator(3)
        >>> p.open(3, 1)  # lower left
        >>> p.wqu.connected(6, 9)  # wqu not connected to extra bottom cell...
        False
        >>> p.wqu_connected.connected(6, 9)  # but wqu_connected is
        True
        >>> p.wqu.connected(6, 7)  # not connected to closed neighbor to right
        False
        >>> p.open(1, 2)  # top middle
        >>> p.wqu.connected(1, 10) # now connected to extra top cell
        True
        >>> p.wqu.connected(1, 4)  # not connected to neighbor below
        False
        >>> p.open(3, 2)
        >>> p.wqu.connected(6, 7)  # now (3,1) and (3,2) are connected
        True
        >>> p.open(2, 2)
        >>> p.wqu.connected(4, 6)  # should connect to (3, 1) via (3, 2)
        True
        >>> p.percolates()
        True
        """
        if not self.is_open(row, col):
            cell = self._row_col_to_id(row, col)
            self.cell_state[cell] = True  # open it
            if col > 1:  # left
                if self.is_open(row, col - 1):
                    nbr = self._row_col_to_id(row, col - 1)
                    self.wqu.union(cell, nbr)
                    self.wqu_connected.union(cell, nbr)
            if col < self.n:  # right
                if self.is_open(row, col + 1):
                    nbr = self._row_col_to_id(row, col + 1)
                    if not self.wqu.connected(cell, nbr):
                        self.wqu.union(cell, nbr)
                        self.wqu_connected.union(cell, nbr)
            if row > 1: # above
                if self.is_open(row - 1, col):
                    nbr = self._row_col_to_id(row - 1, col)
                    if not self.wqu.connected(cell, nbr):
                        self.wqu.union(cell, nbr)
                        self.wqu_connected.union(cell, nbr)
            if row < self.n:  # below
                if self.is_open(row + 1, col):
                    nbr = self._row_col_to_id(row + 1, col)
                    if not self.wqu.connected(cell, nbr):
                        self.wqu.union(cell, nbr)
                        self.wqu_connected.union(cell, nbr)

            print('\n')
            print(self.wqu_connected.sz)
            if row == 1:  # top row: attach to extra top cell
                if not self.wqu.connected(self.extra_top_cell, cell):
                    self.wqu.union(self.extra_top_cell, cell)
                    print(self.wqu_connected.connected(self.extra_top_cell, cell))
                    self.wqu_connected.union(self.extra_top_cell, cell)
            if row == self.n:  # bottom row: attach to extra bottom cell
                if not self.wqu_connected.connected(self.extra_bottom_cell, cell):
                    self.wqu_connected.union(self.extra_bottom_cell, cell)
            print(self.wqu_connected.sz)

    def is_open(self, row, col):
        """Return True if cell (row, col) is open, False otherwise."""
        return self.cell_state[self._row_col_to_id(row, col)]

    def is_full(self, row, col):
        """Return True if cell (row, col) is full, False otherwise.
        
        Notes
        -----
        A cell is full if it is both open and connected to the extra top cell.
        The test for being open is needed because cells on the top row are
        connected to the top cell from the start, even if they are closed.
        
        Examples
        --------
        >>> p = Percolator(2)
        >>> p.is_full(2, 1)
        False
        >>> p = Percolator(3)
        >>> p.open(1, 1)
        >>> p.is_full(1, 1)
        True
        >>> p.open(3, 1)
        >>> p.is_full(3, 1)
        False
        >>> p.open(2, 1)
        >>> p.is_full(3, 1)
        True
        >>> p.open(3, 3)
        >>> p.is_full(3, 3)  # NOT full, because no back-wash
        False
        """
        return (self.is_open(row, col)
                and self.wqu.connected(self._row_col_to_id(row, col),
                                       self.extra_top_cell))

    def number_of_open_sites(self):
        """Return number of open sites.
        
        Examples
        --------
        >>> p = Percolator(2)
        >>> p.open(1, 1)
        >>> p.open(2, 2)
        >>> p.number_of_open_sites()
        2
        """
        return np.sum(self.cell_state)

    def percolates(self):
        """Return True if lattice percolates, False otherwise.

        Examples
        --------
        >>> p = Percolator(3)
        >>> p.open(1, 1)
        >>> p.open(2, 2)
        >>> p.open(3, 3)
        >>> p.percolates()
        False
        >>> p.open(1, 2)
        >>> p.percolates()
        False
        >>> p.open(2, 3)
        >>> p.percolates()
        True
        """
        return self.wqu_connected.connected(self.extra_bottom_cell,
                                            self.extra_top_cell)

    def reset(self):
        """Reset data structures for a new run."""
        self.cell_state[:] = False
        self.wqu.reset()
        self.wqu_connected.reset()


def main():
    """Instantiate and run a Percolator"""
    try:
        n = sys.argv[1]
    except:
        n = 4
        
    import doctest
    doctest.testmod()
        
    p = Percolator(n)
    print(p.cell_state)


if __name__ == '__main__':
    main()

    