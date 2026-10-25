import boto3
from botocore.exceptions import NoCredentialsError, NoRegionError, ClientError

def audit_ebs_volumes():
    """
    Audits EBS volumes to find unattached (available) volumes.
    """
    print("[*] Scanning unattached EBS volumes...")
    try:
        ec2_client = boto3.client('ec2')
        response = ec2_client.describe_volumes(
            Filters=[{'Name': 'status', 'Values': ['available']}]
        )
        
        unattached_volumes = []
        for volume in response.get('Volumes', []):
            unattached_volumes.append({
                'VolumeId': volume['VolumeId'],
                'Size': volume['Size'],
                'VolumeType': volume['VolumeType'],
                'CreateTime': str(volume['CreateTime'])
            })
            
        return unattached_volumes
    except (NoCredentialsError, NoRegionError, ClientError) as e:
        print(f"[!] AWS Authentication/Region Warning: {e}")
        return []

if __name__ == "__main__":
    result = audit_ebs_volumes()
    print("Unattached Volumes:", result)
