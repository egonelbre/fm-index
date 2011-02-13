#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import random
import string
import time

import bwt

def sampler(alphabet, count):
    return [random.choice(alphabet) for _ in xrange(count)]

class Test_BWT_Simple(unittest.TestCase):
    TEST_STRINGS = [ 'abracdabra', '', 'abcdefghijklmnopqrstuvw',
                     'ACGACTGCGAGCTCGA', 'a', 'aa', 'aaaaa', 'aaabb']
    
    def setUp(self):
        self.bw = self.getBW()
        self.start = time.time()
    
    def getBW(self):
        return bwt.BurrowsWheeler()
    
    def tearDown(self):
        self.stop = time.time()
        print str(int((self.stop - self.start) * 1000)) + 'ms'
        
    def do_test_string(self, s):
        ts = self.bw.transform(s)
        ns = self.bw.inverse(ts)
        self.assertEqual(s, ns)
    
    def test_fixed(self):
        for s in self.TEST_STRINGS:
            self.do_test_string(s)
    
    def do_test_random(self, alpha, min = 3, max = 100, times = 30):
        for _ in xrange(times):
            x = sampler(alpha, random.randint(min,max))
            self.do_test_string(''.join(x))
            
    def test_dna(self):
        self.do_test_random('ACGT')
    
    def test_letters(self):
        self.do_test_random(string.letters)
    
    def test_alphanum(self):
        self.do_test_random(string.letters + string.digits)

class Test_BWT_SuffixTree(Test_BWT_Simple):
    def getBW(self):
        return bwt.SuffixTreeBurrowsWheeler()

class Test_BWT_SuffixArray(Test_BWT_Simple):
    def getBW(self):
        return bwt.SuffixArrayBurrowsWheeler()

class Test_BWT_Fast(Test_BWT_Simple):
    def getBW(self):
        return bwt.FastBurrowsWheeler()

class Test_BWT_Checkpointing(Test_BWT_Simple):
    def getBW(self):
        return bwt.CheckpointingBurrowsWheeler()

if __name__ == '__main__':
    unittest.main(argv = unittest.sys.argv + ['--verbose'])