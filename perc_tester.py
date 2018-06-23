#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 20:22:37 2018

@author: gtucker
"""

import sys
import numpy as np
from percolation import Percolator


FULL = 1  # code for full cell in 'cell' array, used for plotting (only)


class PercTester(object):
    """A PercTester implements testing of percolation on a square lattice with
    iterative opening of randomly selected cells."""
    
    def __init__(self, n, plot_interval=0, seed=0):
        """Initialize the PercTester."""
        self.p = Percolator(n)
        self.n = n
        self.closed_cells = np.arange(n*n)
        self.num_closed_cells = n * n
        np.random.seed(seed)

        self.plot_interval = plot_interval
        if plot_interval > 0:
            self.cell = np.zeros((n, n), dtype=int)

    def _pick_random_closed_cell(self):
        """Choose a closed cell at random and return its row and column.
        
        Notes
        -----
        Assumes valid cells are those in indices < num_closed_cells. To help
        ensure this, swaps contents of chosen index with the last valid index.

        Examples
        --------
        >>> pt = PercTester(2)
        >>> pt.closed_cells
        array([0, 1, 2, 3])
        >>> pt._pick_random_closed_cell()
        (1, 1)
        >>> pt.closed_cells
        array([3, 1, 2, 0])
        """
        r = np.random.randint(self.num_closed_cells)
        cell_id = self.closed_cells[r]

        # swap the id at r with the id at num_closed_cells
        self.closed_cells[r] = self.closed_cells[self.num_closed_cells - 1]
        self.closed_cells[self.num_closed_cells - 1] = cell_id

        return self._cell_id_to_row_col(cell_id)
    
    def _cell_id_to_row_col(self, cell_id):
        """Return cell id corresponding to a given row and column.

        Examples
        --------
        >>> pt = PercTester(2)
        >>> pt._cell_id_to_row_col(0)
        (1, 1)
        >>> pt._cell_id_to_row_col(1)
        (1, 2)
        >>> pt._cell_id_to_row_col(2)
        (2, 1)
        >>> pt._cell_id_to_row_col(3)
        (2, 2)
        """
        row = (cell_id // self.n) + 1
        col = (cell_id % self.n) + 1
        return row, col

    def run(self):
        """Run the perc tester once through, opening cells one at a time at
        random locations until lattice is fully open."""
        first_perc = 0
        
        if self.plot_interval > 0:
            self.plot_lattice()
            next_plot = self.plot_interval
        else:
            next_plot = self.n * self.n
        for i in range(self.n * self.n):
            
            (r, c) = self._pick_random_closed_cell()
            self.p.open(r, c)
            self.num_closed_cells -= 1
            
            if i == next_plot:
                print('Lattice with ' + str(i + 1) + ' open sites:')
                self.plot_lattice()
                next_plot += self.plot_interval
                
            if first_perc == 0 and self.p.percolates():
                first_perc = i
                print('Percolates after ' + str(i + 1) + ' openings ('
                      + str(100.0 * float(i)/(self.n * self.n)) + '%).')
                print('\n')

    def run_to_percolation(self):
        """Run the perc tester once through, opening cells one at a time at
        random locations until percolation occurs.
        
        Returns
        -------
        float : proportion of cells open at percolation.
        
        Examples
        --------
        >>> pt = PercTester(8)
        >>> round(100 * pt.run_to_percolation())
        73.0
        """
        num_open = 0.0

        while not self.p.percolates():
            
            (r, c) = self._pick_random_closed_cell()
            self.p.open(r, c)
            self.num_closed_cells -= 1
            num_open += 1

        return num_open / (self.n * self.n)

    def map_full_cells(self):
        """Identify full cells in self.cell array and assign a code of 2."""
        for r in range(self.n):
            for c in range(self.n):
                if self.p.is_open(r+1, c+1) and self.p.is_full(r+1, c+1):
                    self.cell[r,c] = FULL
    
    def plot_lattice(self):
        """Plot the lattice, showing closed, open, and full cells."""
        import matplotlib.pyplot as plt
        
        self.cell[:] = 2 * self.p.cell_state.reshape(n, n)
        self.map_full_cells()

        plt.clf()
        plt.imshow(self.cell, vmin=0, vmax=2)
        plt.show()
    
    def reset(self, seed=0):
        """Reset PercTester and Percolator for a new run."""
        self.closed_cells = np.arange(n*n)
        self.num_closed_cells = n * n
        np.random.seed(seed)
        self.p.reset()

if __name__ == '__main__':
    
    import doctest
    doctest.testmod()

    try:
        n = sys.argv[1]
    except:
        n = 8
        
    pt = PercTester(n, plot_interval=1)
    pt.run()
    perc_thresh = pt.run_to_percolation()
    print('Percolation threshold = ' + str(perc_thresh))

        