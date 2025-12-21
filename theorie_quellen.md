# Theoretische Grundlagen & Quellen (PQC TLS Benchmark)

## 1. Elliptic Curve Cryptography
* **Cloudflare Blog:** [A Relatively Easy-To-Understand Guide to Elliptic Curve Cryptography](https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/) (Hervorragender Einstieg in ECC)
* **Standard:** [RFC 7748](https://tools.ietf.org/html/rfc7748) – Elliptic Curves for Security (X25519)

## 2. Quantencomputer
* **Shors Algorithmus:** [Shors Algorithmus](https://www.spinquanta.com/news-detail/shors-algorithm) 
* **NIST PQC:** [Post-Quantum Cryptography FAQ](https://csrc.nist.gov/Projects/post-quantum-cryptography/faqs) (Offizielle Sicht der Standardisierungs-Behörde)

## 3. Gitterbasierte Kryptographie 
* **Learning with Errors (LWE):** [Learning with Errors](https://www.youtube.com/watch?v=K026C5YaB3A) (2 Videos davor auch super)
* **Lattice Cryptography:** https://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf oder https://eprint.iacr.org/2015/938.pdf

## 4. Kyber / ML-KEM
* **Offizielles Paper:** [CRYSTALS-Kyber: a lattice-based KEM](https://pq-crystals.org/kyber/resources.shtml) (Algorithmus-Spezifikation und Performance-Daten)
* **NIST Standard:** [FIPS 203 (ML-KEM)](https://csrc.nist.gov/pubs/fips/203/final) (finale Standard vom August 2024)

## 5. PQC in der Praxis
* **IETF Draft:** [Hybrid key exchange in TLS 1.3](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/) (Wie PQC technisch in das Protokoll integriert wird), Google (X25519 + Kyber-768, https://pq.cloudflareresearch.com/) 
