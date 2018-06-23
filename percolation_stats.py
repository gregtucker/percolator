#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:43:51 2018

@author: gtucker
"""

import sys
import numpy as np
from perc_tester import PercTester



class PercolationStats(object):
    """Generates lattice-percolation statistics by running perc models."""
    
    def __init__(self, n, trials):
        """Set up data structures."""
        self.n = n
        self.num_trials = trials
        self.pt = PercTester(n)
        self.perc_threshold = np.zeros(trials)
        
        # Create zero vals for stats, to avoid crash if someone calls mean etc.
        # before run
        self.mean_perc = 0.0
        self.std_perc = 0.0
        self.conf_lo = 0.0
        self.conf_hi = 0.0

    def mean(self):
        """Calculate and return mean threshold."""
        return self.mean_perc
    
    def stddev(self):
        """Calculate and return standard deviation of threshold."""
        return self.std_perc

    def confidenceLo(self):
        """Return lower 95% confidence interval."""
        return self.conf_lo

    def confidenceHi(self):
        """Return lower 95% confidence interval."""
        return self.conf_hi
    
    def calc_stats(self):
        """Calculate and store mean, std, and confidence intervals."""
        self.mean_perc = np.mean(self.perc_threshold)
        self.std_perc = np.std(self.perc_threshold)
        root_T = self.num_trials ** 0.5
        two_sig_t = 1.96 * self.std_perc / root_T
        self.conf_lo = self.mean_perc - two_sig_t
        self.conf_hi = self.mean_perc + two_sig_t

    def run(self):
        """Run T trials up to perc point, recording perc val for each.
        Then calc and store stats."""
        for t in range(self.num_trials):
            self.perc_threshold[t] = self.pt.run_to_percolation()
            self.pt.reset(seed=t+1)
        self.calc_stats()


def main(args):
    """Instantiate and run PercolationStats, and report results."""
    try:
        n = args[1]
        T = args[2]
    except:
        n = 20
        T = 30

    ps = PercolationStats(n, T)
    ps.run()
    print('\nAll vals:')
    print(ps.perc_threshold)
    print('\nMean = ' + str(ps.mean()))
    print('Std dev = ' + str(ps.stddev()))
    print('Lower 95% = ' + str(ps.confidenceLo()))
    print('Upper 95% = ' + str(ps.confidenceHi()))


if __name__ == '__main__':
    main(sys.argv)
    