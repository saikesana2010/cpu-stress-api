import re
from datetime import datetime, timezone
import uvicorn
from fastapi import FastAPI, HTTPException, Query
import time
import math
import multiprocessing
import multiprocessing as mp

app = FastAPI(title="CPU Burn Lab",version="1.0")

# ---------- Core logic (helpers) ----------


def burn_worker(seconds: float, complexity: int):
    end = time.time() + seconds
    x = 0.0
    while time.time() < end:
        for i in range(complexity):
            x = (x + math.sqrt(i + 1)) % 1.0
    return x


def cpu_task(duration: int):
    """CPU intensive task for the given duration."""
    end_time = time.time() + duration
    while time.time() < end_time:
        math.sqrt(987654321)  # Heavy math operation

# ---------- API endpoints ----------

@app.get("/cpu-busy")
def make_cpu_busy(seconds: int = Query(5, ge=1, le=60)):
    """
    Keep all CPU cores busy for 'seconds' duration.
    Default: 5 sec, Max: 60 sec
    """
    cores = multiprocessing.cpu_count()
    processes = []

    # Start CPU busy processes
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_task, args=(seconds,))
        p.start()
        processes.append(p)

    # Wait for all processes to finish
    for p in processes:
        p.join()

    return {
        "message": f"Kept {cores} CPU cores busy for {seconds} seconds"
    }


@app.get("/cpu-full")
def cpu_full_burn(
        seconds: float = Query(10.0, gt=0, le=600),
        complexity: int = Query(5000, gt=100, le=5_000_000),
        processes: int = Query(mp.cpu_count(), gt=0, le=256)
):
    """
    Fully utilize CPU across all available cores by spawning `processes` workers.
    """
    ctx = mp.get_context("spawn")  # works cross-platform
    with ctx.Pool(processes) as pool:
        pool.starmap(burn_worker, [(seconds, complexity)] * processes)
    return {
        "mode": "multi-process",
        "seconds": seconds,
        "complexity": complexity,
        "processes_used": processes,
        "status": "CPU burn complete"
    }

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.now(timezone.utc).isoformat()}

@app.get("/hello")
def hello(name: str = Query("World")):
    wish = "Hello"
    return wish + name


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
