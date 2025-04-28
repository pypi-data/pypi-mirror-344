import os
import shutil
from datetime import datetime

def export_database():
    source_file = os.path.expanduser("~/.pinetodo.config.json")
    dist_dir = os.path.expanduser("~/.pinetodo_dist")
    today = datetime.now().strftime("%d-%m-%y")
    export_filename = f".pinetodo.database.{today}.json"
    export_path = os.path.join(dist_dir, export_filename)

    if not os.path.exists(source_file):
        print("No data found to export.")
        return

    os.makedirs(dist_dir, exist_ok=True)
    shutil.copy(source_file, export_path)
    print(f"Successfully exported to {export_path}")
