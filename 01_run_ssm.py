import boto3
import time
import sys
import os

# import csv
from datetime import datetime

# Function to wait for command to complete and return the result
def wait_for_command_to_complete(instance_id, command_id):
    while True:
        # Wait for 5 seconds before checking again
        time.sleep(5)
        # Fetch the command invocation details
        invocation_response = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        # Check if the command has completed
        status = invocation_response["Status"]
        if status not in ["Pending", "InProgress", "Delayed"]:
            return invocation_response

region = sys.argv[1]

instance_ids = sys.argv[2]
instance_ids = instance_ids.split(',')

# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client("ssm")
s3 = session.client("s3")

# Load the PowerShell script from a file
with open("script.ps1", "r") as file:
    powershell_script = file.read()

# Send the command
response = ssm.send_command(
    InstanceIds=instance_ids,
    DocumentName="AWS-RunPowerShellScript",
    Parameters={"commands": [powershell_script], "executionTimeout": ["3600"]},
    TimeoutSeconds=300 #,
    #OutputS3BucketName=target_bucket,
)

# Extract command ID
command_id = response["Command"]["CommandId"]
print(command_id)

# Wait for the command to complete and display the output
# invocation_response = wait_for_command_to_complete(instance_id, command_id)

