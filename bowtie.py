# -*- coding: utf-8 -*-
#!/usr/bin/python
import os, re
import bwt

class Bowtie:
    def __init__(self, data):
        self.orig = data
        self.offset = {}
        self.data = bwt.transform(data)
        self.FM = None
        self.init_FM()
    
    def init_FM(self):
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
    
    def LF(self, idx, qc):
        return self.FM[(idx,qc)]
    
    def walk(self, idx):
        r = 0
        i = idx
        while self.data[i] != "\0":
            if self.offset.get(i):
                r += self.offset[i]
                break
            r += 1
            i = self.FM[i]
            
        if not self.offset.get(idx):
            self.offset[i] = r
        return r    
    
    def search(self, q):
        top = 0
        bot = len(self.data)
        for i, qc in enumerate(q[::-1]):
            top = self.LF(top,qc)
            bot = self.LF(bot,qc)
            if top == bot: return []
        matches = []
        for i in range(top, bot):
            matches.append(self.walk(i))
        return sorted(matches)

b = Bowtie("ACGTCCGTAAAGCAGTCG")
