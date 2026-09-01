# QGSS26-Labs

Hands-on lab exercises for the **Qiskit Global Summer School 2026**.

## Prerequisites

- Python 3.14+
- [UV](https://docs.astral.sh/uv/) package manager
- [IBM Quantum](https://quantum.ibm.com/) account (free tier works)

## Setup

1. Clone the repo and navigate to the labs directory:

   ```bash
   git clone <repo-url>
   cd QGSS26-Labs
   ```

2. Create your `.env` file with your IBM Quantum credentials:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and fill in your API key and instance CRN from [IBM Quantum](https://quantum.ibm.com/).

3. Install dependencies:

   ```bash
   uv pip install -r requirements.txt
   ```

4. Run a lab:

   ```bash
   marimo run QGSS2026_Lab0.py
   ```

## Labs

| Lab | Title | Topics | QPU Time |
|-----|-------|--------|----------|
| 0 | Welcome to QGSS 2026 | Package setup, Sampler & Estimator primitives, statevectors, Qiskit C API | None |
| 1 | Building Quantum Circuits for Real Hardware | Basic gates, circuit depth, transpilation, noisy simulation (133-qubit IBM Heron) | None |
| 2 | Noise, Backends, and Benchmarking | Backend properties, noise models, transpilation comparison, backend benchmarking | None |
| 3 | Your New Tool For Quantum Advantage | Samplomatic, error mitigation, Pauli propagation, PNA & Shaded Lightcones add-ons | Minimal |
| 4a | Towards Quantum Advantage — Overview | Quantum advantage criteria, Quantum Advantage Tracker | None |
| 4b | QAOA for the Partition Problem | QAOA, error mitigation, Pauli correlation encoding | ~5 min 30 sec (Heron r2) |
| 4c | Sample-Based Quantum Diagonalization *(bonus)* | SQD, N2 molecule ground energy | ~2–10 sec (Heron r2 / Nighthawk r1) |

## Directory Structure

```
QGSS26-Labs/
├── QGSS2026_Lab*.py      # Marimo notebook apps (primary)
├── notebooks/             # Jupyter notebook versions
├── utils/                 # Helper functions and precomputed data
├── __marimo__/            # Marimo session cache (auto-generated)
├── .env.example           # Environment variable template
└── requirements.txt       # Python dependencies
```

## Running in Jupyter

Jupyter versions of each lab are in the `notebooks/` directory:

```bash
uv pip install jupyter
jupyter notebook notebooks/QGSS2026_Lab0.ipynb
```
