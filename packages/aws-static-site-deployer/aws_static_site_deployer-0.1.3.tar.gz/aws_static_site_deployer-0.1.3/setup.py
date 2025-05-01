from setuptools import setup, find_packages

setup(
    name="aws-static-site-deployer",
    version="0.1.3",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        "boto3>=1.28.0",
        "botocore>=1.31.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "argparse>=1.4.0"
    ],
    entry_points={
        'console_scripts': [
            'aws-static-site-deployer=aws_static_site_deployer.cli:main',
        ],
    },
    author="Syed Danial",
    author_email="your.email@example.com",
    description="AWS CloudFront Static Website Deployment Tool",
    python_requires=">=3.6",
)