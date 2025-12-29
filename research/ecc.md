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
## Impact on Project

n.V.

## Resources and Quotes

https://blog.cloudflare.com/a-relatively-easy-to-understand-primer-on-elliptic-curve-cryptography

## Open Questions

