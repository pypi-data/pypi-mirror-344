#!/usr/bin/env python3
import sys
from aws_static_site_deployer.main import run_deployment

def main():
    """Entry point for the application"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║  Static Website Deployment Tool for AWS   ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)
    
    return run_deployment()

if __name__ == "__main__":
    sys.exit(main())