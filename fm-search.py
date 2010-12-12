#!/usr/bin/python
import os
from os.path import join, abspath, isfile, isdir, exists, basename
import sys
import fmindex

def main():
    if not len(sys.argv) in [3]:
        print 'Usage: '
        print '  %s index search_string' % sys.argv[0]
        os.abort()
    else:
        if not isfile(sys.argv[1]):
            print "Index file doesn't exist"
            os.abort()
        
        inp = open(sys.argv[1])
        
        idx = fmindex.load(inp)
        print "count:"
        print str(idx.count(sys.argv[2]))
        print "matches:"
        print str(idx.search(sys.argv[2]))

if __name__ == '__main__':
    main()