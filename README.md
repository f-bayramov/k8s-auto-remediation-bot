# Kubernetes Auto-Remediation Controller 🚑

![Status](https://img.shields.io/badge/status-active-success)
![Kubernetes](https://img.shields.io/badge/kubernetes-v1.27%2B-blue)
![Python](https://img.shields.io/badge/python-3.9-yellow)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

**An event-driven self-healing framework for Kubernetes clusters that eliminates manual intervention for common infrastructure failures.**

## 📖 Executive Summary
In high-scale production environments, "Mean Time to Recovery" (MTTR) is a critical KPI. Manual troubleshooting of memory leaks or stuck processes can take minutes or hours. 

This project implements a **Level-4 Autonomous System** (Self-Healing) that detects anomalies via Prometheus metrics and executes automated remediation strategies via a custom Kubernetes Operator logic.

## 🏗️ Architecture Design

The system operates on a closed-loop feedback mechanism:

```mermaid
graph LR
    A[Target Application] -->|Metrics Exporter| B(Prometheus)
    B -->|Alert: HighMemory| C{Alertmanager}
    C -->|Webhook Payload| D[Healer Bot Controller]
    D -->|K8s API Call| E((Kubernetes Control Plane))
    E -->|Restart Pod| A



    
