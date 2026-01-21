# Open Quantum Safe (OQS)

## Überblick:

- Forschungsprojekt gegründet 2014
- Open Source (MIT License)
- Ziel: Unterstützung des Übergangs zu quantensicherer Kryptografie
- Teil der Linux Foundation Post-Quantum Cryptography Alliance

## Kern-Komponenten:

1. liboqs:
    - C-Bibliothek, welche die mathematischen Algorithmen implementiert
    - Bietet einheitliche Schnittstelle für alle Algorithmen
    - Algorithmen:
        - KEMs (Key Encapsulation): Für den Schlüsselaustausch (z.B. ML-KEM/Kyber, FrodoKEM, Bikel)
        - Signaturen: Für Authentifizierung (z.B. ML-DSA/Dilithium, Falcon/FN-DSA)
        - sowie hybride Verfahren
    - Implementiert Neutral sowohl NIST-Finalisten (FIPS Standards) als auch Round-4-Kandidaten
    - Language Wrapper verfügbar für z.B. Python, Java, Go, ...

2. Integrationen:
    - Prototype Integrationen in Protokolle und Bibliotheken
    - OpenSSL 3 Provider, OpenSSH, ...

## OQS Provider für OpenSSL 3:

- nutzt modulare Provider-Architektur von OpenSSL 3
- kann als dynamisches Modul in OpenSSL verwendet werden
- macht PQC-Algorithmen für Anwendungen (nginx, curl, Apache) verfügbar

## Relevanz für unser Projekt:

- Basis für Benchmark: openquantumsafe/nginx Docker Image für Performance Messungen
- zeigt das TLS 1.3 bereits heute PQC fähig ist (via Key Share Extension)


## Ressources
- https://openquantumsafe.org/
- https://github.com/open-quantum-safe