from tabulate import tabulate

def generate_report(ec2_results, ebs_results, rds_results):
    """
    Generates a clean CLI report for AWS cost leaks and waste, including EC2, EBS, and RDS.
    """
    print("\n" + "="*60)
    print("             AWS COST OPTIMIZATION REPORT             ")
    print("="*60 + "\n")
    
    # 1. Stopped EC2 Instances
    stopped = ec2_results.get("stopped_instances", [])
    print(f"[*] Stopped EC2 Instances Found: {len(stopped)}")
    if stopped:
        table_data = [[i['InstanceId'], i['Type'], i['State']] for i in stopped]
        print(tabulate(table_data, headers=["Instance ID", "Type", "State"], tablefmt="fancy_grid"))
    else:
        print("[+] No stopped EC2 instances found.")
        
    print("\n" + "-"*60 + "\n")
    
    # 2. Unused Elastic IPs
    eips = ec2_results.get("unused_eips", [])
    print(f"[*] Unused Elastic IPs Found: {len(eips)}")
    if eips:
        for ip in eips:
            print(f"  - Public IP: {ip}")
    else:
        print("[+] No unused Elastic IPs found.")
        
    print("\n" + "-"*60 + "\n")
    
    # 3. Unattached EBS Volumes
    volumes = ebs_results
    print(f"[*] Unattached EBS Volumes Found: {len(volumes)}")
    if volumes:
        vol_data = [[v['VolumeId'], f"{v['Size']} GB", v['VolumeType'], v['CreateTime']] for v in volumes]
        print(tabulate(vol_data, headers=["Volume ID", "Size", "Type", "Created At"], tablefmt="fancy_grid"))
    else:
        print("[+] No unattached EBS volumes found.")

    print("\n" + "-"*60 + "\n")

    # 4. Stopped RDS Instances & Manual Snapshots
    stopped_rds = rds_results.get("stopped_rds", [])
    manual_snaps = rds_results.get("manual_snapshots", [])
    
    print(f"[*] Stopped RDS Instances Found: {len(stopped_rds)}")
    if stopped_rds:
        rds_data = [[db['DBInstanceIdentifier'], db['Engine'], db['InstanceClass'], db['Status']] for db in stopped_rds]
        print(tabulate(rds_data, headers=["DB Identifier", "Engine", "Class", "Status"], tablefmt="fancy_grid"))
    else:
        print("[+] No stopped RDS instances found.")

    print(f"\n[*] RDS Manual Snapshots Found: {len(manual_snaps)}")
    if manual_snaps:
        snap_data = [[s['DBSnapshotIdentifier'], s['DBInstanceIdentifier'], f"{s['AllocatedStorage']} GB", s['SnapshotCreateTime']] for s in manual_snaps]
        print(tabulate(snap_data, headers=["Snapshot ID", "DB Identifier", "Storage", "Created At"], tablefmt="fancy_grid"))
    else:
        print("[+] No manual RDS snapshots found.")
        
    print("\n" + "="*60)
    print("End of Report. Review resources before taking action!")
    print("="*60 + "\n")
