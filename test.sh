#!/bin/bash

./fm-build.py test_data test_idx && ./fm-search.py test_idx "acgt"
