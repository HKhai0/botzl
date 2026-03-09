import psutil
import time
from logging_utils import Logging

logger = Logging()

def get_high_cpu_process():
    processes = [(p.info['pid'], p.info['name'], p.info['cpu_percent']) 
                 for p in psutil.process_iter(['pid', 'name', 'cpu_percent']) 
                 if p.info['cpu_percent'] > 0 and p.info['pid'] != 0]
    return max(processes, key=lambda p: p[2]) if processes else None

def optimize_cpu_usage():
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        get = f"Mức sử dụng CPU: {cpu_usage}%"
        logger.logger('CHECK CPU', get)
        
        if cpu_usage > 80:
            high_cpu_process = get_high_cpu_process()
            if high_cpu_process:
                pid, name, cpu_percent = high_cpu_process
                check = f"Tiến trình đang sử dụng nhiều CPU: {name} (PID: {pid}, Sử dụng CPU: {cpu_percent}%)"
                logger.logger('CLEAR CPU', check)
                
                try:
                    p = psutil.Process(pid)
                    if p.status() == psutil.STATUS_RUNNING:
                        p.nice(psutil.IDLE_PRIORITY_CLASS)
                        logger.warning(f"Đã giảm mức ưu tiên của tiến trình: {name}")
                except Exception as e:
                    logger.error(f"Lỗi khi xử lý tiến trình: {e}")

        time.sleep(120)

if __name__ == "__main__":
    optimize_cpu_usage()
