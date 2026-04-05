# AWS Automated Forensics Orchestrator for EC2

## Overview
This project implements an automated incident response system in AWS. It captures forensic evidence and isolates compromised EC2 instances using AWS Lambda.

## Features
- Automated EBS snapshot creation for forensic analysis
- Isolation of EC2 instances using a custom security group
- Serverless automation using AWS Lambda
- Secure access using IAM roles

## Architecture
- AWS Lambda (Python, Boto3)
- Amazon EC2
- Amazon EBS Snapshots
- Security Groups
- IAM Role

## Workflow
1. Event triggers Lambda function
2. Lambda identifies EC2 instance
3. Snapshot of EBS volume is created
4. Instance is isolated by applying a restricted security group

## Files
- lambda_function.py → Main automation script

## Future Improvements
- Add CloudWatch alerts
- Integrate with EventBridge
- Store logs in S3
