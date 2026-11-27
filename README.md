# GuardianNodes RoadSoS

An advanced AI-powered emergency road accident response system built with Python and Streamlit.

## Features
- 🧠 **AI Zero-Shot Classification Triage Engine** (DistilBERT / MiniLM / Heuristic fallback)
- 🗺️ **NetworkX Dijkstra Traffic-Aware Routing**
- 📡 **BLE/Wi-Fi Direct Mesh Protocol Simulator** with binary struct & CRC-32 checksums
- 📊 **Real-Time Operations Metrics Dashboard**

---

## Quickstart

### 1. Run with Docker (Recommended)

#### Option A: Docker Compose
```bash
docker compose up --build
```
Access the application at `http://localhost:8501`.

#### Option B: Standard Docker
```bash
# Build image
docker build -t roadsafety:latest .

# Run container
docker run -p 8501:8501 --name roadsafety-app roadsafety:latest
```

---

### 2. Run Locally

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Streamlit application
streamlit run app.py
```

---

## Running Pytest Suite

Run the full automated test suite (55 unit & integration tests):

```bash
# Run all tests
pytest

# Run tests with code coverage report
pytest --cov=modules --cov-report=term-missing
```

---

## Tech Stack
- **Python 3.11+**
- **Streamlit** (UI & Real-Time Dashboard)
- **HuggingFace Transformers & PyTorch** (Zero-Shot Classification)
- **NetworkX** (Graph Pathfinding & Dijkstra Routing)
- **Plotly** (Dynamic Radar Charts & Incident Mapping)
- **PyTest** (Automated Test Suite & Coverage)
- **Docker & Docker Compose** (Containerization & Deployment)
