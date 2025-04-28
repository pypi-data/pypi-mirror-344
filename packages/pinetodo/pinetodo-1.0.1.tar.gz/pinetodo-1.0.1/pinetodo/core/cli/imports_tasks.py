import os
import json
import requests

def import_data(path=None, raw_url=None):
    config_dir = os.path.expanduser("~/.pinetodo_dist")
    config_file = os.path.join(config_dir, ".pinetodo.config.json")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f" Created directory: {config_dir}")

    data = None

    if path:
        if not os.path.exists(path):
            print(f"The file '{path}' does not exist.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f" Successfully loaded data from local path: {path}")
        except Exception as e:
            print(f"Failed to load JSON from local path: {e}")
            return

    elif raw_url:
        try:
            response = requests.get(raw_url)
            response.raise_for_status()
            data = response.json()
            print(f" Successfully loaded data from URL: {raw_url}")
        except Exception as e:
            print(f"Failed to fetch JSON from URL: {e}")
            return

    else:
        print("No valid input source provided.")
        return

    try:
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f" Data imported and written to: {config_file}")
    except Exception as e:
        print(f"Failed to write data to config file: {e}")
