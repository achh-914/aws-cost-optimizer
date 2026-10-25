import boto3

def audit_ebs_volumes():
    """
    Audits EBS volumes to find unattached (available) volumes.
    """
    print("[*] Scanning unattached EBS volumes...")
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
