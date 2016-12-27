#!/bin/env python3
'''child.py'''
import os, sys

print('Hello from child', os.getpid(), sys.argv[0], sys.argv[1])