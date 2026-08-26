#!/usr/bin/env python
import os
import sys

# Ensure repository root is in python path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from server.src.cli.dispatcher import main

if __name__ == '__main__':
    main()
