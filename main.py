import time
import threading
import statistics
from tls_server import run_server
from tls_client import run_client_handshake
from pqc_kyber import measure_kyber_kem

def benchmark_tls(iterations=100):
    latencies = []
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Give server a moment to start
    time.sleep(1)
    
    for _ in range(iterations):
        lat = run_client_handshake()
        if lat is not None:
            latencies.append(lat)
        time.sleep(0.01) # Small delay to avoid overwhelming
        
    return latencies

def benchmark_kyber(iterations=100):
    latencies = []
    pk_size = 0
    ct_size = 0
    
    for _ in range(iterations):
        res = measure_kyber_kem("Kyber768")
        if res:
            latencies.append(res["latency_ms"])
            pk_size = res["pk_size"]
            ct_size = res["ct_size"]
            
    return latencies, pk_size, ct_size

def main():
    ITERATIONS = 100
    print(f"Running benchmarks with {ITERATIONS} iterations...")
    
    # 1. Classic TLS (ECDHE)
    print("Benchmarking Classic TLS (ECDHE)...")
    tls_latencies = benchmark_tls(ITERATIONS)
    if not tls_latencies:
        print("TLS Benchmark failed!")
        return

    tls_mean = statistics.mean(tls_latencies)
    tls_stdev = statistics.stdev(tls_latencies)
    
    # 2. PQC (Kyber)
    print("Benchmarking PQC (Kyber768)...")
    kyber_latencies, kyber_pk_size, kyber_ct_size = benchmark_kyber(ITERATIONS)
    
    kyber_mean = statistics.mean(kyber_latencies)
    kyber_stdev = statistics.stdev(kyber_latencies)
    
    # 3. Report
    print("\n" + "="*60)
    print(f"{'Metric':<25} | {'Classic (ECDHE)':<15} | {'PQC (Kyber768)':<15}")
    print("-" * 60)
    
    # Sizes
    # ECDHE P-256 public key is 64 bytes (uncompressed) or 33 bytes (compressed). 
    # TLS 1.3 usually sends 32 bytes for X25519 or ~65 bytes for P-256.
    # Let's assume ~64 bytes for P-256 for comparison.
    ecdhe_pk_size = 64 
    ecdhe_ct_size = 0 # Implicit in TLS, but effectively the key share is the "ciphertext" equivalent
    
    print(f"{'Public Key Size (Bytes)':<25} | {ecdhe_pk_size:<15} | {kyber_pk_size:<15}")
    print(f"{'Ciphertext Size (Bytes)':<25} | {ecdhe_ct_size:<15} | {kyber_ct_size:<15}")
    print("-" * 60)
    
    # Latency
    print(f"{'Mean Latency (ms)':<25} | {tls_mean:<15.4f} | {kyber_mean:<15.4f}")
    print(f"{'Std Dev (ms)':<25} | {tls_stdev:<15.4f} | {kyber_stdev:<15.4f}")
    print("="*60)
    
    # Overhead calculation
    latency_overhead = ((kyber_mean - tls_mean) / tls_mean) * 100
    print(f"\nLatency Overhead (Kyber vs TLS Handshake): {latency_overhead:.2f}%")
    print("Note: TLS latency includes full TCP+TLS handshake. Kyber latency is pure KEM crypto operations.")

if __name__ == "__main__":
    main()
