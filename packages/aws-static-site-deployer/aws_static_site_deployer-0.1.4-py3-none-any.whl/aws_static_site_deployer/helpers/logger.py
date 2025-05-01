import logging

def setup_logger(name='static-site-deployer', level=logging.INFO):
    """Configure and return a logger"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    return logging.getLogger(name)