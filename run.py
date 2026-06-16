#!/usr/bin/env python3
import sys
import os

# Ensure the parent directory is in the PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from mac_monitor.cli.main import main

if __name__ == "__main__":
    main()
