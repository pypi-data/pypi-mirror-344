import os
import shutil
import subprocess
from src.helpers.logger import setup_logger

logger = setup_logger()

def clone_github_repo(repo_url, branch, output_dir):
    logger.info(f"Cloning repository {repo_url} (branch: {branch})")
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([repo_url, output_dir])
        
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Repository cloned successfully to {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error cloning repository: {e}")
        logger.error(f"Git output: {e.stderr.decode()}")
        return False
