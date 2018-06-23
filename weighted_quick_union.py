#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 19:34:32 2018

@author: gtucker
"""

import numpy as np


class WeightedQuickUnion(object):
    """Implementation class for Weighted Quick Union algorithm (with PC).
    
    Examples
    --------
    The following example sequence of union operations is from the
    demonstration in Sedgewick and Wayne's Algorithms course.

    >>> wqu = WeightedQuickUnion(10)
    >>> wqu.id
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> wqu.connected(4, 5)
    False
    >>> wqu.union(4, 3)
    >>> wqu.id
    array([0, 1, 2, 4, 4, 5, 6, 7, 8, 9])
    >>> wqu.union(3, 8)
    >>> wqu.id
    array([0, 1, 2, 4, 4, 5, 6, 7, 4, 9])
    >>> wqu.union(6, 5)
    >>> wqu.id
    array([0, 1, 2, 4, 4, 6, 6, 7, 4, 9])
    >>> wqu.union(9, 4)
    >>> wqu.id
    array([0, 1, 2, 4, 4, 6, 6, 7, 4, 4])
    >>> wqu.union(2, 1)
    >>> wqu.id
    array([0, 2, 2, 4, 4, 6, 6, 7, 4, 4])
    >>> wqu.union(5, 0)
    >>> wqu.id
    array([6, 2, 2, 4, 4, 6, 6, 7, 4, 4])
    >>> wqu.union(7, 2)
    >>> wqu.id
    array([6, 2, 2, 4, 4, 6, 6, 2, 4, 4])
    >>> wqu.union(6, 1)
    >>> wqu.id
    array([6, 2, 6, 4, 4, 6, 6, 2, 4, 4])
    >>> wqu.union(7, 3)
    >>> wqu.id  # Note: path compression changes ID 7 from 2 to 6
    array([6, 2, 6, 4, 6, 6, 6, 6, 4, 4])
    >>> wqu.connected(4, 5)
    True
    >>> wqu.reset()
    >>> wqu.id
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    """

    def __init__(self, n):
        """Initialize id and sz arrays."""
        self.id = np.arange(n, dtype=np.int)
        self.sz = np.ones(n, dtype=np.int)
        
    def root(self, i):
        """Return the root of the group to which element i belongs."""
        while i != self.id[i]:
            self.id[i] = self.id[self.id[i]]  # path compression ("PC")
            i = self.id[i]
        return i

    def connected(self, p, q):
        """Return True if p and q are in the same group; False otherwise."""
        return self.root(p) == self.root(q)

    def union(self, p, q):
        """Join p and q."""
        if p == q:
            return
        i = self.root(p)
        j = self.root(q)
        if self.sz[i] < self.sz[j]:  # join the smaller to the larger
            self.id[i] = j
            self.sz[j] += self.sz[i]
        else:
            self.id[j] = i
            self.sz[i] += self.sz[j]

    def reset(self):
        """Reset id and sz arrays."""
        self.id[:] = np.arange(self.id.size, dtype=int)
        self.sz[:] = 1
