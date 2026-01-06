Das ist ein hervorragendes und hochaktuelles Thema. Da das NIST (National Institute of Standards and Technology) im August 2024 die ersten PQC-Standards (wie ML-KEM/Kyber und ML-DSA/Dilithium) finalisiert hat, ist euer Projekt am Puls der Zeit.

### Phase 1: Die richtige Werkzeugwahl (Nicht alles selbst programmieren!)

Versucht auf keinen Fall, den TLS-Stack oder die PQC-Algorithmen von Grund auf neu zu schreiben. Das sprengt den Rahmen eines Moduls. Nutzt etablierte Forks.

**Das Tool der Wahl: Open Quantum Safe (OQS)**
Das *Open Quantum Safe Project* (liboqs) bietet einen Fork von OpenSSL, der bereits PQC-Algorithmen integriert hat. Das ist der Industriestandard für Forschung in diesem Bereich.

* **Vorteil:** Ihr könnt verschiedene Algorithmen (Kyber, Dilithium, Falcon etc.) einfach per Konfiguration austauschen, ohne den C-Code ändern zu müssen.
* **Alternative:** *WolfSSL* (falls ihr eher in Richtung Embedded Systems gehen wollt), aber OQS ist für reine Performance-Tests auf PCs/Servern zugänglicher.

---

### Phase 2: Definition des Szenarios (Scope)

Ihr müsst entscheiden, *was* genau ihr im TLS Handshake austauschen wollt. Ein TLS 1.3 Handshake besteht grob aus zwei kryptographischen Teilen, die durch PQC ersetzt werden können:

1.  **Key Encapsulation Mechanism (KEM):** Der Schlüsselaustausch (ersetzt ECDH).
    * *Algorithmus:* **ML-KEM (Kyber)**.
    * *Schwierigkeit:* Mittel.
    * *Empfehlung:* **Macht das auf jeden Fall.** Das ist der wichtigste Teil für "Forward Secrecy" gegen Quantencomputer.
2.  **Authentication (Signaturen):** Die Zertifikate.
    * *Algorithmus:* **ML-DSA (Dilithium)** oder **Falcon**.
    * *Schwierigkeit:* Hoch (ihr müsst eine eigene PKI/CA aufsetzen und PQC-Zertifikate erstellen).
    * *Empfehlung:* Macht das nur, wenn Zeit bleibt. Konzentriert euch primär auf KEM oder "Hybrid KEM" (klassisch + PQC).



> **Tipp:** Vergleicht am besten **Hybrid-Verfahren** (z.B. X25519 + Kyber768) gegen **Klassisch** (X25519). Hybride Verfahren sind das, was Google (in Chrome) und Cloudflare aktuell bereits testen.

---

### Phase 3: Die Testumgebung aufbauen (Architektur)

Ihr braucht eine Umgebung, in der ihr Netzwerkbedingungen simulieren könnt. Wenn ihr Client und Server nur auf `localhost` (127.0.0.1) laufen lasst, werdet ihr kaum Unterschiede bemerken, da die Latenz praktisch null ist. PQC-Algorithmen haben oft größere Schlüssel, was bei langsamen Netzwerken stark ins Gewicht fällt.

**Vorschlag für das Setup (Docker):**

1.  **Container A (Server):** OQS-OpenSSL Server (z.B. `nginx` mit OQS-Patch).
2.  **Container B (Client):** OQS-OpenSSL Client (Kommandozeile oder `curl` mit OQS).
3.  **Netzwerk-Simulation:** Nutzt Tools wie `tc` (Traffic Control) unter Linux oder "Pumba" (für Docker), um künstliche Latenz (z.B. 50ms, 100ms) und Packet Loss hinzuzufügen.

---

### Phase 4: Messgrößen (Metriken)

Um den Performance-Vergleich wissenschaftlich fundiert zu gestalten, solltet ihr folgende Daten erheben:

1.  **Handshake Time (Latenz):**
    * Wie lange dauert es vom `ClientHello` bis zum `Finished`?
    * Messt dies für: Klassisch (ECDH), PQC (Kyber Level 1, 3, 5) und Hybrid.
2.  **Datenübertragung (Overhead):**
    * PQC-Schlüssel sind viel größer als ECC-Schlüssel.
    * Messt die Größe der `ClientHello` und `ServerHello` Pakete.
    * *Achtung:* Führt die Größe zur IP-Fragmentierung (wenn das Paket größer als die MTU von ca. 1500 Bytes ist)? Das kostet massiv Performance.
3.  **CPU-Last (Optional):**
    * Manche PQC-Algorithmen sind rechenintensiver, andere (wie Kyber) sind oft sogar schneller als klassische Elliptische Kurven, verlieren aber durch die große Datenmenge.

**Tools zum Messen:**
* **Wireshark:** Um die Pakete und Fragmentierung visuell zu bestätigen.
* `openssl s_time`: Ein eingebautes Tool für Performance-Tests.
* Python-Skripte: Um den Handshake 1000-mal laufen zu lassen und den Durchschnitt zu bilden.

---

### Phase 5: Der Vortrag (Storytelling)

Für den Master-Vortrag bietet sich folgende Gliederung an:

1.  **Motivation:** "Q-Day" (Wann brechen Quantencomputer RSA/ECC?). Warum müssen wir *jetzt* handeln (Store Now, Decrypt Later)?
2.  **Theorie (Kurz):** Ganz grob erklären, wie gitterbasierte Kryptographie (Lattice-based) funktioniert (z.B. Learning with Errors), ohne die Zuhörer mit Formeln zu erschlagen.
3.  **Versuchsaufbau:** Zeigt euer Docker-Setup und erklärt, warum ihr Netzwerk-Latenz simuliert habt (Realismus!).
4.  **Ergebnisse (Der Kern):**
    * Zeigt Grafiken: Balkendiagramme (Handshake-Dauer in ms).
    * Vergleich: *Standard TLS* vs. *Kyber-512* vs. *Kyber-1024*.
    * Diskussion: "Ist es langsam?" (Antwort ist meist: Kaum spürbar im Web, aber messbar).
5.  **Fazit:** PQC ist bereit für den Einsatz (NIST Standards sind da), der Overhead ist akzeptabel.

---

### Zusammenfassung der Aufgabenverteilung (Vorschlag)

* **Person A (Infrastruktur):** Aufsetzen der Docker-Container mit OQS-OpenSSL. Einrichten der Netzwerk-Drosselung (`tc` commands).
* **Person B (Messung & Skripte):** Schreiben der Python-Skripte, die den Handshake 1000x ausführen, Parsen der Logs, Erstellen der Graphen.
* **Person C (Theorie & Analyse):** Einarbeitung in Kyber/Dilithium für den Theorieteil, Analyse der Wireshark-Dumps (Fragmentierung prüfen), Vorbereitung der Folien.