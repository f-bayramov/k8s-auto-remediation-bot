from fastapi import FastAPI, Request
from kubernetes import client, config
import logging
import os

# Configure logging to capture remediation events
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("HealerBot")

app = FastAPI()

# Load Kubernetes configuration
# This allows the pod to authenticate with the K8s API using the ServiceAccount
try:
    config.load_incluster_config()
    logger.info("✅ Successfully loaded in-cluster Kubernetes config.")
except:
    logger.warning("⚠️ Failed to load in-cluster config. Falling back to local kubeconfig (Dev Mode).")
    config.load_kube_config()

# Initialize the CoreV1 API client
v1 = client.CoreV1Api()

@app.post("/webhook")
async def handle_alert(request: Request):
    """
    Endpoint to receive webhook payloads from Alertmanager.
    """
    payload = await request.json()
    logger.info(f"📩 Received Alert Payload: Processing {len(payload.get('alerts', []))} alerts...")

    for alert in payload.get('alerts', []):
        status = alert.get('status')
        labels = alert.get('labels', {})
        
        alert_name = labels.get('alertname')
        pod_name = labels.get('pod')
        namespace = labels.get('namespace')

        # Check if the alert is firing and matches our specific rule
        if status == "firing" and alert_name == "MemoryLeakDetected":
            logger.info(f"🚨 TARGET IDENTIFIED: Pod '{pod_name}' in namespace '{namespace}' is unhealthy.")
            delete_pod(namespace, pod_name)
            
    return {"status": "processed"}

def delete_pod(ns, name):
    """
    Deletes the target pod to trigger a restart by the Deployment controller.
    """
    try:
        v1.delete_namespaced_pod(name, ns)
        logger.info(f"💉 HEALING ACTION: Pod '{name}' successfully deleted. Kubernetes will reschedule a fresh instance.")
    except Exception as e:
        logger.error(f"❌ REMEDIATION FAILED: Could not delete pod '{name}'. Reason: {e}")

if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
