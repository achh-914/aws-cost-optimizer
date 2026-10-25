import boto3

def audit_ec2_resources(session=None):
    """
    Audits EC2 instances and unused Elastic IPs using paginators for large-scale environments.
    """
    ec2_client = session.client('ec2') if session else boto3.client('ec2')
    
    # 1. Stopped EC2 Instances (using Paginator)
    paginator = ec2_client.get_paginator('describe_instances')
    stopped_instances = []
    
    page_iterator = paginator.paginate(
        Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}]
    )
    
    for page in page_iterator:
        for reservation in page.get('Reservations', []):
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
