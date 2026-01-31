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
