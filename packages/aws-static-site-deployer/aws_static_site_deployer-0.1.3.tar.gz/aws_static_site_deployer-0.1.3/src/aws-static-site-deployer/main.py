import os
import argparse
import json
from datetime import datetime
from aws_static_site_deployer.helpers.logger import setup_logger
from aws_static_site_deployer.helpers.git_helpers import clone_github_repo
from aws_static_site_deployer.helpers.template_helpers import generate_yaml_for_application
from aws_static_site_deployer.helpers.aws_helpers import deploy_cloudformation_stack, upload_to_s3
from aws_static_site_deployer.helpers.file_helpers import cleanup_outputs, validate_json_file

logger = setup_logger()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Deploy static websites to AWS CloudFront')
    parser.add_argument('--repo-url', required=True, help='GitHub repository URL containing the website and config.json')
    parser.add_argument('--branch', default='main', help='Git branch to clone (default: main)')
    parser.add_argument('--deploy', action='store_true', help='Deploy the CloudFormation stack')
    parser.add_argument('--wait', action='store_true', help='Wait for stack creation to complete')
    parser.add_argument('--cleanup', action='store_true', help='Clean up all output directories after deployment')
    parser.add_argument('--force-cleanup', action='store_true', help='Force cleanup without confirmation prompt')
    return parser.parse_args()

def process_application(repo_url, branch, output_dir, timestamp, deploy=False, wait=False):
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    logger.info(f"Processing repository: {repo_name} (branch: {branch})")

    repo_dir = os.path.join(output_dir, f"{repo_name}_repo")
    success = clone_github_repo(repo_url, branch, repo_dir)
    
    if not success:
        logger.error(f"Failed to clone repository: {repo_url}")
        return False
    
    config_path = os.path.join(repo_dir, 'config.json')
    if not os.path.exists(config_path):
        logger.error(f"config.json not found in the repository")
        return False
    
    try:
        with open(config_path, 'r') as file:
            application = json.load(file)
        
        if not application or not application.get('ApplicationName'):
            logger.error(f"Invalid or incomplete configuration in config.json")
            return False
            
        app_name = application.get('ApplicationName')
        logger.info(f"Found application configuration for: {app_name}")
    except Exception as e:
        logger.error(f"Error loading config.json: {e}")
        return False
    
    try:
        yaml_file = generate_yaml_for_application(application, timestamp, output_dir)
        logger.info(f"Generated CloudFormation template: {yaml_file}")
    except Exception as e:
        logger.error(f"Error generating CloudFormation template: {e}")
        return False
    
    if deploy:
        stack_success = deploy_cloudformation_stack(yaml_file, wait)
        if not stack_success:
            logger.error(f"Failed to deploy CloudFormation stack")
            return False
        
        s3_bucket_name = f"{application['DomainNamePrefix']}-{application['ApplicationName']}.{application['DomainNameSuffix']}"
        upload_success = upload_to_s3(repo_dir, s3_bucket_name)
        
        if not upload_success:
            logger.warning(f"Failed to upload content to S3")
        
        return upload_success
    else:
        return True

def run_deployment():
    try:
        args = parse_arguments()
        repo_name = args.repo_url.split('/')[-1].replace('.git', '')
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_dir = os.path.join("/tmp", f"{repo_name}")
        os.makedirs(output_dir, exist_ok=True)
        
        success = process_application(
            args.repo_url, 
            args.branch, 
            output_dir, 
            timestamp, 
            args.deploy, 
            args.wait
        )
        
        print("\n--- Deployment Summary ---")
        status = "✅ Success" if success else "❌ Failed"
        logger.info(f"{status}: {repo_name}")
        
        if args.cleanup:
            print("\n--- Starting Cleanup ---")
            cleanup_outputs(output_dir, force=args.force_cleanup)
        
        return 0 if success else 1
    
    except Exception as e:
        logger.error(f"Error in deployment execution: {e}", exc_info=True)
        return 1