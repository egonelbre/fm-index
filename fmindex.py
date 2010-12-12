# -*- coding: utf-8 -*-

import pickle
import bwt

bw = bwt.BurrowsWheeler()

def save(idx, f):
    pickle.dump(idx,f)

def load(f):
    idx = pickle.load(f)
    return idx

def index(data):
    return FMSimpleIndex(data)
    #return FMFullIndex(data)

class FMSimpleIndex(object):   
    def __init__(self, data):
        self.orig = data
        self.data = bw.transform(data)
        self.offset = {}
        self.occ = {}
        self._build()
    
    def _build(self):
        self.occ = bwt.calc_first_occ(self.data)
    
    def _occ(self, idx, qc):
        c = self.occ.get(qc)
        if c == None:
            return 0
        return c
    
    def _count(self, idx, qc):
        if not qc in self.occ.keys(): return 0
        c = 0
        for i in xrange(idx):
            if self.data[i] == qc:
                c += 1
        return c
    
    def _lf(self, idx, qc):
        o = self._occ(idx, qc)
        c = self._count(idx, qc)
        return o + c
    
    def _walk(self, idx):
        # walk to the beginning using lf mapping
        # this is same as inverse of burrow wheeler transformation
        # from arbitrary location
        r = 0
        i = idx 
        while self.data[i] != bw.EOS:
            if self.offset.get(i):
                # we have cached the location and can use it
                r += self.offset[i]
                break
            r += 1
            i = self._lf(i, self.data[i])
        
        # save the offset of some idx for faster searches
        if not self.offset.get(idx):
            self.offset[i] = r
        return r
    
    def bounds(self, q):
        # find the appropriate suffixes
        top = 0
        bot = len(self.data)
        for i, qc in enumerate(q[::-1]):
            top = self._lf(top, qc)
            bot = self._lf(bot, qc)
            if top == bot: return (-1,-1)
        return (top,bot)
    
    def search(self, q):
        # find the suffixes for the query
        top, bot = self.bounds(q)
        matches = []
        # find the location of the suffixes
        # by walking the reverse text from that position
        # with lf mapping
        for i in range(top, bot):
            pos = self._walk(i)
            matches.append(pos)
        return sorted(matches)
    
    def count(self, q):
        top, bot = self.bounds(q)
        return bot - top

class FMFullIndex(FMSimpleIndex):
    """ creates full LF index for each letter, space inefficient """
    
    def __init__(self, data):
        self.orig = data
        self.data = bw.transform(data)
        self.offset = {}
        self.FM = None
        self._build()
    
    def _build(self):       
        occ = bwt.calc_first_occ(self.data)
        
        # FM Index
        FM = {}
        for i, c in enumerate(self.data):
            # we'll store the nearest LF mapping for each letter
            # space inefficient
            for x, v in occ.items():
                FM[(i,x)] = v
            FM[i] = occ[c]
            occ[c] += 1
        i = len(self.data)
        for x, v in occ.items():
            FM[(i,x)] = v
        del occ
        
        self.FM = FM
    
    def _lf(self, idx, qc):
        return self.FM[(idx,qc)]
    
    def _walk(self, idx):
        r = 0
        i = idx 
        while self.data[i] != bw.EOS:
            if self.offset.get(i):
                r += self.offset[i]
                break
            r += 1
            i = self.FM[i]
            
        if not self.offset.get(idx):
            self.offset[i] = r
        return r
    
class FMCheckpointing(FMSimpleIndex):
    """ creates full LF index for each letter, space inefficient """
    
    def __init__(self, data, step = 20):
        self.orig = data
        self.data = bw.transform(data)
        self.step = step
        self.offset = {}
        self.FM = None
        self._build()
    
    def _build(self):       
        occ = bwt.calc_first_occ()
        
        # FM Index
        FM = {}
        for i, c in enumerate(self.data):
            # we'll store the nearest LF mapping for each letter
            # space inefficient
            for x, v in occ.items():
                FM[(i,x)] = v
            FM[i] = occ[c]
            occ[c] += 1
        i = len(self.data)
        for x, v in occ.items():
            FM[(i,x)] = v
        del occ
        
        self.FM = FM
    
    def _lf(self, idx, qc):
        return self.FM[(idx,qc)]
    
    def _walk(self, idx):
        r = 0
        i = idx 
        while self.data[i] != bw.EOS:
            if self.offset.get(i):
                r += self.offset[i]
                break
            r += 1
            i = self.FM[i]
            
        if not self.offset.get(idx):
            self.offset[i] = r
        return r
    