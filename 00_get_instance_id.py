import boto3
import sys

def get_instance_id(instance_name, region):
    # Create a session using your AWS credentials
    session = boto3.Session(region_name=region)
    ec2_client = session.client('ec2')

    # Describe all instances
    response = ec2_client.describe_instances()

    # Loop through all instances to find the one with the specified name
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            # Check if the 'Name' tag matches the instance_name (case insensitive)
            tags = instance.get('Tags', [])
            for tag in tags:
                if tag['Key'] == 'Name' and tag['Value'].lower() == instance_name.lower():
                    # Check if the instance is running and passed all 3 status checks
                    if instance['State']['Name'] == 'running':
                        # Check instance status checks
                        instance_status = ec2_client.describe_instance_status(InstanceIds=[instance['InstanceId']])
                        if instance_status['InstanceStatuses']:
                            status = instance_status['InstanceStatuses'][0]
                            if status['SystemStatus']['Status'] == 'ok' and status['InstanceStatus']['Status'] == 'ok':
                                return instance['InstanceId']
    
    # If no instance is found or it's not running with 3/3 checks, return None
    return None

instance_name = sys.argv[1]
region = sys.argv[2]

# Example usage
if __name__ == "__main__":
    instance_id = get_instance_id(instance_name, region)
    if instance_id:
        print(f'{instance_id}')
