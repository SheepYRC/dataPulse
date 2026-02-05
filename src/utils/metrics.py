import psutil

def get_system_metrics():
    """Wrapper for psutil metrics."""
    return {
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
