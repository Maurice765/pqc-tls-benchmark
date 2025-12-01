How to Run
Activate the environment (if not already active):

source .venv/bin/activate
Run the benchmark:

python3 main.py
Expected Output
You will see a table comparing the two approaches.

Sample Output:

Running benchmarks with 100 iterations...
Benchmarking Classic TLS (ECDHE)...
Benchmarking PQC (Kyber768)...
============================================================
Metric                    | Classic (ECDHE) | PQC (Kyber768)
------------------------------------------------------------
Public Key Size (Bytes)   | 64              | 1184
Ciphertext Size (Bytes)   | 0               | 1088
------------------------------------------------------------
Mean Latency (ms)         | 1.2521          | 0.8543
Std Dev (ms)              | 0.1200          | 0.0500
============================================================
Latency Overhead (Kyber vs TLS Handshake): -31.77%
Note: TLS latency includes full TCP+TLS handshake. Kyber latency is pure KEM crypto operations.
NOTE

Interpretation:

Key Sizes: Kyber keys and ciphertexts are significantly larger (approx 1KB each) compared to ECC (64 bytes). This is the main trade-off.
Latency: The computational latency of Kyber is very low (often faster than ECC). However, in a real network (not localhost), the transmission of the larger keys would add network latency. This prototype measures pure computation for Kyber vs full handshake for TLS.