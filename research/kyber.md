# Kyber (ML-KEM)

## Overview
Kyber ist ein KEM (Key Encapsulation Mechanism), kein klassischer Key Exchange (wie Diffie-Hellman), obwohl das Ergebnis dasselbe ist: Ein geteiltes Geheimnis.
Seit 2024 ist es standardisiert als **ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism).

## Mathematical Foundation: 

### Ring-LWE

**Problem**: Die Matrix $A$ in LWE muss aus zufälligen Zahlen bestehen und damit sehr groß sein. Das führt zu mehr Rechenleistung und Speicherbedarf. 

**Lösung**: Statt Zahlen nutzt Ring-LWE Polynome in einem Ring $R_q = \mathbb{Z}_q[x] / (x^n + 1)$

Polynom: $$a(x) = a_0 + a_1x + a_2x^2 + \dots + a_{n-1}x^{n-1}$$
Beispiel:  $$3 + 5x + 2x^2$$
Vektor: $$(3, 5, 2)$$
Um die Polynome klein zu halten, wird in Ring-LWE mit Modulo $x^n + 1$ gerechnet (anti-zyklisch)

Beispiel: Vektor $(a_0, a_1, \dots, a_{n-1})$ wird mit $x$ multipliziert, $x \cdot a(x) = a_0x + a_1x^2 + \dots + a_{n-2}x^{n-1} + a_{n-1}x^n$. Der Ergebnisvektor ist $(-a_{n-1}, a_0, a_1, \dots, a_{n-2})$. Der letzte Wert rutscht nach vorne und ändert dabei sein Vorzeichen.

**Ideal**: Ein Ideal $I$ ist eine Teilmenge eines Rings $R$, mit folgenden 2 Bedingungen:
1. Wenn 2 Elemente aus einem Ideal addiert werden, muss das Ergebnis wieder im Ideal liegen
2. Wenn irgendein Element aus dem Ring $R$ mit einem Element aus dem Ideal $I$ multipliziert wird, muss das Ergebnis im Ideal liegen. 

Beispiel: Ring $R = \mathbb{Z}[x] / (x^n + 1)$, wobei $n=2$ ist

Das erzeugende Element ist $g(x) = 2 + 1x$, somit besteht das Ideal  $I = \langle g(x) \rangle$ aus einem Vielfachen aus $g(x)$

$$g(x) \cdot 1 = (2 + x) \cdot 1 = 2 + x$$
Als Vektorform: $(2, 1)$

$$g(x) \cdot x = (2 + x) \cdot x = 2x + x^2 \pmod{x^2 +1} = 2x - 1$$
Als Vektorform: $(-1, 2)$. Hier sieht man die antizyklische Verschiebung.

### Module-LWE (MLWE)
MLWE ersetzt die Polynome $a_1,a_2,...,a_n$ aus Ring-LWE mit Vektoren von Polynomen in $R^k_q$. Das Module ist damit $R^k_q$, welches aus k-langen Polynomial-Vektoren aus $R_q$ besteht.

$\text{MLWE}(m, k, q, B)$:
Sei $s \in_R R_q^k$ und $e \in_R S_B^m$ wobei $m > k$ und $B \ll q/2$.
Sei $a_1, a_2, \dots, a_m \in_R R_q^k$ und $b_i = a_i^T s + e_i \in R_q$ für $i = 1, \dots, m$.
Gegeben $a_i$ und $b_i$, finde $s$.

*   **Hinweis:** Jedes $a_i$ ist jetzt ein Vektor von Polynomen: $a_i = [a_{i1}, a_{i2}, \dots, a_{ik}]^T$.
*   Kyber basiert auf dem **Module-LWE** Problem, das eine Lösung $s \in R_q^k, e \in S_B^m$ für die Polynom-Matrix-Gleichung sucht:

$$
\begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1k} \\
a_{21} & a_{22} & \dots & a_{2k} \\
\vdots & \vdots & & \vdots \\
a_{m1} & a_{m2} & \dots & a_{mk}
\end{bmatrix}_{m \times k}
\cdot
\begin{bmatrix}
s_1 \\
s_2 \\
\vdots \\
s_k
\end{bmatrix}_{k \times 1}
+
\begin{bmatrix}
e_1 \\
e_2 \\
\vdots \\
e_m
\end{bmatrix}_{m \times 1}
=
\begin{bmatrix}
b_1 \\
b_2 \\
\vdots \\
b_m
\end{bmatrix}_{m \times 1}
$$

**Module**
*   **$k=1$** erzeugt ein Ring-LWE --> effizient, aber Sicherheit nicht fein skalierbar
*   **$n=1$** erzeugt ein LWE --> sehr sicher, aber riesige Schlüssel
*   **Module-LWE** nutzt feste Parameter $q$ und $n$ ($n=256$) und skaliert die Sicherheit über die Dimension $k$ ($k=2$ für leicht, $k=3$ für mittel, $k=4$ für hoch). Dadurch kann im jeweiligen Modul die Arithmetik optimiert werden

### Kyber-PKE

**Schlüssel Generierung - Alice:**

**Parameter:**
*   $q = 3329$
*   $n = 256$ (Polynomgrad)
*   $R_q = \mathbb{Z}_{3329}[x] / (x^{256} + 1)$
*   $k \in \{2, 3, 4\}$ (Dimension)
*   $(\eta_1, \eta_2) \in \{(3,2),(2,2),(2,2)\}$: Parameter für die Fehlerverteilung

1.  Wähle $s \in_R S_{\eta_1}^k$ (Geheimes Polynom)
2.  Wähle $A \in_R R_q^{k \times k}$ (Öffentliche Matrix, quadratisch wegen ss-MLWE)
3.  Wähle $e \in_R S_{\eta_1}^k$ (Fehler, klein)
4.  Berechne $b = As + e$
5.  **Public Key:** $(A, b)$. **Private Key:** $s$

**Sicherheit:**
*   $s$ aus $(A, b)$ zu berechnen $\rightarrow$ **ss-MLWE** (Search Problem)
*   Informationen über $s$ aus $(A, b)$ zu unterscheiden $\rightarrow$ **ss-DMLWE** (Decision Problem)

**Verschlüsselung - Bob:**
Verschlüsseln einer Nachricht $m \in \{0,1\}^{256}$ für Alice:

1.  Hole Alice's Encryption Key $(A, b)$.
2.  Wähle $r \in_R S_{\eta_1}^k, z \in_R S_{\eta_2}^k$ und $z' \in_R S_{\eta_2}$.
3.  Berechne $c_1 = A^T r + z$
    und $c_2 = b^T r + z' + \lceil q/2 \rceil m$.
4.  Output $c = (c_1, c_2)$.

**Entschlüsselung - Alice:**
Um $c = (c_1, c_2)$ zu entschlüsseln:

1.  Berechne $m' = \text{Round}_q(c_2 - s^T c_1)$.

## Kyber - Optimizations

Im Standard ML-KEM-768 die Parameter sind $q =3329, n = 256, k = 3, \eta_1 = 2, \eta_2 = 2$. Die Länge eines Integers beträgt damit $\lceil log_2 3329 \rceil$ = 12 bits.

Der Encryption Key $(A, b)$ hat die Größe $(9 \times 256 \times 12) + (3 \times 256 \times 12)$ bits = 4608 bytes (ECDH hat 48 bytes)

Der Ciphertext $c = (c_1,c_2)$ hat die Größe $(3 \times 256 \times 12) + (256 \times 12)$ bits = 1536 bytes

Der Encryption Key kann durch Hashing reduziert werden. Dabei wird $A$ durch ein zufälliges 256-bit seed $\rho$ generiert. 
1. Zuerst wird ein $\rho \in_R \{0,1\}^{256}$ ausgewählt
2. Dann werden die Koeffizienten des Polynomials durch das hashen von $\rho$ + einem Zähler generiert
3. Der Encryption Key ist statt $(A,b)$ jetzt $(\rho, b)$
4. Der Encryption Key ist jetzt $256 + (3 \times 256 \times 12)$ bits = 1184 bytes

### Compression und Decompression

Um die Schlüssel- und Ciphertext-Größen weiter zu reduzieren, verwendet Kyber verlustbehaftete Kompression. Die Idee: Statt alle 12 Bits pro Koeffizient zu speichern, werden nur die wichtigsten $d$ Bits behalten.

**Compress (Zahl):**
$$\text{Compress}_q(x, d) = \lceil (2^d / q) \cdot x \rfloor \mod 2^d$$

**Decompress (Zahl):**
$$\text{Decompress}_q(x, d) = \lceil (q / 2^d) \cdot x \rfloor$$

**Beispiel (Zahl):** Sei $q = 3329$, $d = 4$, und $x = 1000$.

*Kompression:*
$$\text{Compress}_{3329}(1000, 4) = \lceil (16 / 3329) \cdot 1000 \rfloor = \lceil 4.805 \rfloor = 5$$

*Dekompression:*
$$\text{Decompress}_{3329}(5, 4) = \lceil (3329 / 16) \cdot 5 \rfloor = \lceil 1040.3 \rfloor = 1040$$

Der ursprüngliche Wert 1000 wird zu 1040 rekonstruiert – ein kleiner Fehler von 40, der durch das LWE-Rauschen toleriert wird.

**Compress/Decompress (Polynom):**
Für ein Polynom $f \in R_q$ wird die Funktion koeffizientenweise angewendet:
$$\text{Compress}_q(f, d) = \sum_{i=0}^{n-1} \text{Compress}_q(f_i, d) \cdot x^i$$

**Beispiel (Polynom):** Sei $f(x) = 1000 + 2500x + 500x^2$ mit $q = 3329$, $d = 4$.

*Kompression:*
- $f_0 = 1000 \rightarrow 5$
- $f_1 = 2500 \rightarrow \lceil (16/3329) \cdot 2500 \rfloor = 12$
- $f_2 = 500 \rightarrow \lceil (16/3329) \cdot 500 \rfloor = 2$

Komprimiertes Polynom: $5 + 12x + 2x^2$ (nur 4 Bits pro Koeffizient statt 12)

*Dekompression:*
- $5 \rightarrow 1040$
- $12 \rightarrow 2497$
- $2 \rightarrow 416$

Rekonstruiertes Polynom: $1040 + 2497x + 416x^2$

### Ciphertext Compression

In Kyber wird der Ciphertext $c = (c_1, c_2)$ komprimiert, um die Übertragungsgröße zu reduzieren:

*   $c_1 \in R_q^k$: Komprimiert mit $d_u = 10$ Bits pro Koeffizient
*   $c_2 \in R_q$: Komprimiert mit $d_v = 4$ Bits pro Koeffizient

**Kyber-768 Ciphertext-Größe nach Kompression:**
- $c_1$: $3 \times 256 \times 10$ bits = 960 bytes
- $c_2$: $256 \times 4$ bits = 128 bytes
- **Gesamt: 1088 bytes** (statt 1536 bytes unkomprimiert)

**Funktionsweise:**
Die Kompression fügt zusätzliches Rauschen hinzu. Solange dieses Rauschen zusammen mit dem LWE-Fehler klein genug bleibt (unter $q/4$), kann Alice die Nachricht korrekt entschlüsseln. Die Parameter $d_u$ und $d_v$ sind so gewählt, dass die Decryption Failure Rate vernachlässigbar klein ist ($< 2^{-139}$ für Kyber-768).

### NTT (Number Theoretic Transform)

**Problem:** Polynom-Multiplikation in $R_q$ hat naiv Komplexität $O(n^2)$. Bei $n = 256$ ist das sehr langsam.

**Lösung:** Die Number Theoretic Transform (NTT) ist die modulare Variante der Fast Fourier Transform (FFT). Sie reduziert die Komplexität auf $O(n \log n)$.

**Idee:** 
1. Transformiere beide Polynome in den "NTT-Raum" (Punktweise Darstellung)
2. Multipliziere punktweise (nur $O(n)$)
3. Transformiere zurück

**Mathematisch:**
Sei $\omega$ eine primitive $n$-te Einheitswurzel modulo $q$ (d.h. $\omega^n \equiv 1 \pmod q$).

$$\text{NTT}(f) = \hat{f}, \quad \text{wobei } \hat{f}_i = \sum_{j=0}^{n-1} f_j \cdot \omega^{ij} \pmod q$$

Kyber wählt $q = 3329$, weil:
1. $q \equiv 1 \pmod{256}$, daher existiert eine 256-te Einheitswurzel
2. $q$ ist prim (einfache modulare Arithmetik)
3. $q$ passt in 12 Bits

**In Kyber:**
- Schlüssel und Ciphertexts werden intern im NTT-Raum gespeichert
- Multiplikationen sind dadurch schnell
- Nur bei Ein-/Ausgabe wird zurücktransformiert

## Kyber-KEM

### Bedeutung von KEM:

Ein **Key Encapsulation Mechanism (KEM)** ist ein asymmetrisches Verfahren zum sicheren Austausch eines symmetrischen Schlüssels. Im Gegensatz zu klassischem Public-Key-Encryption (PKE) verschlüsselt ein KEM keine beliebige Nachricht, sondern kapselt einen zufällig generierten Schlüssel.

**KEM besteht aus drei Algorithmen:**

1. **KeyGen()** $\rightarrow (pk, sk)$: Erzeugt Schlüsselpaar
2. **Encaps(pk)** $\rightarrow (c, K)$: Erzeugt Ciphertext $c$ und Shared Secret $K$
3. **Decaps(sk, c)** $\rightarrow K$: Extrahiert Shared Secret $K$ aus Ciphertext

**KEM vs. Key Exchange (z.B. ECDH):**

| Aspekt | ECDH | KEM |
|--------|------|-----|
| Interaktion | Beide Parteien tragen bei | Eine Partei wählt das Geheimnis |
| Berechnung | $K = g^{ab}$ (symmetrisch) | Encaps/Decaps (asymmetrisch) |
| Ergebnis | Shared Secret für symmetrische Verschlüsselung | Shared Secret für symmetrische Verschlüsselung |

### Von PKE zu KEM: Fujisaki-Okamoto Transform

**Problem:** Kyber-PKE (wie oben beschrieben) ist nur **IND-CPA** sicher (sicher gegen passive Angreifer). Für TLS brauchen wir **IND-CCA2** Sicherheit (sicher gegen aktive Angreifer, die Ciphertexts manipulieren können).

**Lösung:** Die Fujisaki-Okamoto (FO) Transformation verwandelt ein IND-CPA-sicheres PKE-Schema in ein IND-CCA2-sicheres KEM.

**Grundidee:**
1. Der Zufall für die Verschlüsselung wird nicht zufällig gewählt, sondern aus der Nachricht $m$ deterministisch abgeleitet
2. Bei der Entschlüsselung wird die Verschlüsselung **neu berechnet** und mit dem empfangenen Ciphertext verglichen
3. Stimmen sie nicht überein → Manipulation erkannt → Ablehnung

**Kyber-KEM Ablauf:**

**Encaps(pk):**
1. Wähle zufällige Nachricht $m \in \{0,1\}^{256}$
2. Berechne $(K, r) = G(m \| H(pk))$ wobei $G$ eine Hash-Funktion ist
3. Berechne Ciphertext $c = \text{PKE.Encrypt}(pk, m; r)$ mit Zufall $r$
4. Berechne Shared Secret $K' = H(K \| H(c))$
5. Output $(c, K')$

**Decaps(sk, c):**
1. Entschlüssle $m' = \text{PKE.Decrypt}(sk, c)$
2. Berechne $(K, r) = G(m' \| H(pk))$
3. Berechne $c' = \text{PKE.Encrypt}(pk, m'; r)$ ← **Re-Encryption**
4. **Vergleiche:** Wenn $c' = c$:
   - Output $K' = H(K \| H(c))$
5. **Sonst (Manipulation!):**
   - Output $K' = H(z \| H(c))$ wobei $z$ ein geheimer Zufallswert aus $sk$ ist

**Warum ist das sicher?**
- Ein Angreifer kann keinen gültigen Ciphertext für eine Nachricht $m'$ erzeugen, ohne $m'$ zu kennen (weil $r$ von $m$ abhängt)
- Manipulierte Ciphertexts führen zu einem unabhängigen Schlüssel $K'$, der dem Angreifer keine Information gibt

### Kyber-KEM Parameter (ML-KEM-768)

| Parameter | Wert |
|-----------|------|
| Encapsulation Key | 1184 bytes |
| Decapsulation Key | 2400 bytes |
| Ciphertext | 1088 bytes |
| Shared Secret | 32 bytes |
| Security Level | NIST Level 3 (~AES-192) |

## Resources
- Menezes, Alfred. THE MATHEMATICS OF LATTICE-BASED CRYPTOGRAPHY. n.d.
- Lyubashevsky, Vadim, Chris Peikert, and Oded Regev. “On Ideal Lattices and Learning with Errors over Rings.” J. ACM (New York, NY, USA) 60, no. 6 (2013). https://doi.org/10.1145/2535925.
- Micciancio, Daniele. “Generalized Compact Knapsacks, Cyclic Lattices, and Efficient One-Way Functions.” Computational Complexity 16, no. 4 (2007): 365–411. https://doi.org/10.1007/s00037-007-0234-9.
- Langlois, Adeline, and Damien Stehlé. “Worst-Case to Average-Case Reductions for Module Lattices.” Designs, Codes and Cryptography 75, no. 3 (2015): 565–99. https://doi.org/10.1007/s10623-014-9938-4.
