#!/usr/bin/env python

# Beginning of Chinese Range: 11904 (traditional), 19968 (simplified?)

for i in range(1, 100000):
    s = '\\u%04x'%(i,)
    print(' ', chr(i), ' ', i, s)

