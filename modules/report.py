from tabulate import tabulate

def generate_report(ec2_results, ebs_results):
    """
    Generates a clean CLI report for AWS cost leaks and waste.
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

    print("\n" + "="*60)
    print("End of Report. Review resources before taking action!")
    print("="*60 + "\n")
