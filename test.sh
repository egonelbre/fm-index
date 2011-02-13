#!/bin/bash

./fm-build.py data/test_data data/test_idx && ./fm-search.py data/test_idx "acgt"
