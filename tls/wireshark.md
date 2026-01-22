# Wireshark

## Handshake mit test.openquantumsafe.org

Verwendung des OQS-OpenSSL Docker-Containers:
```
docker run -it --rm openquantumsafe/oqs-ossl3 openssl s_client -connect test.openquantumsafe.org:6012 -groups mlkem1024 -tls1_3
```

## Overview
![image](images/wireshark_1.png)

- Transport Layer: Standardkonformer TCP 3-Way-Handshake (Pakete 217–220)

- Protokoll: TLS 1.3 mit effizientem 1-RTT

## ClientHello
![image](images/wireshark_client.png)

- Key Share Extension: Initiierung des Schlüsselaustauschs mittels KEM (Key Encapsulation Mechanism)

- Algorithmus: Spezifikation von ML-KEM-1024

- Key Share Extension: Hier findet der eigentliche Schlüsselaustausch statt

- Datenmenge: Public Key ist 1568 Bytes groß
    - Klassische Elliptische Kurven (ECC) brauchen nur ca. 32 Bytes



## ServerHello
![image](images/wireshark_server.png)

- Cipher Suite: Auswahl von TLS_AES_256_GCM_SHA384 für symmetrische Nutzdaten-Verschlüsselung

- Key Encapsulation: Server bestätigt ML-KEM-1024 und sendet 1568 Bytes Ciphertext zurück

- Handshake: Post-Quanten-Sicherheit durch ML-KEM

- Record Layer: Klassische Sicherheit durch AES-256


## Ressources:

- https://test.openquantumsafe.org/