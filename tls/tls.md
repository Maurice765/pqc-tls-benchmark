# TLS 1.3

- Veröffentlicht im August 2018 durch die IETF in RFC 8446
- Definiert aktuellen Stand der Technik für sichere Kommunikation im Internet
- Grundlegende Überarbeitung von TLS 1.2
- Einführung des 1-RTT Handshake
- Integration von PQC (wie ML-KEM) erfordert die Übertragung signifikant größerer Schlüsseldaten
    -> Ein effizienter Handshake ist essenziell, um die zusätzliche Latenz der großen Keys zu kompensieren

# Vergleich Handshake TLS 1.2 vs TLS 1.3

![image](/tls/images/tls-1.2-1.3-handshake.webp)

- **Latenz:** 
    - Reduktion der Round Trip Time (RTT) durch proaktives Senden der key_share Extension im ClientHello

- **Sicherheit:**
    - Entfernung obsoleter kryptografischer Primitiven (z.B. statischer RSA-Key-Exchange, SHA-1)
    - Durchsetzung von Perfect Forward Secrecy (PFS) mittels Ephemeral Diffie-Hellman

- **Privacy:** 
    - Verschlüsselung von Metadaten (insb. Server-Zertifikate) zum Schutz vor passiver Netzwerkanalyse

# TLS 1.3 Handshake

![image](/tls/images/tls13handshake.png)

## 1. Key Exchange

- Ziel: Aushandlung der kryptografischen Parameter und Etablierung des Shared Secrets

- **ClientHello:**
    - Client initiiert den Handshake
    - Enthält: 
        - Zufällige Zahl (Random)
        - Sitzungs-ID (legacy_session_id)
        - Liste unterstützter Chiffren (cipher_suites)
    - TLS 1.3 Erweiterungen:
        - Supported Versions: Client gibt explizit an, dass er TLS 1.3 bevorzugt
        - Key Share: 
            - Client generiert proaktiv Schlüsselpaare für verschiedene Algorithmen (z.B. X25519 oder PQC-Kandidaten)
            - Sendet seine öffentlichen Schlüssel ("Key Shares") direkt mit
        - Signature Algorithms: Liste der Signaturverfahren, die Client zur Überprüfung von Zertifikaten unterstützt (z. B. ecdsa_secp256r1_sha256)
    

- **ServerHello:**
    - Server antwortet mit seiner gewählten Konfiguration
    - Wählt eine Cipher Suite und Protokollversion (TLS 1.3) aus dem Angebot des Clients aus
    - Key Share:
        - Wählt einen der angebotenen Schlüsselaustausch-Algorithmen des Clients
        - Generiert sein eigenes Schlüsselpaar und sendet seinen öffentlichen Teil zurück
    - Status: Schlüsselaustausch ist mathematisch abgeschlossen, beide Seiten können das gemeinsame Geheimnis berechnen


## 2. Server-Parameter
- Ziel: Austausch von Parametern für die Anwendungsebene

- **Encrypted Extensions:** 
    - Enthält Protokoll-Details wie ALPN (z. B. Einigung auf HTTP/2 oder HTTP/3)

- **CertificateRequest(Optional):** 
    - Wird nur gesendet, wenn Mutual TLS (mTLS) gewünscht ist(Server will Identität des Clients prüfen)

## 3. Authentifizierung
- Ziel: Authentifizierung des Servers (und optional des Clients) sowie Integritätsprüfung

### Server-Seite:

- **Certificate:** 
    - Server sendet Zertifikatskette (X.509) als Identitätsnachweis
    - Im Gegensatz zu TLS 1.2 ist das Zertifikat hier verschlüsselt

- **Certificate Verify:** 
    - Server erstellt digitale Signatur über den Hash aller bisherigen Handshake-Nachrichten
    - Beweist den Besitz des zum Zertifikat gehörenden Private Keys
    - Client verifiziert diese Signatur mit dem öffentlichen Schlüssel aus dem Zertifikat

- **Finished:** 
    - Abschluss des Server-Handshakes
    - Enthält einen HMAC (Hash-based Message Authentication Code) über das gesamte Transkript
    - Stellt sicher, dass niemand den Handshake manipuliert hat

### Client:

- **Certificate(Optional):** 
    - Client sendet eigenes Zertifikat (nur bei CertificateRequest)

- **Certificate Verify (Optional):** 
    - Client unterschreibt das Transkript (nur bei CertificateRequest)

- **Finished:**
    - Client sendet ebenfalls HMAC über das Transkript
    - Sobald der Server dies verifiziert, ist der Handshake komplett
    - Ergebnis: Sicherer Austausch von Application Data beginnt


## Resources
* https://datatracker.ietf.org/doc/html/rfc8446
* https://www.ietf.org/blog/tls13/
* https://www.ibm.com/docs/en/sdk-java-technology/8?topic=works-tls-13-handshake
* https://www.cloudflare.com/learning/ssl/why-use-tls-1.3/
* https://www.cloudflare.com/learning/ssl/what-happens-in-a-tls-handshake/