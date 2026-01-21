# PQC-TLS-Benchmark: Struktur & Ergebnisse

Dieses Dokument beschreibt die Struktur des Benchmarking-Projekts und analysiert die erzielten Ergebnisse. Das Ziel ist der Vergleich von Post-Quanten-Kryptographie (Kyber/ML-KEM) mit klassischer Elliptic Curve Kryptographie (ECDHE) und hybriden Verfahren in einem TLS 1.3 Szenario.

## 1. Dateistruktur & Zweck

Das `benchmarks`-Verzeichnis enthält eine in sich geschlossene Umgebung zur Simulation und Messung.

### Infrastruktur & Konfiguration

*   **`docker-compose.yml`**
    *   **Zweck**: Definiert die Testumgebung bestehend aus zwei Diensten: `server` (Nginx) und `client` (Curl).
    *   **Warum**: Ermöglicht eine reproduzierbare, isolierte Netzwerkumgebung, die unabhängig vom Host-System ist.

*   **`Dockerfile.client`**
    *   **Zweck**: Bauanleitung für den Client-Container. Basiert auf `openquantumsafe/curl` und installiert zusätzlich `iproute2`.
    *   **Warum**: Das Standard-Image enthält keine Tools zur Netzwerkmanipulation. Wir benötigen `tc` (Traffic Control) aus `iproute2`, um künstliche Latenzen (Ping) zu simulieren und realistische WAN-Szenarien nachzustellen.

*   **`nginx.conf`**
    *   **Zweck**: Konfiguration des OQS-Nginx-Servers.
    *   **Warum**: Hier werden die entscheidenden Krypto-Parameter gesetzt.
        *   Aktivierung von **TLS 1.3**.
        *   Definition der erlaubten Kurven (`ssl_ecdh_curve`), inklusive reiner PQC-Algorithmen (`mlkem512` etc.) und Hybriden (`p256_mlkem512`).

### Benchmarking-Logik

*   **`benchmark.py`**
    *   **Zweck**: Das zentrale Steuerungsskript.
    *   **Funktion**:
        1.  Erstellt eine 10MB Testdatei auf dem Server.
        2.  Iteriert durch definierte Latenzen (0ms, 50ms, 100ms).
        3.  Manipuliert die Netzwerklatenz im Client-Container dynamisch mittels `tc`.
        4.  Führt `curl`-Messungen für verschiedene Algorithmen (Klassisch, PQC, Hybrid) durch.
        5.  Sammelt Ergebnisse und generiert Plots.
    *   **Warum**: Automatisiert den komplexen Testablauf und stellt sicher, dass alle Algorithmen unter identischen Bedingungen getestet werden.

*   **`get_key_lengths.py`**
    *   **Zweck**: Ein Analyse-Tool, das `openssl s_client -trace` nutzt.
    *   **Warum**: Dient zur Verifikation. Es liest die tatsächliche Größe der ausgetauschten "Key Shares" (Public Keys / Ciphertexts) aus dem TLS-Handshake aus, um sicherzustellen, dass wirklich die erwarteten PQC-Algorithmen verwendet werden.

### Ergebnisse & Output

*   **`results.json`**: Die rohen Messdaten. Dient als Datenbasis für Analysen und Plots.
*   **`benchmark_plot.png` / `benchmark_boxplot.png`**: Visualisierungen der Ergebnisse für schnelle Vergleiche.

ML


---

## 2. Analyse der Ergebnisse

Die Ergebnisse (basierend auf `results.json`) zeigen klare Trends beim Vergleich von klassischen und quantensicheren Verfahren.

### Beobachtungen

#### 1. Handshake-Zeiten (Verbindungsaufbau)

| Algorithmus (Beispiel) | 0ms Latenz | 50ms Latenz | 100ms Latenz |
| :--- | :--- | :--- | :--- |
| **P-256 (Klassisch)** | ~37ms | ~130ms | ~227ms |
| **ML-KEM-512 (PQC)** | ~34ms | ~130ms | ~229ms |
| **P-256 + ML-KEM-512 (Hybrid)** | ~50ms | ~144ms | ~242ms |

*   **Latenz-Dominanz**: Sobald Netzwerklatenz (50ms oder 100ms) hinzugefügt wird, dominiert die Round-Trip-Time (RTT) die Handshake-Dauer massiv. Der Unterschied zwischen den Algorithmen wird relativ gesehen sehr klein.
*   **Effizienz von ML-KEM**: ML-KEM (Kyber) ist rechnerisch extrem effizient. Bei 0ms Latenz (lokal) ist es oft sogar schneller oder gleichauf mit klassischen Elliptischen Kurven, obwohl die Schlüssel deutlich größer sind.
*   **Hybrid-Overhead**: Hybride Verfahren (z.B. `p256_mlkem512`) benötigen etwas mehr Zeit (~10-15ms mehr bei 0ms). Dies liegt an der doppelten Krypto-Operation und den größeren Datenpaketen, die übertragen werden müssen. Dieser Overhead fällt jedoch bei realen Netzwerklatenzen kaum noch ins Gewicht.

#### 2. Datentransfer (10MB Download)

| Szenario | Zeit (ca.) |
| :--- | :--- |
| 0ms Latenz | ~0.025s |
| 50ms Latenz | ~0.49s |
| 100ms Latenz | ~0.98s |

*   **Kein Einfluss des Algorithmus**: Der gewählte Schlüsselaustausch-Algorithmus hat **keinen** signifikanten Einfluss auf die Geschwindigkeit der eigentlichen Datenübertragung nach dem Handshake. Sobald der symmetrische Session-Key etabliert ist (AES/ChaCha20), ist die Geschwindigkeit identisch.
*   **Einfluss der Latenz**: Die Transferzeit steigt linear mit der Latenz, was auf das TCP-Verhalten (Window-Scaling, RTT) zurückzuführen ist, nicht auf die Kryptographie.

### Fazit & Begründung

1.  **Praktikabilität**: Post-Quanten-Kryptographie (speziell ML-KEM) ist heute schon absolut praxistauglich. Die befürchteten Performance-Einbußen durch größere Schlüssel bestätigen sich in modernen Netzwerken mit hoher Bandbreite nicht signifikant.
2.  **Hybrid ist der Weg**: Der minimale Performance-Verlust durch hybride Verfahren (Klassisch + PQC) ist ein sehr geringer Preis für die Sicherheit gegen "Harvest Now, Decrypt Later"-Angriffe. Man erhält die bewährte Sicherheit von ECC plus die Quantenresistenz von ML-KEM.
3.  **Netzwerk > Krypto**: In fast allen realistischen Szenarien (Internet, WAN) ist die Netzwerklatenz der limitierende Faktor, nicht die Rechenzeit für die PQC-Mathematik oder die Übertragung der etwas größeren Schlüssel.
