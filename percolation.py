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
        """
        if n <= 0:
            raise ValueError
        self.n = n
        self.cell_state = np.zeros(n*n, dtype=bool)
        self.wqu = WeightedQuickUnion(n*n+2)
        self.extra_bottom_cell = n * n
        self.extra_top_cell = self.extra_bottom_cell + 1
        #self._connect_extra_top_and_bottom_cells()

#    def _connect_extra_top_and_bottom_cells(self):
#        """Connect cells in bottom & top rows to extra bottom & top cell.
#        
#        Notes
#        -----
#        We introduce an extra cell 'below' the grid, and an extra one 'above',
#        in order to easily test whether the lattice percolates: if these top
#        and bottom cells are connected, then the whole lattice percolates.
#
#        Examples
#        --------
#        >>> p = Percolator(2)
#        >>> p.wqu.connected(0, 4)
#        True
#        >>> p.wqu.connected(3, 5)
#        True
#        >>> p.wqu.connected(0, 2)
#        False
#        >>> p.wqu.connected(0, 5)
#        False
#        >>> p.wqu.id
#        array([4, 4, 5, 5, 4, 5])
#        >>> p.wqu.sz
#        array([1, 1, 1, 1, 3, 3])
#        """
#        self.extra_bottom_cell = self.n ** 2
#        self.extra_top_cell = self.extra_bottom_cell + 1
#        offset = self.n * (self.n - 1)
#        for i in range(self.n):
#            self.wqu.union(self.extra_bottom_cell, i)
#            self.wqu.union(self.extra_top_cell, i + offset)

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
        >>> p.open(1, 1)
        >>> p.wqu.connected(0, 9)  # now connected to extra bottom cell
        True
        >>> p.wqu.connected(0, 1)  # not connected to closed neighbor to right
        False
        >>> p.open(3, 2)
        >>> p.wqu.connected(7, 10) # now connected to extra top cell
        True
        >>> p.wqu.connected(7, 4)  # not connected to neighbor below
        False
        >>> p.open(1, 2)
        >>> p.wqu.connected(0, 1)  # now (1,1) and (1,2) are connected
        True
        >>> p.open(2, 2)
        >>> p.wqu.connected(4, 0)  # should connect to (1, 1) via (1, 2)
        True
        >>> p.percolates()
        True
        """
        #TODO: flip top and bottom
        if not self.is_open(row, col):
            cell = self._row_col_to_id(row, col)
            self.cell_state[cell] = True  # open it
            if col > 1:  # left
                if self.is_open(row, col - 1):
                    nbr = self._row_col_to_id(row, col - 1)
                    self.wqu.union(cell, nbr)
            if col < self.n:  # right
                if self.is_open(row, col + 1):
                    nbr = self._row_col_to_id(row, col + 1)
                    self.wqu.union(cell, nbr)
            if row == self.n:  # top row: attach to extra top cell
                self.wqu.union(self.extra_top_cell, cell)
            else: # above
                if self.is_open(row + 1, col):
                    nbr = self._row_col_to_id(row + 1, col)
                    self.wqu.union(cell, nbr)
            if row == 1:  # bottom row: attach to extra bottom cell
                self.wqu.union(self.extra_bottom_cell, cell)
            else:  # below
                if self.is_open(row - 1, col):
                    nbr = self._row_col_to_id(row - 1, col)
                    self.wqu.union(cell, nbr)

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
        """
        # TODO: add more tests once open() works
        return (self.is_open(row, col)
                and self.wqu.connected(self._row_col_to_id(row, col),
                                       self.extra_top_cell))

    def number_of_open_sites(self):
        """Return number of open sites."""
        #TODO: ADD A TEST
        return np.sum(self.cell_state)

    def percolates(self):
        """Return True if lattice percolates, False otherwise."""
        #TODO: ADD A TEST
        return self.wqu.connected(self.extra_bottom_cell, self.extra_top_cell)

    
def test_perc():
    pass


def main():
    """Instantiate and run a Percolator"""
    try:
        n = sys.argv[1]
    except:
        n = 4
        
    p = Percolator(n)
    print(p.cell_state)


if __name__ == '__main__':
    main()

    