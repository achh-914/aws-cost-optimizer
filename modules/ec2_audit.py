import boto3

def audit_ec2_resources():
    """
    Audits EC2 instances for stopped states and unused Elastic IPs.
    Raises exception on failure to prevent false negatives.
    """
    print("[*] Scanning EC2 instances and Elastic IPs...")
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

    # 2. Unused Elastic IPs (checked via AssociationId)
    eips_response = ec2_client.describe_addresses()
    unused_eips = []
    for address in eips_response.get('Addresses', []):
        if 'AssociationId' not in address:
            unused_eips.append(address.get('PublicIp'))

    return {
        "stopped_instances": stopped_instances,
        "unused_eips": unused_eips
    }
