# AWS Cost Optimizer

A Python CLI tool designed to audit AWS infrastructure, detect hidden cost leaks, and provide actionable savings recommendations.

## 🚀 Features
- **EC2 Audit:** Detects idle or stopped instances that are still incurring storage/metadata costs.
- **Elastic IP (EIP) Audit:** Identifies unattached public IPs wasting monthly allocations.
- **EBS Audit:** Scans for unattached (available) EBS volumes accumulating dead storage costs.
- **RDS Audit:** Scans for stopped/idle RDS instances and old manual snapshots that waste storage allocations.
- **CLI Reporting:** Generates clean, formatted terminal reports using `tabulate`.

---

## 📊 Architecture Workflow

```mermaid
flowchart TD
    User([User / CLI]) --> Main[main.py: Cost Optimizer]
    
    subgraph AWS_Audit [AWS Cost Audit Process]
        Main --> EC2[modules/ec2_audit.py]
        Main --> EBS[modules/ebs_audit.py]
        Main --> RDS[modules/rds_audit.py]
        
        EC2 -->|Boto3 API| AWS_EC2[AWS EC2 & EIP Services]
        EBS -->|Boto3 API| AWS_EBS[AWS EBS Volumes]
        RDS -->|Boto3 API| AWS_RDS[AWS RDS Instances & Snapshots]
    end
    
    AWS_EC2 -->|Return Idle Resources| Main
    AWS_EBS -->|Return Unattached Volumes| Main
    AWS_RDS -->|Return Stopped DBs & Snapshots| Main
    
    Main --> Report[modules/report.py]
    Report --> Terminal[Terminal Summary & Savings Estimate]
