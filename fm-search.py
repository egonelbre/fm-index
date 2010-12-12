#!/usr/bin/python
import os
from os.path import join, abspath, isfile, isdir, exists, basename
import time

import sys
import fmindex
import tarfile

def diff_time(start, end):
    return int((end - start) * 1000)

def main():
    if not len(sys.argv) in [3]:
        print 'Usage: '
        print '  %s index search_string' % sys.argv[0]
        os.abort()
    else:
        if not isfile(sys.argv[1]):
            print "Index file doesn't exist"
            os.abort()
        
        tim = time.clock
        
        t_start = tim()
        
        idx = fmindex.load(sys.argv[1])
        t_load = tim()
        
        c = idx.count(sys.argv[2])
        t_count = tim()
        
        m = idx.search(sys.argv[2])
        t_search = time.clock()
        print "load: %sms" % diff_time(t_start, t_load)
        print "count: %sms" % diff_time(t_load, t_count)
        print str(c)
        print "matches: %sms" % diff_time(t_count, t_search)
        print str(m)
if __name__ == '__main__':
    main()