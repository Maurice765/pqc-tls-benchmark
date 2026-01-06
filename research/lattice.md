# Lattice-based Cryptography (Gitterbasierte Kryptographie)

## Key Concepts
Gitter (Lattices) sind regelmäßige Punktgitter in einem n-dimensionalen Raum.
Sie sind die Grundlage für die aktuelle PQC-Verfahren (Kyber, Dilithium).

## Mathematical Foundation
Ein Gitter wird durch eine Basis $B = \{b_1, ..., b_n\}$ aufgespannt. Jeder Punkt im Gitter ist eine ganzzahlige Linearkombination dieser Basisvektoren.

$$ L = \{ a_1 b_1 + ... + a_n b_n \mid a_i \in \mathbb{Z} \} $$

### The Hard Problems (Warum ist das sicher?)
Während Faktorisierung (RSA) und Diskreter Logarithmus (ECC) von Quantencomputern gelöst werden können, gelten bestimmte Probleme auf Gittern als "schwer" auch für Quantencomputer.

1.  **SVP (Shortest Vector Problem):** Finde den kürzesten Vektor im Gitter (der nicht der Nullvektor ist).
    *   In 2D (auf Papier) einfach zu sehen.
    *   In 500+ Dimensionen extrem schwer.
2.  **CVP (Closest Vector Problem):** Gegeben ein Punkt im Raum (nicht auf dem Gitter), finde den Gitterpunkt, der am nächsten liegt.
    *   Das ist im Prinzip das "Rauschen entfernen" bei LWE.

## Impact on Project
Kyber's Sicherheit beruht darauf, dass das Lösen von Module-LWE so schwer ist wie das Lösen von SVP in einem Gitter (Worst-case to average-case reduction).

## Resources
*   [Lattice-based Cryptography - Simons Institute](https://simons.berkeley.edu/)
