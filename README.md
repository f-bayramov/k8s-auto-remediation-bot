# Kubernetes Auto-Remediation Controller 🚑

![Status](https://img.shields.io/badge/status-active-success)
![Kubernetes](https://img.shields.io/badge/kubernetes-v1.27%2B-blue)
![Python](https://img.shields.io/badge/python-3.9-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**An event-driven self-healing framework for Kubernetes clusters designed to eliminate manual intervention for common infrastructure failures.**

---

## 📖 Executive Summary
In high-scale production environments, **Mean Time to Recovery (MTTR)** is a critical KPI. Relying on human engineers to manually restart services during memory leaks or deadlocks introduces latency and potential for error.

This project implements a **Level-4 Autonomous System** (Self-Healing) that detects anomalies via Prometheus metrics and executes automated remediation strategies via a custom Kubernetes Operator logic. It bridges the gap between **Observability** and **Action**.

## 🏗️ Architecture Design

The system operates on a closed-loop feedback mechanism, ensuring zero-touch recovery.

```mermaid
graph LR
    A[Target Application] -->|Metrics Exporter| B(Prometheus)
    B -->|Alert: HighMemory| C{Alertmanager}
    C -->|Webhook Payload| D[Healer Bot Controller]
    D -->|K8s API Call| E((Kubernetes Control Plane))
    E -->|Restart/Patch Pod| A
    style D fill:#f9f,stroke:#333,stroke-width:2px
Core Components
Metric Ingestion: Prometheus scrapes container_memory_usage_bytes and other signals in real-time.

Decision Engine: Alertmanager aggregates alerts to prevent "alert storms" and triggers the webhook.

Remediation Controller: A custom Python-based FastAPI service that authenticates with the K8s API using internal ServiceAccount tokens to perform targeted pod eviction (Graceful Restart).

🚀 Technical Implementation
Prerequisites
Kubernetes Cluster (v1.24+)

Prometheus & Alertmanager (kube-prometheus-stack)

Python 3.9+ & Docker

Installation Guide
1. Clone the repository
Bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/k8s-auto-remediation-bot.git](https://github.com/YOUR_GITHUB_USERNAME/k8s-auto-remediation-bot.git)
cd k8s-auto-remediation-bot
2. Build & Load Images
Note: If using a remote registry (Docker Hub/ECR), push the images instead of importing.

Bash
docker build -t bad-app:v1 ./bad-app
docker build -t healer-bot:v1 ./bot

# For k3d users:
k3d image import bad-app:v1 healer-bot:v1 -c dev-secops
3. Deploy RBAC & Services
The bot requires specific Least Privilege permissions to manage pods.

Bash
# Apply RBAC roles and ServiceAccount
kubectl apply -f k8s/rbac/service-account.yaml

# Deploy the Simulation App and the Bot
kubectl apply -f k8s/deployment.yaml
4. Configure Monitoring (The Logic)
Apply the Prometheus Rule that defines the "unhealthy" state (e.g., Memory > 300MB).

YAML
# k8s/prometheus-rule.yaml (Example)
apiVersion: [monitoring.coreos.com/v1](https://monitoring.coreos.com/v1)
kind: PrometheusRule
metadata:
  name: memory-leak-rules
spec:
  groups:
  - name: heavy-apps
    rules:
    - alert: MemoryLeakDetected
      expr: container_memory_usage_bytes > 314572800 # 300MB
      for: 30s
      labels:
        severity: critical
🧪 Simulation Scenario
The repository includes a bad-app engineered to simulate a progressive memory leak (~50MB/sec).

Start: The bad-app pod starts and begins consuming RAM.

Detect: Prometheus notices consumption crossing the 300MB threshold.

Alert: Alertmanager fires a payload to http://healer-bot/webhook.

Heal: The Bot receives the signal, identifies the specific pod, and issues a DELETE command.

Result: Kubernetes automatically reschedules a fresh, healthy pod.

Logs Evidence:

Plaintext
INFO:HealerBot: 📩 Received Alert Payload: 1 alerts
INFO:HealerBot: 🚨 TARGET IDENTIFIED: Pod 'bad-app-7f8d9c' in 'default'
INFO:HealerBot: 💉 HEALED: Pod 'bad-app-7f8d9c' was successfully deleted.
📊 Business Impact & NIW Context
This project demonstrates advanced Site Reliability Engineering (SRE) principles essential for maintaining critical US digital infrastructure:

Operational Efficiency: Eliminates "Toil" by automating repetitive troubleshooting tasks, allowing engineers to focus on architecture.

High Availability (HA): Drastically lowers downtime by reacting to issues in milliseconds rather than minutes.

Cost Optimization: Prevents runaway processes from consuming cluster-wide resources (CPU/RAM), directly impacting cloud billing efficiency.

🛡️ Security
RBAC Least Privilege: The controller operates with a scoped ServiceAccount, limited strictly to delete actions on specific namespaces. No cluster-admin access is required.

Audit Logging: All remediation actions are logged for compliance and post-mortem analysis.

📜 License
MIT License. Open for contribution.
