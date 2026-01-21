# OpenSSL

## Überblick:
- Robuste, vollumfängliche Implementierung der TLS- und SSL-Protokolle
- Open-Source
- Basis für Webserver (Apache, Nginx), VPNs und die meisten Linux-Distributionen

## Kern-Komponenten:

1. libssl:
    - Implementiert die Protokollschicht: TLS State Machine, Handshake-Logik, Record Layer

2. libcrypto:
    - Allgemeine Kryptografie-Bibliothek
    - Stellt die mathematischen Algorithmen bereit (AES, SHA, RSA, ECDH)
    - Kryptografie-Bibliothek, stellt verschieden Algorithmen bereit (AES, SHA, RSA, ECDH)

## Funktionalität:
- Command Line Interface
- bietet Werkezeuge für:
    - Schlüsselmanagement (PKI)
    - Zertifikatserstellung (X.509)
    - Protokoll-Debugging


## Ressources
- https://openssl-library.org/
- https://github.com/openssl/openssl