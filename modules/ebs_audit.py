import boto3

def audit_ebs_volumes():
    """
    Audits EBS volumes to find unattached (available) volumes that waste money.
    """
    ec2_client = boto3.client('ec2')
    print("[*] Scanning unattached EBS volumes...")

    # Filter for volumes that are not attached to any instance (status: available)
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

if __name__ == "__main__":
    result = audit_ebs_volumes()
    print("Unattached Volumes:", result)
