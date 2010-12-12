# -*- coding: utf-8 -*-

import pickle
import bwt

bw = bwt.BurrowsWheeler()

def save(idx, f):
    pickle.dump(idx,f)

def load(f):
    idx = pickle.load(f)
    return idx

class FMSimpleIndex(object):
    def __init__(self, data):
        self.orig = data
        self.offset = {}
        self.data = bw.transform(data)
        self.FM = None
        self._build()
    
    def _build(self):
        if self.FM != None: return
        
        # left column
        L = sorted(self.data)
        
        # A is a index for letter -> L first occurance of letter
        A = {}
        last = ""
        for i, c in enumerate(L):
            if last != c:
                A[c] = i
                last = c
        del last, L
        
        # FM Index
        FM = {}
        for i, c in enumerate(self.data):
            for x, v in A.items():
                FM[(i,x)] = v
            FM[i] = A[c]
            A[c] += 1
        i = len(self.data)
        for x, v in A.items():
            FM[(i,x)] = v
        del A
        
        self.FM = FM
    
    def _LF(self, idx, qc):
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
    
    def bounds(self, q):
        top = 0
        bot = len(self.data)
        for i, qc in enumerate(q[::-1]):
            top = self._LF(top,qc)
            bot = self._LF(bot,qc)
            if top == bot: return (-1,-1)
        return (top,bot)
    
    def search(self, q):
        top, bot = self.bounds(q)
        if top == bot:
            return []
        matches = []
        for i in range(top, bot):
            pos = self._walk(i)
            matches.append(pos)
        return matches
    
    def count(self, q):
        top, bot = self.bounds(q)
        return bot - top