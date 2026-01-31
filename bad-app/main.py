import time
import os

# Global list to hold data and simulate memory leak
memory_hog = []

print("🔥 Bad App Started: Initiating intentional memory leak...", flush=True)

try:
    while True:
        # Allocate approx. 50MB of string data
        chunk = ' ' * 50 * 1024 * 1024 
        memory_hog.append(chunk)
        
        # Calculate current usage based on the list size
        current_usage_mb = len(memory_hog) * 50
        print(f"Stats: Consuming {current_usage_mb} MB RAM...", flush=True)
        
        # Wait 2 seconds before next allocation to simulate gradual leak
        time.sleep(2)
except MemoryError:
    print("💀 System OOM: The application has crashed due to lack of memory.")
