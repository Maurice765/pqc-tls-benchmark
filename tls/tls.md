# Einleitung
- 2018 in RFC 8446 finalisiert (IETF TLS Working Group)
- Basiert auf TLS 1.2, entfernt Veraltete Verfahren (kein SHA-1, kein RSA-Key-Exchange ohne Forward Secrecy)
- Einführung des 1-RTT Handshake (Verbindung steht nach nur einer Runde)
    - PQC-Schlüssel sind groß -> effizienter Handshake umso wichtiger, um Latenz zu kompensieren



# Vergleich Handshake TLS 1.2 vs TLS 1.3

![image](/tls/images/tls-1.2-1.3-handshake.webp)


# TLS 1.3 Handshake

1. Key Exchance:

    - Ziel: Einigung auf gemeinsame kryptografische Parameter und Erzeugung eines Shared Secrets

    - Client Hello: 
        - sendet "Random" (Zufallszahl) und Liste der unterstützten Cipher Suites
        - enthält Extension key_share mit dem öffentlichen Schlüssel

    - Server Hello:
        - wählt Algorithmus aus
        - sendet seinen Teil des key_share zurück

    - beide Seiten besitzen jetzt Handshake Key, alles folgende ist verschlüsselt

2. Server Parameters:
    - Ziel: Konfiguration der Verbindungsumgebung

    - Encrypted Extensions:
        - Beinhaltet Parameter, die keine eigenen Nachrichten benötigen

    - CertificateRequest (optional):
        - nur bei zertifikatsbasierter Client-Authentifizierung
        - enthält gewünschte Zertifikat Parameter

3. Authentication:
    - Ziel: Sicherstellen, dass wir mit dem richtigen Server sprechen.

    - Certificate:
        - Server sendet seine Zertifikatskette (X.509)

    - Certificate Verify:
        - digitale Signatur über den bisherigen Handshake-Verlauf
        - beweist, dass der Server den Private Key zum Zertifikat besitzt

    - Finished:
        - MAC (Message Authentication Code) über den gesamten Handshake

4. Application Data:
    - Sicherer Kanal ist etabliert
    - Datenfluss (HTTP Traffic) beginnt

![image](/tls/images/tls13handshake.png)

## Resources
* https://datatracker.ietf.org/doc/html/rfc8446
* https://www.ietf.org/blog/tls13/
* https://www.ibm.com/docs/en/sdk-java-technology/8?topic=works-tls-13-handshake