# PQC-TLS-Benchmark

Eine Benchmark-Suite zur Bewertung von Post-Quantum Cryptography (PQC) in TLS-Kontexten. Vergleicht traditionelle elliptische Kurven-Kryptographie (ECC) mit PQC-Algorithmen wie Kyber, fokussiert auf Leistungsmetriken wie Latenz und Schlüsselgrößen.

## Installation

1. Repository klonen:
   ```bash
   git clone https://github.com/yourusername/pqc-tls-benchmark.git
   cd pqc-tls-benchmark
   ```

2. Setup-Script ausführen:
   ```bash
   ./setup.sh
   ```
   Erstellt eine virtuelle Umgebung und installiert erforderliche Pakete (`cryptography`, `kyber-py`).

## Verwendung

1. Virtuelle Umgebung aktivieren:
   ```bash
   source .venv/bin/activate
   ```

2. Benchmark ausführen:
   ```bash
   python3 benchmarks/benchmark.py
   ```