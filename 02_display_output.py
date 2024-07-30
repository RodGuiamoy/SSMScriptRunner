import sys
import boto3
import time

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
command_id = sys.argv[2]
instance_id = sys.argv[3]

# Initialize a Boto3 session
session = boto3.Session(region_name=region)

# Use the SSM (Simple Systems Manager) client
ssm = session.client("ssm")

# Wait for the command to complete and display the output
invocation_response = wait_for_command_to_complete(instance_id, command_id)

output = invocation_response['StandardOutputContent'].splitlines()
print(output)

error = invocation_response['StandardErrorContent'].splitlines()
print(error)