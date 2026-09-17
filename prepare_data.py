import os

docs = {
    "data/raw/k8s_troubleshooting.txt": """# Kubernetes Cluster Troubleshooting Manual
Document ID: K8S-DOC-01
Section 1: CrashLoopBackOff Resolution
When a pod enters CrashLoopBackOff, inspect logs with 'kubectl logs <pod-name> --previous'. 
Common causes include:
1. Application initialization failure (missing environment variables or unresolvable secrets).
2. Out Of Memory (OOMKilled - Exit Code 137). Check limits using 'kubectl describe pod <pod-name>'.
3. Liveness probe failure due to high latency or incorrect health check path.

Section 2: Node NotReady State
If a node status changes to NotReady:
1. Inspect kubelet status using 'systemctl status kubelet' on the host.
2. Check disk pressure and memory pressure conditions in 'kubectl describe node <node-name>'.
3. Verify overlay network plugin pods (e.g., Calico or Cilium) are running without restarts.
""",
    "data/raw/database_failover.txt": """# PostgreSQL Disaster Recovery and Failover Guide
Document ID: DB-DOC-02
Section 1: High Availability Architecture
Our PostgreSQL deployment uses streaming replication with Patroni and etcd for consensus.
A quorum of 3 etcd nodes is required for automatic leader election.

Section 2: Manual Failover Steps
If automatic failover does not trigger:
1. Identify the healthy replica with minimal lag: 'patronictl -c /etc/patroni/config.yml list'.
2. Execute failover manually: 'patronictl -c /etc/patroni/config.yml failover'.
3. Verify client connectivity via PgBouncer load balancers on port 6432.
Never force primary election if replication lag exceeds 100MB to avoid data loss.
""",
    "data/raw/incident_sla_policy.txt": """# Incident Response SLA & Escalation Policy
Document ID: SLA-DOC-03
Section 1: Severity Classifications
- Severity 1 (Critical): Total outage of user-facing production systems. SLA Response: < 15 minutes. Update interval: Every 30 minutes.
- Severity 2 (Major): Partial degradation of service with no immediate workaround. SLA Response: < 1 hour. Update interval: Every 2 hours.
- Severity 3 (Minor): Non-critical bugs, administrative portal issues. SLA Response: < 4 hours.

Section 2: Communication Protocols
All Sev-1 incidents require an incident commander and an active war room on Slack channel #incident-war-room.
Post-mortems (Root Cause Analysis - RCA) must be published within 72 hours of incident resolution.
"""
}

os.makedirs("data/raw", exist_ok=True)
for path, content in docs.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())
print("Data files generated successfully in data/raw/")


