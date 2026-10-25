import boto3

def audit_rds_resources():
    """
    Audits RDS instances and manual snapshots.
    """
    print("[*] Scanning RDS instances and manual snapshots...")
    rds_client = boto3.client('rds')
    
    # 1. Stopped RDS instances
    response = rds_client.describe_db_instances()
    stopped_rds = []
    for db in response.get('DBInstances', []):
        if db['DBInstanceStatus'] in ['stopped', 'stopping']:
            stopped_rds.append({
                'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                'Engine': db['Engine'],
                'InstanceClass': db['DBInstanceClass'],
                'Status': db['DBInstanceStatus']
            })
            
    # 2. Manual Snapshots
    snapshots_response = rds_client.describe_db_snapshots(SnapshotType='manual')
    manual_snapshots = []
    for snap in snapshots_response.get('DBSnapshots', []):
        manual_snapshots.append({
            'DBSnapshotIdentifier': snap['DBSnapshotIdentifier'],
            'DBInstanceIdentifier': snap['DBInstanceIdentifier'],
            'SnapshotCreateTime': str(snap['SnapshotCreateTime']),
            'AllocatedStorage': snap.get('AllocatedStorage', 0)
        })

    return {
        "stopped_rds": stopped_rds,
        "manual_snapshots": manual_snapshots
    }
