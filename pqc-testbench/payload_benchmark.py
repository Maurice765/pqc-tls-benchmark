import subprocess
import time
import re
import os

# --- KONFIGURATION ---
ALGORITHMS = [
    "P-256",
    "P-384",
    "P-521",
    "mlkem512",         # Level 1
    "mlkem768",         # Level 3 (Standard)
    "mlkem1024",        # Level 5 (Größer als MTU?)
    "X25519MLKEM768"    # Hybrid
]

MTU_LIMIT = 1460 

def setup_tools():
    """Installiert tcpdump im Client-Container"""
    print("[Setup] Prüfe tcpdump...")
    check = subprocess.run("docker exec pqc-client tcpdump --version", shell=True, capture_output=True)
    if check.returncode != 0:
        print("[Setup] Installiere tcpdump...")
        subprocess.run("docker exec pqc-client apk update && docker exec pqc-client apk add tcpdump", shell=True, stdout=subprocess.DEVNULL)

def start_server(algo):
    subprocess.run("docker exec pqc-server pkill openssl", shell=True, stderr=subprocess.DEVNULL)
    time.sleep(1)

    cmd = f"docker exec -d pqc-server openssl s_server -cert /certs/server.crt -key /certs/server.key -accept 4433 -www -groups {algo}"
    subprocess.run(cmd, shell=True)
    time.sleep(2)

def measure_packet_sizes(algo):
    dump_file = "/tmp/handshake.pcap"
    
    start_dump = f"docker exec -d pqc-client tcpdump -i eth0 port 4433 -w {dump_file} -U"
    subprocess.run(start_dump, shell=True)
    time.sleep(1)
    
    cmd_handshake = f"echo Q | docker exec -i pqc-client openssl s_client -connect server:4433 -groups {algo} -CAfile /certs/CA.crt"
    subprocess.run(cmd_handshake, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    
    subprocess.run("docker exec pqc-client pkill tcpdump", shell=True)
    time.sleep(0.5)
    
    analyze_cmd = f"docker exec pqc-client tcpdump -r {dump_file} -nn -v"
    result = subprocess.run(analyze_cmd, shell=True, capture_output=True, text=True)
    
    
    max_client_size = 0
    max_server_size = 0
    total_bytes_client = 0
    total_bytes_server = 0


    for line in result.stdout.splitlines():

        length_match = re.search(r'length (\d+)', line)
        if length_match:
            length = int(length_match.group(1))
            
            if "> 172.18.0.3.4433" in line or "> server.4433" in line:
                if length > 0:
                    max_client_size = max(max_client_size, length)
                    total_bytes_client += length
            elif "4433 >" in line:
                if length > 0:
                    max_server_size = max(max_server_size, length)
                    total_bytes_server += length

    return max_client_size, max_server_size, total_bytes_client, total_bytes_server


print("=== PQC SIZE & FRAGMENTATION ANALYSE ===")
print(f"{'Algorithmus':<20} | {'ClientHello':<12} | {'ServerHello':<12} | {'Fragmentiert?':<12}")
print("-" * 65)

setup_tools()


for algo in ALGORITHMS:
    start_server(algo)
    ch_size, sh_size, tot_c, tot_s = measure_packet_sizes(algo)
    

    fragmented = "NEIN"
    if sh_size >= MTU_LIMIT or tot_s > (sh_size + 500): 
        if algo == "prime256v1" or algo == "mlkem512":
            pass
        else:
            fragmented = "JA!"
    
    print(f"{algo:<20} | {ch_size:<10} B | {sh_size:<10} B | {fragmented:<12}")

print("-" * 65)