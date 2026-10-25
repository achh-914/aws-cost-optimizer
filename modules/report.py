from tabulate import tabulate

def generate_report(ec2_results, ebs_results, rds_results):
    """
    Generates a professional CLI report including estimated monthly financial waste in USD.
    """
    print("\n" + "="*70)
    print("             AWS COST OPTIMIZATION & FINOPS REPORT             ")
    print("="*70 + "\n")
    
    total_estimated_waste = 0.0
    
    # 1. Stopped EC2 Instances
    stopped = ec2_results.get("stopped_instances", [])
    print(f"[*] Stopped EC2 Instances Found: {len(stopped)}")
    if stopped:
        table_data = [[i['InstanceId'], i['Type'], i['State']] for i in stopped]
        print(tabulate(table_data, headers=["Instance ID", "Type", "State"], tablefmt="fancy_grid"))
    else:
        print("[+] No stopped EC2 instances found.")
        
    print("\n" + "-"*70 + "\n")
    
    # 2. Unused Elastic IPs ($3.65 / month each)
    eips = ec2_results.get("unused_eips", [])
    eip_cost = len(eips) * 3.65
    total_estimated_waste += eip_cost
    print(f"[*] Unused Elastic IPs Found: {len(eips)} (Est. Waste: ${eip_cost:.2f}/mo)")
    if eips:
        for ip in eips:
            print(f"  - Public IP: {ip}")
    else:
        print("[+] No unused Elastic IPs found.")
        
    print("\n" + "-"*70 + "\n")
    
    # 3. Unattached EBS Volumes (~$0.08 per GB/month)
    volumes = ebs_results
    ebs_cost = sum(v['Size'] * 0.08 for v in volumes)
    total_estimated_waste += ebs_cost
    print(f"[*] Unattached EBS Volumes Found: {len(volumes)} (Est. Waste: ${ebs_cost:.2f}/mo)")
    if volumes:
        vol_data = [[v['VolumeId'], f"{v['Size']} GB", v['VolumeType'], f"${v['Size'] * 0.08:.2f}", v['CreateTime']] for v in volumes]
        print(tabulate(vol_data, headers=["Volume ID", "Size", "Type", "Est. Cost/Mo", "Created At"], tablefmt="fancy_grid"))
    else:
        print("[+] No unattached EBS volumes found.")

    print("\n" + "-"*70 + "\n")

    # 4. RDS Instances & Manual Snapshots (~$0.095 per GB/month for snapshots)
    stopped_rds = rds_results.get("stopped_rds", [])
    manual_snaps = rds_results.get("manual_snapshots", [])
    
    snapshot_cost = sum(s['AllocatedStorage'] * 0.095 for s in manual_snaps)
    total_estimated_waste += snapshot_cost

    print(f"[*] Stopped RDS Instances Found: {len(stopped_rds)}")
    if stopped_rds:
        rds_data = [[db['DBInstanceIdentifier'], db['Engine'], db['InstanceClass'], db['Status']] for db in stopped_rds]
        print(tabulate(rds_data, headers=["DB Identifier", "Engine", "Class", "Status"], tablefmt="fancy_grid"))
    else:
        print("[+] No stopped RDS instances found.")

    print(f"\n[*] RDS Manual Snapshots Found: {len(manual_snaps)} (Est. Waste: ${snapshot_cost:.2f}/mo)")
    if manual_snaps:
        snap_data = [[s['DBSnapshotIdentifier'], s['DBInstanceIdentifier'], f"{s['AllocatedStorage']} GB", f"${s['AllocatedStorage'] * 0.095:.2f}", s['SnapshotCreateTime']] for s in manual_snaps]
        print(tabulate(snap_data, headers=["Snapshot ID", "DB Identifier", "Storage", "Est. Cost/Mo", "Created At"], tablefmt="fancy_grid"))
    else:
        print("[+] No manual RDS snapshots found.")
        
    print("\n" + "="*70)
    print(f" 💰 TOTAL ESTIMATED MONTHLY WASTE: ${total_estimated_waste:.2f} / month")
    print("="*70 + "\n")
