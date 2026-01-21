import subprocess
import re
import sys
import shutil

# Algorithms to check (matching benchmark.py)
ALGORITHMS = [
    "mlkem512", "P-256", "p256_mlkem512",
    "mlkem768", "P-384", "p384_mlkem768",
    "mlkem1024", "P-521", "p521_mlkem1024"
]

def run_openssl_trace(algo):
    """
    Runs openssl s_client inside the client container with -trace to capture handshake details.
    """
    # We use 'echo Q' to quit the connection immediately after handshake.
    # We use sh -c to handle piping inside the container.
    cmd = [
        "docker", "compose", "exec", "-T", "client", 
        "sh", "-c", 
        f"echo Q | openssl s_client -connect server:4433 -curves {algo} -trace -nocommands 2>&1"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, encoding='utf-8', errors='ignore')
        return result.stdout
    except Exception as e:
        print(f"Error running docker command for {algo}: {e}")
        return None

def parse_key_lengths(trace_output):
    """
    Parses the openssl trace output to find key_share lengths.
    Returns (client_len, server_len)
    """
    if not trace_output:
        return None, None
        
    # Look for key_exchange entries
    # Pattern: key_exchange:.*\(len=(\d+)\)
    # We expect the first one to be ClientHello (Public Key / Key Share)
    # The second one to be ServerHello (Ciphertext / Key Share)
    
    matches = re.findall(r'key_exchange:\s*\(len=(\d+)\)', trace_output)
    
    if len(matches) >= 2:
        return int(matches[0]), int(matches[1])
    elif len(matches) == 1:
        return int(matches[0]), "?"
    else:
        return None, None

def main():
    print(f"{'Algorithm':<20} | {'Client Share (PK)':<20} | {'Server Share (CT)':<20}")
    print("-" * 66)
    
    for algo in ALGORITHMS:
        sys.stdout.write(f"Probing {algo}...")
        sys.stdout.flush()
        
        output = run_openssl_trace(algo)
        client_len, server_len = parse_key_lengths(output)
        
        # Clear the "Probing..." line
        sys.stdout.write("\r" + " " * 40 + "\r")
        
        c_str = f"{client_len} bytes" if client_len else "Failed to parse"
        s_str = f"{server_len} bytes" if server_len else "Failed to parse"
        
        print(f"{algo:<20} | {c_str:<20} | {s_str:<20}")

if __name__ == "__main__":
    main()
