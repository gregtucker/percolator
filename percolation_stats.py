#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:43:51 2018

@author: gtucker
"""

import sys




class PercolationStats(object):
    """Generates lattice-percolation statistics by running perc models."""
    
    def __init__(self, n, trials):
        
        pass
    
    def mean(self):
        pass
    
    def stddev(self):
        pass

    def confidenceLo():
        pass

    def confidenceHi():
        pass

    def run(self):
        pass


def main(args):
    """Instantiate and run PercolationStats, and report results."""
    try:
        n = args[1]
        T = args[2]
    except:
        n = 4
        T = 10

    ps = PercolationStats(n, T)
    ps.run()


if __name__ == '__main__':
    main(sys.argv)
    