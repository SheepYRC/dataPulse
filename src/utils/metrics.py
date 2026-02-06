import psutil

def get_system_metrics():
    """Wrapper for psutil metrics."""

    # interval = 1 秒 来计算 CPU 频率
    # 这对于 5 秒刷新的 Fragment 来说几乎无感知
    cpu_usage = psutil.cpu_percent(interval=1)

    # 内存和磁盘是瞬时值，不需要 interval
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    return {
        "cpu": cpu_usage,
        "memory": memory,
        "disk": disk
    }
