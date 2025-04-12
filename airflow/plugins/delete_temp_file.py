import os
import logging
import os

def delete(file_name: str):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_dir = os.path.join(script_dir, "temp")
    local_path = os.path.join(local_dir, file_name)

    os.remove(local_path)
    
    logging.info(f"Removed temporary file {local_path}")