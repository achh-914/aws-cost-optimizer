import boto3

def audit_rds_resources(session=None):
    """
    Audits RDS instances and manual snapshots using paginators.
    """
    rds_client = session.client('rds') if session else boto3.client('rds')
    
    # 1. Stopped RDS instances (using Paginator)
    db_paginator = rds_client.get_paginator('describe_db_instances')
    stopped_rds = []
    
    for page in db_paginator.paginate():
        for db in page.get('DBInstances', []):
            if db['DBInstanceStatus'] in ['stopped', 'stopping']:
                stopped_rds.append({
                    'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                    'Engine': db['Engine'],
                    'InstanceClass': db['DBInstanceClass'],
                    'Status': db['DBInstanceStatus']
                })
                
    # 2. Manual Snapshots (using Paginator)
    snap_paginator = rds_client.get_paginator('describe_db_snapshots')
    manual_snapshots = []
    
    for page in snap_paginator.paginate(SnapshotType='manual'):
        for snap in page.get('DBSnapshots', []):
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
