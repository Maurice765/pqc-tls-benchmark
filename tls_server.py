import socket
import ssl

def run_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    # Force TLS 1.3 and ECDHE if possible (Python 3.7+ defaults to TLS 1.3 support)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    
    # Bind to localhost on a random port or fixed port. Let's use 4433.
    bind_addr = '127.0.0.1'
    bind_port = 4433
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((bind_addr, bind_port))
        sock.listen(5)
        # print(f"Server listening on {bind_addr}:{bind_port}")
        
        while True:
            try:
                conn, addr = sock.accept()
                with context.wrap_socket(conn, server_side=True) as ssock:
                    # Just complete the handshake and close
                    # print(f"Accepted connection from {addr}")
                    pass
            except Exception as e:
                # print(f"Server error: {e}")
                pass
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    run_server()
