# PQC-TLS-Benchmark: Analyse & Ergebnisse

## 1. Warum Benchmarks?
*   **Problemstellung**: PQC-Schlüssel (z.B. ML-KEM/Kyber) sind viel größer als klassische Schlüssel (ECC).
*   **Fragestellung**: Führt die Größe zu spürbaren Verzögerungen im TLS-Handshake?
*   **Ziel**: Empirischer Vergleich unter realen Bedingungen.
    *   **Klassisch**: ECDH
    *   **Post-Quanten**: ML-KEM
    *   **Hybrid**: ECDH + ML-KEM (Klassische Sicherheit + Quanten-Sicherheit)
*   **Fokus**: Nicht nur CPU-Last, sondern Netzwerk-Verhalten (Latenz & Paketverlust).

## 2. Setup Files
Das `benchmarks`-Verzeichnis enthält eine isolierte Testumgebung.

*   **`docker-compose.yml`**
    *   Startet zwei Container: `server` (Nginx) und `client`.
    *   Definiert internes Netzwerk `oqs_net` (Isolierung von Störfaktoren).
*   **`nginx.conf`**
    *   Konfiguration für den OQS-Nginx-Server.
    *   Aktiviert **TLS 1.3**.
    *   Definiert Krypto-Gruppen (`ssl_ecdh_curve`): `mlkem512`, `p256_mlkem512`, etc.
*   **`Dockerfile.client`**
    *   Baut Client-Image auf Basis von `openquantumsafe/curl`.
    *   **Wichtig**: Installiert `iproute2` für `tc` (Traffic Control).
    *   Zweck: Simulation von schlechten Netzwerkbedingungen.

## 3. Erklärung `benchmark.py`
Zentrales Skript zur Steuerung der Messungen.

*   **Ablauf**:
    1.  Erstellt 10MB Testdatei auf dem Server.
    2.  Iteriert durch Szenarien:
        *   **Latenz**: 0ms, 50ms, 100ms.
        *   **Packet Loss**: 0%, 5%, 20%.
    3.  Manipuliert Netzwerk im Client-Container mittels `tc` (Traffic Control).
    4.  Führt `curl` Messungen durch.
*   **Gemessene Metriken**:
    *   **Handshake-Zeit (`time_appconnect`)**: Zeit bis der sichere Tunnel steht (Client Hello -> Finished).
    *   **Transfer-Zeit**: Zeit für Download der 10MB Datei (nach Handshake).
*   **Output**:
    *   Speichert Rohdaten in `results.json`.
    *   Generiert Plots (`benchmark_plot.png`, Boxplots).

## 4. Ergebnisse & Auswertung

### A. Latenz (Ping) - Detailanalyse
*   **0ms (Reine Rechenleistung)**:
    *   **Warum ist ML-KEM schnell?** ML-KEM basiert auf Gitter-Mathematik (Matrix-Vektor-Multiplikation). Das ist für CPUs effizienter zu berechnen als die komplexe Skalarmultiplikation auf Elliptischen Kurven (ECDHE).
    *   **Ergebnis**: Trotz größerer Schlüssel ist die *Berechnung* von Kyber oft schneller als P-256.
    *   **Hybrid**: Hier addieren sich die Zeiten (~35ms Kyber + ~35ms ECC = ~70ms), aber es bleibt im Millisekunden-Bereich.
*   **50ms / 100ms (Netzwerk-Dominanz)**:
    *   **Der "Equalizer"**: Ein Handshake benötigt 1 Round-Trip (Hin- und Rückweg).
    *   **Rechnung**: Bei 50ms Ping wartet man garantiert 50ms auf das Netzwerk. Ob die Berechnung 3ms oder 10ms dauert, ist für den Nutzer nicht spürbar.
    *   **Bandbreite**: Ob 1KB (Kyber) oder 65 Byte (ECC) übertragen werden, dauert bei heutigen Geschwindigkeiten (z.B. 100 Mbit/s) nur Mikrosekunden Unterschied.

### B. Packet Loss (Paketverlust) - Warum PQC leidet
*   **MTU-Grenze (1500 Bytes)**:
    *   **Klassisch (P-256)**: Public Key (~65B) + Header passt bequem in **1 Paket**. Wahrscheinlichkeit für Verlust = $p$.
    *   **PQC (ML-KEM-1024)**: Public Key (~1568B) + Header > 1500B. Muss in **2 Pakete** zerteilt werden.
*   **Die Mathematik**:
    *   Damit der Handshake klappt, müssen *beide* Fragmente ankommen.
    *   Verlustwahrscheinlichkeit steigt: Das Gesamtrisiko ist höher als bei einem einzelnen Paket.
    *   **Folge**: TCP muss verlorene Fragmente neu senden (Retransmission). Das kostet Zeit (mindestens 1x RTT extra). Daher die "Ausreißer" in den Messungen bei Kyber.
    *   **Levels**: Level 5 (größere Keys) ist hier anfälliger als Level 1.

### C. Datentransfer (10MB) - Warum alles gleich ist
*   **Entkopplung**: Der *Handshake* dient nur dazu, sich auf ein gemeinsames Geheimnis zu einigen.
*   **Symmetrische Phase**: Sobald das Geheimnis da ist, wechseln beide Seiten auf symmetrische Verschlüsselung (z.B. **AES-256-GCM** oder **ChaCha20**).
*   **Hardware-Support**: Moderne CPUs haben Hardware-Beschleunigung für AES (AES-NI).
*   **Ergebnis**: Egal ob das Geheimnis via Kyber oder ECC ausgetauscht wurde – die AES-Verschlüsselung der 10MB Datei läuft immer gleich schnell. Der Flaschenhals ist hier nur die Bandbreite.

### D. Vergleich der Sicherheits-Level (Level 1 vs. 5)
*   **Handshake**:
    *   **PQC pur**: Der Unterschied zwischen ML-KEM-512 (Level 1) und ML-KEM-1024 (Level 5) ist in der reinen Berechnung fast nicht messbar (Gitter-Operationen skalieren sehr gut).
    *   **Hybrid**: Hier entstehen messbare Unterschiede vor allem durch den *klassischen* Partner. P-521 (genutzt für Level 5) ist rechnerisch aufwändiger als P-256 (Level 1). Daher sind Level-5-Hybride etwas langsamer als Level-1-Hybride.
*   **Transfer**:
    *   **Kein Unterschied**: Ein ausgehandelter symmetrischer Schlüssel (z.B. 256 Bit) ist immer gleich groß und gleich schnell, egal ob er ursprünglich mit Level 1 (niedrig) oder Level 5 (hoch) geschützt wurde.

## 5. Fazit
*   **Performance**: PQC (ML-KEM) ist performant und praxistauglich.
*   **Flaschenhals**: In realen Netzen ist fast immer die Latenz (Ping) der limitierende Faktor, nicht die Kryptographie.
*   **Empfehlung**: **Hybride Verfahren** nutzen.
    *   Minimaler Performance-Verlust.
    *   Maximale Sicherheit (Gegenwart + Zukunft).
    *   Stabilität auch bei moderatem Packet Loss gegeben.
