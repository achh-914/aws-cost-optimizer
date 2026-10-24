import boto3

def audit_ec2_resources():
    """
    Audits EC2 instances to find stopped ones and unattached Elastic IPs.
    """
    ec2_client = boto3.client('ec2')
    
    print("[*] Scanning EC2 instances and Elastic IPs...")
    
    # 1. Check for stopped EC2 instances
    response = ec2_client.describe_instances()
    stopped_instances = []
    
    for reservation in response.get('Reservations', []):
        for instance in reservation.get('Instances', []):
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            if state == 'stopped':
                stopped_instances.append({
                    'InstanceId': instance_id,
                    'Type': instance['InstanceType'],
                    'State': state
                })

    # 2. Check for unattached Elastic IPs
    addresses_response = ec2_client.describe_addresses()
    unused_eips = []
    
    for addr in addresses_response.get('Addresses', []):
        if 'InstanceId' not in addr and 'NetworkInterfaceId' not in addr:
            unused_eips.append(addr.get('PublicIp'))

    return {
        "stopped_instances": stopped_instances,
        "unused_eips": unused_eips
    }

if __name__ == "__main__":
    result = audit_ec2_resources()
    print("Stopped Instances:", result["stopped_instances"])
    print("Unused EIPs:", result["unused_eips"])
