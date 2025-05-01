import os
import json
import subprocess
import boto3
from botocore.exceptions import ClientError
from src.helpers.logger import setup_logger

logger = setup_logger()

def upload_to_s3(local_dir, bucket_name):
    logger.info(f"Uploading content to S3 bucket: {bucket_name}")
    
    s3_client = boto3.client('s3')
    
    try:
        s3_client.head_bucket(Bucket=bucket_name)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            logger.warning(f"Bucket {bucket_name} does not exist yet. It will be created by CloudFormation.")
            return False
        else:
            logger.error(f"Error checking S3 bucket: {e}")
            return False

    try:
        file_count = 0
        for root, _, files in os.walk(local_dir):
            if '.git' in root:
                continue
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_dir)
                s3_key = relative_path.replace("\\", "/")
                
                content_type = get_content_type(file)
                
                logger.debug(f"Uploading {local_path} to s3://{bucket_name}/{s3_key}")
                s3_client.upload_file(
                    local_path, 
                    bucket_name, 
                    s3_key,
                    ExtraArgs={'ContentType': content_type}
                )
                file_count += 1
        
        logger.info(f"Successfully uploaded {file_count} files to S3 bucket {bucket_name}")
        return True
    except Exception as e:
        logger.error(f"Error uploading to S3: {e}")
        return False

def get_content_type(filename):
    extension = os.path.splitext(filename)[1].lower()
    content_types = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.xml': 'application/xml',
        '.txt': 'text/plain',
        '.ico': 'image/x-icon',
        '.pdf': 'application/pdf',
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.ttf': 'font/ttf',
        '.eot': 'application/vnd.ms-fontobject',
        '.otf': 'font/otf',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
    }
    return content_types.get(extension, 'application/octet-stream')

def deploy_cloudformation_stack(yaml_file, wait=False):
    stack_name = os.path.basename(yaml_file).split('.')[0]
    logger.info(f"Deploying CloudFormation stack: {stack_name}")
    
    cmd = [
        "aws", "cloudformation", "create-stack",
        "--stack-name", stack_name,
        "--template-body", f"file://{yaml_file}",
        "--capabilities", "CAPABILITY_IAM", "CAPABILITY_NAMED_IAM",
        "--region", "us-east-1"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"Stack {stack_name} deployment initiated.")
        
        if wait:
            logger.info(f"Waiting for stack {stack_name} to complete deployment...")
            wait_cmd = [
                "aws", "cloudformation", "wait", "stack-create-complete",
                "--stack-name", stack_name,
                "--region", "us-east-1"
            ]
            subprocess.run(wait_cmd, check=True)
            logger.info(f"Stack {stack_name} deployed successfully.")
            
            outputs = get_stack_outputs(stack_name)
            if outputs:
                logger.info(f"Stack Outputs for {stack_name}:")
                for key, value in outputs.items():
                    logger.info(f"  {key}: {value}")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error deploying stack {stack_name}: {e}")
        if e.stderr:
            logger.error(f"AWS CLI error output: {e.stderr.decode()}")
        return False

def get_stack_outputs(stack_name):
    try:
        cmd = [
            "aws", "cloudformation", "describe-stacks",
            "--stack-name", stack_name,
            "--query", "Stacks[0].Outputs",
            "--output", "json",
            "--region", "us-east-1"
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        outputs = json.loads(result.stdout)
        
        output_dict = {}
        for output in outputs:
            output_dict[output['OutputKey']] = output['OutputValue']
        
        return output_dict
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        logger.error(f"Error retrieving stack outputs: {e}")
        return None
