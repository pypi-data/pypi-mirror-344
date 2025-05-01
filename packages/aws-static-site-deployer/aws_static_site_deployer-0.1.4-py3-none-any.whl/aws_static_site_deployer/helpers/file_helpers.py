import os
import json
import shutil
from aws_static_site_deployer.helpers.logger import setup_logger

logger = setup_logger()

def validate_json_file(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            config_data = json.load(file)
        return config_data
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON validation error: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {json_file_path}")

def cleanup_outputs(output_dir=None, force=False):
    try:
        base_dir = output_dir if output_dir else "output"
        if not os.path.exists(base_dir):
            logger.info(f"Output directory {base_dir} doesn't exist. Nothing to clean.")
            return True
        
        if not force:
            logger.info(f"Will remove the entire output directory: {base_dir}")
                
            confirm = input(f"\nAre you sure you want to remove the entire output directory? (y/n): ")
            if confirm.lower() not in ('y', 'yes'):
                logger.info("Cleanup cancelled.")
                return False
        
        try:
            shutil.rmtree(base_dir)
            logger.info(f"Removed output directory: {base_dir}")
            return True
        except Exception as e:
            logger.error(f"Failed to remove output directory {base_dir}: {e}")
            return False
        
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")
        return False

