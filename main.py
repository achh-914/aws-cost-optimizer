from modules.ec2_audit import audit_ec2_resources
from modules.ebs_audit import audit_ebs_volumes
from modules.report import generate_report

def main():
    print("======================================================")
    print("      Starting AWS Cost Audit & Optimization Tool     ")
    print("======================================================")

    # Run EC2 & EIP audit
    ec2_data = audit_ec2_resources()

    # Run EBS volumes audit
    ebs_data = audit_ebs_volumes()

    # Generate final report
    generate_report(ec2_data, ebs_data)

if __name__ == "__main__":
    main()
