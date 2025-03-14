import boto3
import time
import sys
import os
from datetime import datetime

# Function to wait for a command to complete and return the result
def wait_for_command_to_complete(instance_id, command_id):
    while True:
        time.sleep(5)  # Wait before checking again
        invocation_response = ssm.get_command_invocation(
            CommandId=command_id,
            InstanceId=instance_id,
        )
        status = invocation_response["Status"]
        if status not in ["Pending", "InProgress", "Delayed"]:
            return invocation_response

# Function to replace placeholders in the PowerShell script with given arguments
def replace_arguments(ps_script, arguments):
    for i, arg in enumerate(arguments):
        ps_script = ps_script.replace(f"#arg{i+1}#", arg)  # Replace all occurrences dynamically
    # print(ps_script)
    return ps_script

# Get region and instance IDs from command-line arguments
region = sys.argv[1]
instance_id = sys.argv[2]
arguments = [arg.strip() for arg in sys.argv[3].split(',')]

# Initialize AWS Boto3 session
session = boto3.Session(region_name=region)
ssm = session.client("ssm")
s3 = session.client("s3")

# Load the PowerShell script from a file
with open("script.ps1", "r") as file:
    powershell_script = file.read()

# Replace placeholders in the PowerShell script
powershell_script = replace_arguments(powershell_script, arguments)

# print (powershell_script)

# Send the modified script as an SSM command
response = ssm.send_command(
    InstanceIds=[instance_id],
    DocumentName="AWS-RunPowerShellScript",
    Parameters={"commands": [powershell_script], "executionTimeout": ["300"]},
    TimeoutSeconds=300,
)

# Extract and print the command ID
command_id = response["Command"]["CommandId"]
print(command_id)
