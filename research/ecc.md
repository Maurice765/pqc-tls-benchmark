# Elliptic Curve Cryptography (ECC)

Wird in der Vorlesung noch behandelt.

## Key Concepts

Statt Primzahlen werden Elliptische Kurven verwendet, in diesem Format: y^2 = x^3 + ax + b
Elliptische Kurven sind gespiegelt an der x-Achse

![image](/research/images/elliptic_curve.png)

## Mathematical Foundation

Eine lineare Funktion schneidet die elliptische Kurve in (meist) 3 Punkten, wodurch eine Trapdoor Function (einfach in die eine Richtung zu rechnen aber schwer in die andere, wie bei Primfaktorzerlegung) ermöglicht wird.

Vorgehen:
1. Ausgangspunkt A festlegen
2. Punkt B auf der Kurve finden
3. Gerade G durch A und B konstruieren
4. Punkt T ist der dritte Punkt der elliptische Kurve der durch die G geschnitten wird
5. T an der x-Achse spiegeln um Punkt C zu erhalten
6. Schritt 2 bis 5 wiederholen

Es ist einfach einen Punkt durch beliebiges Anwenden dieses Verfahrens zu generieren, aber schwer nur mit gegebenen finalen Punkt P und Ausgangspunkt A den Weg dorthin zu rekronstruieren (Konstruktion in Gruppe der elliptischen Kurven: A + B = C)

Es kann auch ein Punkt C mit nur Punkt A generiert werden, dafür wird die Tangente an A genutzt. C ergibt sich dann aus A --> 2A --> 3A --> nA = C (heißt Scalar Multiplication)

## Elliptic-Curve Diffie-Hellman (ECDH)

ECDH ist die elliptische Kurve Version vom Diffie-Hellman Protokoll (siehe VL).

**Parameter**:
- Elliptische Kurve $E$ über $\mathbb{Z}_p$ mit $n$ (prim)
- Ein Startpunkt $P \in E(\mathbb{Z}_p), P \neq \infty$
- Eine key derivation function (KDF), z.B. eine Hashfunktion (One-Way Function)

**Ablauf**:

1. Alice wählt $x \in_R [1,n-1]$ und berechnet $X=xP$
2. Alice sendet $X$ an Bob
3. Bob wählt $y \in_R [1,n-1]$ und brecehnet $Y=yP$
4. Bob sende $Y$ an Alice
5. Bob berechnet $K = yX$ und $k=KDF(K)$
6. Alice berechnet $K = xX$ und $k=KDF(K)$

- Alice und Bob haben nun das gleiche $k$ 
- Oscar und Eve können $X,Y$ sehen und müssen versuchen $K = xY = yX$ zu berechnen
- Diese Berechnung ist eine Instanz von elliptic curve discrete logarithm problem (ECDLP)

Diese Version von ECDH kann als unauthenticated betrachtet werden, da hier die Gefahr eines Malicious Intruder-in-the-Middle (MITM) Angriff besteht. Um diese Gefahr zu umgehen kann ECDH authenticated vollzogen werden, indem Alice ihr $X$ an Bob sendet und es dabei mit ECDSA signiert und ein Zertifikat für den ECDSA public key mitschickt. Gleiches macht Bob mit $Y$.

**Curve25519**: Als Standard für eine elliptische Kurve wird oft die von Dan Bernstein in 2005 erfundene Curve25519 benutzt.

- $p=2^{255} - 19$ ist eine Primzahl
- Curve25519 bietet 128-bit Sicherheit 
- Die Curve25519 ist die elliptische Kurve $Y^2=X^3+48662X^2 + X$


## Impact on Project

ECDH braucht für die gleiche Sicherheit von RSA kleinere Schlüssel und war deswegen lange der Standard. Jedoch kann das ECDLP durch Shor's Algorithmus gelöst werden, wodurch Quantensichere Verfahren nötig sind.

## Resources and Quotes

- Menezes, Alfred. ELLIPTIC CURVE CRYPTOGRAPHY. n.d.
- The Cloudflare Blog. “A (Relatively Easy To Understand) Primer on Elliptic Curve Cryptography.” October 24, 2013. https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography/.
- Boyd, Colin, Anish Mathuria, and Douglas Stebila. Protocols for Authentication and Key Establishment. Information Security and Cryptography. Springer, 2020. https://doi.org/10.1007/978-3-662-58146-9.
- Bernstein, Daniel J. “Curve25519: New Diffie-Hellman Speed Records.” In Public Key Cryptography - PKC 2006, edited by Moti Yung, Yevgeniy Dodis, Aggelos Kiayias, and Tal Malkin. Springer, 2006. https://doi.org/10.1007/11745853_14.


