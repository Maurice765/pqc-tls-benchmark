import json
import os
import sys
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np

# Configuration
ALGORITHMS = [
    "mlkem512", "P-256", "p256_mlkem512",
    "mlkem768", "P-384", "p384_mlkem768",
    "mlkem1024", "P-521", "p521_mlkem1024"
]

ALGO_DETAILS = {
    "mlkem512": {"pk": 800, "ct": 768, "label": "ML-KEM-512"},
    "P-256": {"pk": 65, "ct": 65, "label": "P-256"},
    "p256_mlkem512": {"pk": 865, "ct": 833, "label": "P-256 + ML-KEM-512"},
    
    "mlkem768": {"pk": 1184, "ct": 1088, "label": "ML-KEM-768"},
    "P-384": {"pk": 97, "ct": 97, "label": "P-384"},
    "p384_mlkem768": {"pk": 1281, "ct": 1185, "label": "P-384 + ML-KEM-768"},
    
    "mlkem1024": {"pk": 1568, "ct": 1568, "label": "ML-KEM-1024"},
    "P-521": {"pk": 133, "ct": 133, "label": "P-521"},
    "p521_mlkem1024": {"pk": 1701, "ct": 1701, "label": "P-521 + ML-KEM-1024"},
}
# Hybrid: p256_mlkem512, p384_mlkem768, p521_mlkem1024

LATENCIES = [0, 50] # ms
LOSS_RATES = [0,5] # percent
ITERATIONS = 20

def run_command(cmd, shell=True):
    # print(f"Debug: {cmd}")
    result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
    if result.returncode != 0:
        # Check if it is just a warning. Docker compose prints warnings to stderr.
        # If output is empty but return code is 0, it is fine.
        # But here return code is NOT 0.
        pass
        # print(f"Cmd failed: {cmd}\nStderr: {result.stderr}")
    
    # Docker compose can be noisy on stderr even on success.
    # We return stdout.
    return result.stdout.strip()

def setup_server_file():
    print("Setting up 10MB test file...")
    filename = "10MB.bin"
    # Create local 10MB file
    with open(filename, "wb") as f:
        f.write(os.urandom(10 * 1024 * 1024))
    
    # Copy to server
    # Note: openquantumsafe/nginx web root is /opt/nginx/html
    cmd = f"docker compose cp {filename} server:/opt/nginx/html/testfile"
    run_command(cmd)
    
    # Cleanup local
    os.remove(filename)

def set_network(latency_ms, loss_percent):
    # Clean up first
    run_command("docker compose exec -T client tc qdisc del dev eth0 root")
    
    args = []
    if latency_ms > 0:
        args.append(f"delay {latency_ms}ms")
    if loss_percent > 0:
        args.append(f"loss {loss_percent}%")
    
    if args:
        cmd = f"docker compose exec -T client tc qdisc add dev eth0 root netem {' '.join(args)}"
        run_command(cmd)

def benchmark_handshake(algo, latency):
    # Measure time_appconnect using curl
    # Algo can be passed to --curves
    # Use -k for insecure
    # URL: https://server:4433/index.html (small file)
    
    cmd = f"docker compose exec -T client curl -k --curves {algo} -o /dev/null -s -w %{{time_appconnect}} https://server:4433/index.html"
    out = run_command(cmd)
    try:
        val = float(out)
        return val
    except:
        return None

def benchmark_transfer(algo, latency):
    # Measure transfer time for 10MB file
    # We want (time_total - time_appconnect)
    cmd = f"docker compose exec -T client curl -k --curves {algo} -o /dev/null -s -w %{{time_appconnect}},%{{time_total}} https://server:4433/testfile"
    out = run_command(cmd)
    try:
        parts = out.split(',')
        if len(parts) != 2: return None
        t_hs = float(parts[0])
        t_total = float(parts[1])
        return t_total - t_hs
    except:
        return None

def main():
    print("Starting Benchmark...")
    setup_server_file()
    
    final_results = []
    
    for lat in LATENCIES:
        for loss in LOSS_RATES:
            print(f"\n--- Latency: {lat}ms, Loss: {loss}% ---")
            set_network(lat, loss)
            for algo in ALGORITHMS:
                details = ALGO_DETAILS.get(algo, {"pk": "?", "ct": "?", "label": algo})
                print(f"Benchmarking {algo} [PK: {details['pk']}B, CT: {details['ct']}B] ", end="", flush=True)
                
                hs_times = []
                tx_times = []
                
                # Use a few warmups
                benchmark_handshake(algo, lat)
                
                for _ in range(ITERATIONS):
                    hs = benchmark_handshake(algo, lat)
                    if hs is not None:
                        hs_times.append(hs)
                    
                    tx = benchmark_transfer(algo, lat)
                    if tx is not None:
                        tx_times.append(tx)
                    print(".", end="", flush=True)
                    
                avg_hs = sum(hs_times)/len(hs_times) if hs_times else 0
                avg_tx = sum(tx_times)/len(tx_times) if tx_times else 0
                
                print(f" Done. HS: {avg_hs:.4f}s, TX: {avg_tx:.4f}s")
                
                final_results.append({
                    "latency_ms": lat,
                    "packet_loss_percent": loss,
                    "algorithm": algo,
                    "handshake_time_s": avg_hs,
                    "transfer_time_s": avg_tx,
                    "key_details": ALGO_DETAILS.get(algo, {}),
                    "handshake_raw": hs_times,
                    "transfer_raw": tx_times
                })
            
    # Cleanup
    set_network(0, 0)
    
    # Create results directory
    os.makedirs("results", exist_ok=True)
    
    # Save Results
    json_path = "results/results.json"
    with open(json_path, 'w') as f:
        json.dump(final_results, f, indent=2)
    print(f"\nResults saved to {json_path}")
    
    # Plotting
    try:
        plot_results(final_results)
        plot_boxplots(final_results)
    except Exception as e:
        print(f"Plotting failed: {e}")

def plot_results(results):
    # Unique scenarios (lat, loss)
    scenarios = sorted(list(set((r['latency_ms'], r.get('packet_loss_percent', 0)) for r in results)))
    algos = sorted(list(set(r['algorithm'] for r in results)))
    
    # Setup data structures
    # We want grouped bars. Outer group: Scenario. Inner group: Algo.
    
    x = np.arange(len(scenarios))  # the label locations
    width = 0.35  # the width of the bars
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(max(12, len(scenarios)*2), 6))
    
    # Prepare data for easy plotting
    # {algo: [val_at_scen0, val_at_scen1]}
    hs_data = {algo: [] for algo in algos}
    tx_data = {algo: [] for algo in algos}
    
    for algo in algos:
        for lat, loss in scenarios:
            # Find matching result
            res = next((r for r in results if r['latency_ms'] == lat and r.get('packet_loss_percent', 0) == loss and r['algorithm'] == algo), None)
            hs_data[algo].append(res['handshake_time_s'] if res else 0)
            tx_data[algo].append(res['transfer_time_s'] if res else 0)
    
    # Plot Handshake
    multiplier = 0
    bar_width = 0.8 / len(algos)
    
    for algo, measurements in hs_data.items():
        offset = bar_width * multiplier
        rects = ax1.bar(x + offset, measurements, bar_width, label=algo)
        multiplier += 1

    ax1.set_ylabel('Time (s)')
    ax1.set_title('Handshake Time by Network Condition')
    ax1.set_xticks(x + bar_width * (len(algos) - 1) / 2)
    ax1.set_xticklabels([f"{lat}ms, {loss}% Loss" for lat, loss in scenarios], rotation=45, ha='right')
    ax1.legend()
    # ax1.set_yscale('log') # Optional: log scale if differences are huge

    # Plot Transfer
    multiplier = 0
    for algo, measurements in tx_data.items():
        offset = bar_width * multiplier
        rects = ax2.bar(x + offset, measurements, bar_width, label=algo)
        multiplier += 1

    ax2.set_ylabel('Time (s)')
    ax2.set_title('Transfer Time (10MB) by Network Condition')
    ax2.set_xticks(x + bar_width * (len(algos) - 1) / 2)
    ax2.set_xticklabels([f"{lat}ms, {loss}% Loss" for lat, loss in scenarios], rotation=45, ha='right')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('results/benchmark_plot.png')
    print("Bar plot saved to results/benchmark_plot.png")

def plot_boxplots(results):
    # Unique scenarios (lat, loss)
    scenarios = sorted(list(set((r['latency_ms'], r.get('packet_loss_percent', 0)) for r in results)))
    
    # Define groups: (Label, Kyber_Algo, ECDHE_Algo, Hybrid_Algo)
    groups = [
        ("Level 1\n(ML-KEM-512 / P-256)", "mlkem512", "P-256", "p256_mlkem512"),
        ("Level 3\n(ML-KEM-768 / P-384)", "mlkem768", "P-384", "p384_mlkem768"),
        ("Level 5\n(ML-KEM-1024 / P-521)", "mlkem1024", "P-521", "p521_mlkem1024")
    ]
    
    for lat, loss in scenarios:
        lat_results = {r['algorithm']: r for r in results if r['latency_ms'] == lat and r.get('packet_loss_percent', 0) == loss}
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        y_locs = np.arange(len(groups))
        
        # Prepare data arrays
        k_hs, e_hs, h_hs = [], [], []
        k_tx, e_tx, h_tx = [], [], []
        
        for label, k_algo, e_algo, h_algo in groups:
            k_res = lat_results.get(k_algo)
            e_res = lat_results.get(e_algo)
            h_res = lat_results.get(h_algo)
            
            k_hs.append(k_res['handshake_raw'] if k_res else [])
            e_hs.append(e_res['handshake_raw'] if e_res else [])
            h_hs.append(h_res['handshake_raw'] if h_res else [])
            
            k_tx.append(k_res['transfer_raw'] if k_res else [])
            e_tx.append(e_res['transfer_raw'] if e_res else [])
            h_tx.append(h_res['transfer_raw'] if h_res else [])

        # Plot Helper
        def draw_grouped_boxplot(ax, data1, data2, data3, title):
            # data1=Kyber, data2=ECDHE, data3=Hybrid
            
            # Box 1 (Kyber) at y - 0.2
            bp1 = ax.boxplot(data1, positions=y_locs - 0.2, widths=0.15, vert=False, patch_artist=True)
            # Box 2 (ECDHE) at y
            bp2 = ax.boxplot(data2, positions=y_locs, widths=0.15, vert=False, patch_artist=True)
            # Box 3 (Hybrid) at y + 0.2
            bp3 = ax.boxplot(data3, positions=y_locs + 0.2, widths=0.15, vert=False, patch_artist=True)
            
            # Coloring
            for patch in bp1['boxes']: patch.set_facecolor('skyblue')     # Kyber
            for patch in bp2['boxes']: patch.set_facecolor('lightsalmon') # ECDHE
            for patch in bp3['boxes']: patch.set_facecolor('lightgreen')  # Hybrid
            
            ax.set_yticks(y_locs)
            ax.set_yticklabels([g[0] for g in groups])
            ax.invert_yaxis() 
            ax.set_title(title)
            ax.set_xlabel("Time (s)")
            
            # Legend
            ax.legend([bp1["boxes"][0], bp2["boxes"][0], bp3["boxes"][0]], 
                      ['Kyber/ML-KEM', 'ECDHE', 'Hybrid'], loc='best')

        draw_grouped_boxplot(ax1, k_hs, e_hs, h_hs, f"Handshake Time @ {lat}ms / {loss}% Loss")
        draw_grouped_boxplot(ax2, k_tx, e_tx, h_tx, f"Transfer Time (10MB) @ {lat}ms / {loss}% Loss")

        plt.tight_layout()
        filename = f"results/boxplot_lat{lat}ms_loss{loss}.png"
        plt.savefig(filename)
        plt.close(fig)
        print(f"Boxplot saved to {filename}")

if __name__ == "__main__":
    main()
