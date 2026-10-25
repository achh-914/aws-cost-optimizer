from modules.ec2_audit import audit_ec2_resources
from modules.ebs_audit import audit_ebs_volumes
from modules.rds_audit import audit_rds_resources
from modules.report import generate_report

def main():
    print("======================================================")
    print("      Starting AWS Cost Audit & Optimization Tool     ")
    print("======================================================")
    
    # Run Audits
    ec2_data = audit_ec2_resources()
    ebs_data = audit_ebs_volumes()
    rds_data = audit_rds_resources()
    
    # Generate final comprehensive report
    generate_report(ec2_data, ebs_data, rds_data)

if __name__ == "__main__":
    main()
