"""
author: openpineaplehub
copyright: 2025 all rights reversed
"""

import os

def get_config_path() -> str:
    home_dir = os.path.expanduser("~")
    config_file = os.path.join(home_dir, ".pinetodo.config.json")
    return config_file

def get_data_path() -> str:
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), ".pinetodo.opinedocs")
