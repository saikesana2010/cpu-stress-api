# CPU Burn Lab

A tiny [FastAPI](https://fastapi.tiangolo.com/) service for **deliberately stressing CPU cores on demand** via HTTP endpoints.

It's useful for testing things like:

- Autoscaling rules (CPU-based scale-up/scale-down)
- Monitoring & alerting thresholds
- Load balancer / health-check behavior under load

> ⚠️ **Warning:** These endpoints intentionally max out the machine's CPU. Run only in a controlled/test environment and do **not** expose it publicly without authentication.

---

## Requirements

- Python 3.9+
- Dependencies listed in [`requirements.txt`](requirements.txt)

## Setup

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running

```bash
python app.py
```

The server starts on **http://0.0.0.0:8000**.

Interactive API docs (Swagger UI) are available at **http://localhost:8000/docs**.

---

## Endpoints

| Method | Path         | Description |
|--------|--------------|-------------|
| GET    | `/cpu-busy`  | Spawns one process per CPU core and keeps them all busy. |
| GET    | `/cpu-full`  | Saturates the CPU using a configurable pool of worker processes. |
| GET    | `/health`    | Liveness check — returns status and current UTC time. |
| GET    | `/hello`     | Simple demo endpoint. |

### `GET /cpu-busy`

Keeps **all** CPU cores busy for a given duration.

| Query param | Type | Default | Range  | Description |
|-------------|------|---------|--------|-------------|
| `seconds`   | int  | `5`     | 1–60   | How long to keep the cores busy. |

```bash
curl "http://localhost:8000/cpu-busy?seconds=10"
```

### `GET /cpu-full`

Fully utilizes the CPU across a configurable number of worker processes with tunable workload intensity.

| Query param  | Type  | Default      | Range          | Description |
|--------------|-------|--------------|----------------|-------------|
| `seconds`    | float | `10.0`       | > 0 to 600     | Duration of the burn. |
| `complexity` | int   | `5000`       | 100 to 5,000,000 | Work done per loop iteration (higher = more intense). |
| `processes`  | int   | `# of cores` | 1 to 256       | Number of worker processes to spawn. |

```bash
curl "http://localhost:8000/cpu-full?seconds=15&complexity=10000&processes=4"
```

### `GET /health`

```bash
curl "http://localhost:8000/health"
# {"status": "ok", "time": "2026-07-01T12:00:00+00:00"}
```

### `GET /hello`

| Query param | Type | Default   | Description |
|-------------|------|-----------|-------------|
| `name`      | str  | `"World"` | Name to greet. |

```bash
curl "http://localhost:8000/hello?name=Nagasai"
```

---

## Project structure

```
.
├── app.py             # The entire FastAPI application
├── requirements.txt   # Python dependencies
├── .gitignore
└── README.md
```

## Notes

- The CPU-burn endpoints run **synchronously** and block until the burn completes — this is intentional for a stress tool, but the server won't serve other requests during a burn.
