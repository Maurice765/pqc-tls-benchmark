import socket
import ssl
import time

def run_client_handshake():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    
    # ECDHE is standard in TLS 1.3, we can't easily force *only* ECDHE in high-level python ssl 
    # without complex cipher string manipulation, but default TLS 1.3 uses ECDHE.
    
    host = '127.0.0.1'
    port = 4433
    
    start_time = time.perf_counter()
    
    try:
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                # Handshake is done upon entering this block
                pass
        end_time = time.perf_counter()
        return (end_time - start_time) * 1000 # ms
    except Exception as e:
        # print(f"Client error: {e}")
        return None

if __name__ == "__main__":
    latency = run_client_handshake()
    if latency:
        print(f"Handshake latency: {latency:.4f} ms")
    else:
        print("Handshake failed")
