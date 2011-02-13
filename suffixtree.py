#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint as pp
import re

class SuffixTree(object):
    def __init__(self,*args):
        self.root = {}
    
    def _add(self, node, s):
        if len(s) <= 0:
            node[0] = ''
            return
        c = s[0]
        if node.has_key(c):
            self._add(node[c], s[1:])
        else:
            node[c] = {}
            self._add(node[c], s[1:])
    
    def add(self, s):
        for i in xrange(len(s)):
            self._add(self.root, s[i:])
    
    def __repr__(self):
        return str(self.root)
    
    def _strings(self, node, prefix):
        t = []
        for c,n in sorted(node.items()):
            if c == 0:
                t.append(prefix)
                continue
            k = self._strings(n, prefix + c)
            t.extend(k)
        return t
    
    def strings(self):
        return self._strings(self.root,'')
        
    def __str__(self):
        return '\n'.join(self.strings())
    
    def _json(self, node):
        data = "{name:%s}" % (node)
    
    def json(self):
        return _json(self.root)