from kyber_py.kyber.default_parameters import Kyber768
import time

def measure_kyber_kem(kem_alg="Kyber768"):
    if kem_alg == "Kyber768":
        KEM = Kyber768
    else:
        print(f"Unsupported KEM: {kem_alg}")
        return None

    # 1. KeyGen (Server side)
    start_keygen = time.perf_counter()
    pk, sk = KEM.keygen()
    end_keygen = time.perf_counter()
    
    pk_size = len(pk)
    sk_size = len(sk)
    
    # 2. Encaps (Client side)
    start_encaps = time.perf_counter()
    ss_client, c = KEM.encaps(pk)
    end_encaps = time.perf_counter()
    
    ct_size = len(c)
    
    # 3. Decaps (Server side)
    start_decaps = time.perf_counter()
    ss_server = KEM.decaps(sk, c)
    end_decaps = time.perf_counter()
    
    # Verify shared secrets match
    if ss_client != ss_server:
        print("Shared secrets do not match!")
        return None
        
    total_time_ms = (end_encaps - start_encaps + end_decaps - start_decaps) * 1000
    
    return {
        "kem_alg": kem_alg,
        "pk_size": pk_size,
        "ct_size": ct_size,
        "latency_ms": total_time_ms
    }

if __name__ == "__main__":
    result = measure_kyber_kem()
    if result:
        print(f"Kyber768 Results: {result}")
