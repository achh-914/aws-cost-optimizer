import boto3

def audit_rds_resources():
    """
    Audits RDS instances and manual snapshots to find cost-saving opportunities.
    """
    rds_client = boto3.client('rds')
    print("[*] Scanning RDS instances and manual snapshots...")

    # 1. Check RDS instances for stopped/idle ones
    response = rds_client.describe_db_instances()
    stopped_rds = []

    for db in response.get('DBInstances', []):
        db_identifier = db['DBInstanceIdentifier']
        status = db['DBInstanceStatus']
        if status in ['stopped', 'stopping']:
            stopped_rds.append({
                'DBInstanceIdentifier': db_identifier,
                'Engine': db['Engine'],
                'InstanceClass': db['DBInstanceClass'],
                'Status': status
            })

    # 2. Check for manual snapshots that accumulate storage costs
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

if __name__ == "__main__":
    result = audit_rds_resources()
    print("Stopped RDS:", result["stopped_rds"])
    print("Manual Snapshots:", result["manual_snapshots"])
