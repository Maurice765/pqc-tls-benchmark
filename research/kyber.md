# Kyber (ML-KEM)

## Overview
Kyber ist ein KEM (Key Encapsulation Mechanism), kein klassischer Key Exchange (wie Diffie-Hellman), obwohl das Ergebnis dasselbe ist: Ein geteiltes Geheimnis.
Seit 2024 ist es standardisiert als **ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism).

## Mathematical Foundation: Module-LWE
Kyber basiert nicht auf dem "einfachen" LWE (Matrix/Vektor mit Zahlen), sondern auf **Module-LWE**.
*   **Ring/Module**: Statt mit einzelnen Zahlen ($Z_q$) rechnet man mit Polynomen ($R_q$).
*   **Warum?** Effizienz. Man kann mit einer Polynom-Multiplikation viele "Zahlen" gleichzeitig verarbeiten. Kleinere Schlüsselgrößen als klassisches LWE.

## KEM vs. Diffie-Hellman (ECDH)

### Der Unterschied im Ablauf
Obwohl beide Verfahren am Ende einen geheimen Schlüssel für TLS bereitstellen, ist der Weg dorthin unterschiedlich:

| Eigenschaft | Diffie-Hellman (ECDH) | Kyber (KEM) |
| :--- | :--- | :--- |
| **Prinzip** | "Mischen": Beide steuern ihren Teil bei und das Ergebnis entsteht mathematisch aus beiden Teilen. | "Verschließen": Einer wählt das Geheimnis und schickt es verschlüsselt ("gekapselt") zum anderen. |
| **Mathematik** | $K = (g^a)^b = (g^b)^a$ (Kommutativ) | $c = \text{Enc}(pk, \text{random\_seed})$, $K = \text{KDF}(\text{seed})$ |
| **Vergleichbarkeit** | **Ja, absolut.** Im TLS-Handshake ersetzen sie denselben Schritt ("Key Exchange"). Man kann Latenz (Zeit) und Overhead (Größe der Pakete) direkt vergleichen. |

### The Procedure (KEM Detail)
1.  **KeyGen (Server):** Erzeugt Public Key ($pk$) und Secret Key ($sk$).
2.  **Encaps (Client):** 
    *   Nutzt $pk$.
    *   Wählt ein zufälliges Geheimnis $m$ (Seed).
    *   Verschlüsselt $m$ zu einem Chiffretext $c$ ("Kapsel").
    *   Leitet aus $m$ den Shared Secret $K$ ab.
    *   Sendet $c$ an den Server.
3.  **Decaps (Server):**
    *   Nutzt $sk$ und $c$.
    *   Entschlüsselt $m$ aus $c$ (mit Fehlerkorrektur, LWE Rauschen entfernen).
    *   Leitet denselben Shared Secret $K$ ab.

## Hybrid-Verfahren (X25519Kyber768)

Das ist aktuell der "Goldstandard" für die Übergangszeit (genutzt von Google Chrome, Cloudflare, Apple iMessage).

### Theorie (Sehr einfach!)
Es ist kein neuer mathematischer Algorithmus, sondern eine **Kombination**.
1.  Der Client und Server führen **beide** Verfahren durch: Einen klassischen ECDH (X25519) und einen Kyber-KEM.
2.  Man erhält zwei Teilschlüssel: $K_{klassisch}$ und $K_{pq}$.
3.  Der finale Schlüssel ist eine Kombination (z.B. Hash) aus beiden:
    $$ K_{final} = \text{Hash}( K_{klassisch} \ || \ K_{pq} ) $$

### Warum ist das wichtig?
*   **Sicherheit:** Falls Kyber doch eine Schwachstelle hat (der Algorithmus ist noch relativ jung), schützt immer noch der klassische ECC-Teil. Man verliert also nichts an Sicherheit, gewinnt aber Schutz gegen Quantencomputer (falls Kyber sicher ist).
*   **Theorie-Aufwand:** Minimal. Du musst nur erklären, dass beide Werte berechnet und konkateniert (aneinandergehängt) werden. Keine neue Mathematik nötig.

## Parameters (Kyber-768)
*   Sicherheitslevel: Äquivalent zu AES-192 (NIST Level 3).
*   Dimension $k=3$ (Vektoren der Länge 3 über dem Polynomring).

## Resources
*   [Kyber Spec](https://pq-crystals.org/kyber/)
