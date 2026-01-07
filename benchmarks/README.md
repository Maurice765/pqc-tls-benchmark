# Post-Quanten-Kryptographie Benchmarking (Kyber vs ECDHE)

Dieses Projekt vergleicht die Leistung von Post-Quanten-Kryptographie (PQC) Key Encapsulation Mechanisms (speziell ML-KEM/Kyber) mit traditionellem Elliptic Curve Diffie-Hellman (ECDHE) und hybriden Kombinationen.

Es verwendet **Open Quantum Safe (OQS)** Docker-Images, um eine Client-Server-TLS-Handshake- und Datenübertragungsumgebung zu simulieren.

## Überblick

Der Benchmark misst:
1.  **Handshake-Zeit**: Die Zeit, die benötigt wird, um eine TLS-Verbindung unter Verwendung verschiedener Schlüsselaustauschgruppen herzustellen.
2.  **Übertragungszeit**: Die Zeit, die benötigt wird, um nach dem Handshake eine 10MB große Datei herunterzuladen.

Variablen:
-   **Algorithmen**:
    -   **Quantenresistent**: `mlkem512`, `mlkem768`, `mlkem1024`
    -   **Klassisch**: `P-256`, `P-384`, `P-521`
    -   **Hybrid**: `p256_mlkem512`, `p384_mlkem768`, `p521_mlkem1024`
-   **Netzwerklatenz**: Simuliert mit `tc` (Traffic Control) innerhalb des Client-Containers (0ms, 50ms).

## Voraussetzungen

-   **Docker** und **Docker Compose**
-   **Python 3**
-   Python-Abhängigkeiten:
    -   `matplotlib`
    -   `numpy`

## Einrichtung & Nutzung

1.  **Starten der Docker-Container**:
    Stellen Sie sicher, dass Docker läuft, und starten Sie dann die Umgebung:
    ```bash
    docker compose up -d
    ```

2.  **Installieren der Python-Abhängigkeiten**:
    ```bash
    pip install matplotlib numpy
    ```

3.  **Ausführen des Benchmarks**:
    Führen Sie das Python-Skript aus, um den Benchmarking-Prozess zu starten. Dieses Skript interagiert mit den laufenden Docker-Containern.
    ```bash
    python benchmark.py
    ```

    *Hinweis: Das Skript erstellt eine 10MB Testdatei, setzt Netzwerklatenzen, führt curl-Befehle über `docker exec` aus und sammelt die Ergebnisse.*

## Ausgabe

Nach der Ausführung sind folgende Dateien für die Ausgaben verantwortlich:
-   `results.json`: Rohdaten mit Zeitmessungen für alle Iterationen/Algorithmen.
-   `benchmark_plot.png`: Balkendiagramm zur Visualisierung der durchschnittlichen Handshake- und Übertragungszeiten.
-   `benchmark_boxplot.png`: Detaillierte Boxplots, die die Verteilung der Zeitmessungen zeigen.

## Dateistruktur

-   `benchmark.py`: Haupt-Skript zur Orchestrierung.
-   `docker-compose.yml`: Definiert die `server` (OQS-Nginx) und `client` (OQS-Curl) Dienste.
-   `Dockerfile.client`: Benutzerdefiniertes Client-Image basierend auf `openquantumsafe/curl`, ergänzt um `iproute2` zur Latenzsimulation.
-   `nginx.conf`: Konfiguration für den Nginx-Server.
