import os
import time
import psutil
from datetime import datetime
import subprocess

BENCH_LOG = "/home/nic/nyxeos_pi/journal/bench.txt"

def log(msg):
    os.makedirs(os.path.dirname(BENCH_LOG), exist_ok=True)
    with open(BENCH_LOG, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")
    print(msg)

def get_cpu_benchmark():
    try:
        output = subprocess.check_output(
            ["sysbench", "cpu", "--cpu-max-prime=20000", "run"],
            stderr=subprocess.STDOUT, text=True
        )
        for line in output.splitlines():
            if "total time:" in line:
                return line.strip()
        return "CPU: Benchmark result not found"
    except Exception as e:
        return f"CPU benchmark failed: {e}"

def get_ram_bandwidth():
    try:
        output = subprocess.check_output(["mbw", "-n", "3", "100"], stderr=subprocess.STDOUT, text=True)
        last_line = output.strip().splitlines()[-2]
        return f"RAM {last_line}"
    except Exception as e:
        return f"RAM benchmark failed: {e}"

def get_ssd_speed():
    try:
        output = subprocess.check_output(["fio", "--name=test", "--size=512M", "--filename=testfile", "--bs=128k", "--rw=readwrite", "--ioengine=libaio", "--iodepth=16", "--numjobs=1", "--direct=1", "--runtime=5", "--time_based"], stderr=subprocess.STDOUT, text=True)
        lines = [line for line in output.splitlines() if "READ:" in line or "WRITE:" in line]
        return " | ".join(lines)
    except Exception as e:
        return f"SSD benchmark failed: {e}"

def run_benchmarks():
    log("=== Benchmark started ===")
    log(get_cpu_benchmark())
    log(get_ram_bandwidth())
    log(get_ssd_speed())
    log("=== Benchmark completed ===")

if __name__ == "__main__":
    run_benchmarks()
