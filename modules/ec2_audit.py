import boto3
from botocore.exceptions import NoCredentialsError, NoRegionError, ClientError

def audit_ec2_resources():
    """
    Audits EC2 instances for stopped states and unused Elastic IPs.
    """
    print("[*] Scanning EC2 instances and Elastic IPs...")
    try:
        ec2_client = boto3.client('ec2')
        
        # 1. Stopped EC2 Instances
        response = ec2_client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
        )
        
        stopped_instances = []
        for reservation in response.get('Reservations', []):
            for instance in reservation.get('Instances', []):
                stopped_instances.append({
                    'InstanceId': instance['InstanceId'],
                    'Type': instance['InstanceType'],
                    'State': instance['State']['Name']
                })

        # 2. Unused Elastic IPs
        eips_response = ec2_client.describe_addresses()
        unused_eips = []
        for address in eips_response.get('Addresses', []):
            if 'InstanceId' not in address and 'NetworkInterfaceId' not in address:
                unused_eips.append(address.get('PublicIp'))

        return {
            "stopped_instances": stopped_instances,
            "unused_eips": unused_eips
        }
    except (NoCredentialsError, NoRegionError, ClientError) as e:
        print(f"[!] AWS Authentication/Region Warning: {e}")
        return {"stopped_instances": [], "unused_eips": []}

if __name__ == "__main__":
    result = audit_ec2_resources()
    print("EC2 Audit Result:", result)
