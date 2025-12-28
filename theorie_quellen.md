# Theoretische Grundlagen & Quellen (PQC TLS Benchmark)

## 1. Elliptic Curve Cryptography
* **Cloudflare Blog:** [A Relatively Easy-To-Understand Guide to Elliptic Curve Cryptography](https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/) (Einstieg in ECC, wird noch in VL behandelt)
* [Funny Measurements](https://eprint.iacr.org/2013/635.pdf)

## 2. Quantencomputer & Die Bedrohung
* **Shor, I'll do it (Blog):** [Scott Aaronson: Shor's algorithm for everyone](https://www.scottaaronson.com/blog/?p=208)
* **Shors Algorithmus (Visuell):** [MinutePhysics: How Shor's Algorithm- Factors 15](https://www.youtube.com/watch?v=lvTqbM5Dq4Q)
* **Shor's Algorithm (Technisch):** [Qiskit Textbook: Shor's Algorithm](https://learn.qiskit.org/course/ch-algorithms/shors-algorithm)

## 3. Gitterbasierte Kryptographie 
* **Learning with Errors (LWE):** [Learning with Errors](https://www.youtube.com/watch?v=K026C5YaB3A) (2 Videos davor auch super)
* **Lattice Cryptography:** https://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf oder https://eprint.iacr.org/2015/938.pdf

## 4. Kyber / ML-KEM
* **Offizielles Paper:** [CRYSTALS-Kyber: a lattice-based KEM](https://pq-crystals.org/kyber/resources.shtml) (Algorithmus-Spezifikation und Performance-Daten)
* **NIST Standard:** [FIPS 203 (ML-KEM)](https://csrc.nist.gov/pubs/fips/203/final) (finale Standard vom August 2024)

## 5. PQC in der Praxis
* **IETF Draft:** [Hybrid key exchange in TLS 1.3](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/) (Wie PQC technisch in das Protokoll integriert wird), Google (X25519 + Kyber-768, https://pq.cloudflareresearch.com/) 
