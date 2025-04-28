
"""
author: openpineaplehub
copyright: 2025 all rights reversed
"""

from .router import handle_command
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def main():
    handle_command()

if __name__ == "__main__":
    main()
