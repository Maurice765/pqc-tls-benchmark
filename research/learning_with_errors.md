# Learning with Errors

## Key Concepts

LWE basiert auf Gleichungssystemen mit Fehlertermen, bei denen es unmöglich ist die Lösung zu bestimmen. Solch ein Gleichungssystem stellt den Public Key dar, in welchem Bob seine Nachricht verschlüsselt

## Mathematical Foundation

Folgendes Gleichungssystem sei angenommen und stellt den Public Key dar:

$$
\begin{aligned}
77x + 7y + 28z + 23w &= 2859 \\
21x + 19y + 30z + 48w &= 3508 \\
4x + 24y + 33z + 38w &= 3848 \\
8x + 20y + 84z + 61w &= 6225 \\
...
\end{aligned}
$$

Alice hat ihren Private Key um dieses Gleichungssystem zu lösen:
$$
\begin{aligned}
x &= 10 \\
y &= 82 \\
z &= 50 \\
w &= 5
\end{aligned}
$$

Jedoch ist es für einen Computer sehr einfach das Gleichungssystem zu lösen, da es sich um ein lineares Gleichungssystem handelt. Das Ganze nennt man Learning Without Errors.

Um dieses Problem zu lösen wird ein Fehlerterm hinzugefügt, der das Gleichungssystem nicht mehr lösbar macht. Dies nennt man dann Learning With Errors.

Dafür wird auf das Ergebnis jeder Gleichung ein Fehlerterm hinzugefügt:
$$
\begin{aligned}
77x + 7y + 28z + 23w &= 2859 + -3\\
21x + 19y + 30z + 48w &= 3508 + 2\\
4x + 24y + 33z + 38w &= 3848 + -1\\
8x + 20y + 84z + 61w &= 6225 + 0\\
...
\end{aligned}
$$

Dadurch kann das Gleichungssystem nicht mehr gelöst werden, da nur Alice weiß welche Fehlertermen hinzugefügt wurden und nur sie den Private Key besitzt.

Wie standardmäßig in der Kryptographie wird hier mit modularer Arithmetik (mod) gearbeitet.

$$
\begin{aligned}
77x + 7y + 28z + 23w &= 2859 \bmod 89 &= 11\\
21x + 19y + 30z + 48w &= 3508 \bmod 89 &= 37\\
4x + 24y + 33z + 38w &= 3848 \bmod 89 &= 21\\
8x + 20y + 84z + 61w &= 6225 \bmod 89 &= 84\\
...
\end{aligned}
$$

### Verschlüsselung

Für das Verschlüsseln nimmt Bob eine zufällige Menge an Gleichungen aus dem Public Key und addiert diese:

$$
\begin{aligned}
21x + 19y + 30z + 48w &= 37 + 2 \bmod 89\\
4x + 24y + 33z + 38w &= 21 + -1 \bmod 89\\
5x + 24y + 79z + 27w &= 51 + -2 \bmod 89\\
\hline
30x + 67y + 53z + 24w &= 19 + -1 \bmod 89\\
\end{aligned}
$$

Wenn Bob nun "0" senden möchte sendet er die neue Gleichung:

$$
\begin{aligned}
30x + 67y + 53z + 24w &= 19 + 0\bmod 89\\
\end{aligned}
$$

Wenn Bob "1" senden möchte sendet er die neue Gleichung plus 44:

$$
\begin{aligned}
30x + 67y + 53z + 24w &= 19 + 44 \bmod 89\\
\end{aligned}
$$

44 ist die Hälfte von 89 abgerundet (Modulo Arithmetik)

### Entschlüsselung

Bob sendet folgende Gleichung:

$$
\begin{aligned}
49x + 85y + 3z + 78w &= 81\bmod 89\\
\end{aligned}
$$

Das Ergebnis 81 besteht aus 2 Teilen:
- der echten Lösung
- dem enkodierten Bit

Alice nutzt ihren Private Key um die Gleichung zu lösen:

$$
\begin{aligned}
49 \cdot 10 + 85 \cdot 82 + 3 \cdot 50 + 78 \cdot 5 &= 79 \bmod 89\\
\end{aligned}
$$

79 ist die echte Lösung, wodurch das enkodierte Bit der Rest 2 ist. Jedoch sollte das Bit 0 oder 44 sein, durch den Fehler (Rauschen) wurde der echte Wert jedoch verschoben. Da Alice jedoch diese Information hat und weiß das wir mit Modulo 89 rechnen, ist die Lösung entweder nahe 0 oder nahe 44 (Regev-Encyption von Oded Regev). 2 ist näher an 0 als an 44, wodurch Alice weiß das der Bit 0 ist.

### Bedingungen

- Bob muss eine zufällige Menge an Gleichungen aus dem Public Key auswählen und darf nicht nur eine Gleichung nehmen, da Angreifer dann wissen welche Gleichung verwendet wurde
- Alice kann die Nachricht falsch entschlüsseln, wenn Bob zu viele Gleichungen addiert und die Summe der Fehler größer als (N/4) wird

## Formal Definitons

### Mathematische Definition von LWE

**Definition:** Learning With Error problem: $\text{LWE}(m, n, q, B)$

Sei $s \in_R \mathbb{Z}_q^n$ (geheim, zufällig gewählt) und $e \in_R [-B, B]^m$ (Fehler, zufällig aus kleinem Intervall), wobei $B \ll q/2$.

Gegeben $A \in_R \mathbb{Z}_q^{m \times n}$ (öffentliche Matrix) und
$$ b = As + e \pmod q \in \mathbb{Z}_q^m $$
Finde $s$.


### Decisional LWE und ss-DLWE

Neben dem Finden von $s$ (Search-LWE) gibt es das Entscheidungsproblem:

1.  **Decisional LWE (DLWE):** Unterscheide Paare $(a_i, b_i)$, die wie oben erzeugt wurden ("echt"), von Paaren, die komplett zufällig uniform aus $\mathbb{Z}_q^n \times \mathbb{Z}_q$ gezogen wurden ("Müll").
    *   *Warum wichtig?* Wenn ein Angreifer verschlüsselte Nachrichten nicht von Zufallszahlen unterscheiden kann, ist die Verschlüsselung sicher (IND-CPA Sicherheit). Menezes zeigt, dass dies so schwer ist wie Search-LWE.

2.  **ss-DLWE (Small Secret DLWE):**
    *   Beim normalen LWE ist das Geheimnis $s$ zufällig aus dem ganzen Raum $\mathbb{Z}_q^n$.
    *   Beim **ss-DLWE** werden die Komponenten von $s$ ebenfalls aus der "kleinen" Fehlerverteilung $\chi$ gezogen (genau wie die Fehler $e$).
    *   *Kyber-Relevanz:* Kyber nutzt diese Variante! Das spart Platz und macht Berechnungen effizienter, ohne die Sicherheit zu verringern (unter bestimmten Bedingungen).

## Lindner-Peikert PKE (Die Basis von Kyber)

Kyber ist im Kern eine optimierte Version des Lindner-Peikert Verschlüsselungsverfahrens (2011), nur über Polynom-Ringen (Module) statt Matrizen.

### Ablauf (Visualisierung)

**1. KeyGen (Alice):**
Alice wählt:
- Eine öffentliche Matrix $A$ (jeder kennt sie, zufällig).
- Ein geheimes $s$ (kleine Zahlen).
- Einen geheimen Fehler $e$ (kleine Zahlen).
Sie berechnet ihren Public Key $b$:
$$ b = A \cdot s + e $$
*(Vergleich: Das ist genau LWE! $b$ sieht für jeden ohne $s$ aus wie Zufall.)*

**2. Encryption (Bob):**
Bob will eine Nachricht $m$ (Bits) an Alice senden. Er wählt:
- Zufällige kleine Vektoren $s', e', e''$ (sein "Ephemeral Key").
Er berechnet zwei Dinge:
1.  Einen "Hinweis" für Alice: $u = A^T \cdot s' + e'$
2.  Die maskierte Nachricht: $v = b^T \cdot s' + e'' + \text{Encode}(m)$

Bob sendet $(u, v)$ an Alice.

**3. Decryption (Alice):**
Alice empfängt $(u, v)$. Sie rechnet:
$$ m' = v - s^T \cdot u $$

Warum funktioniert das?
$$ v - s^T u \approx (A s + e)^T s' - s^T (A^T s') \approx \text{Encode}(m) $$
(Die Terme mit $A$ heben sich weg, übrig bleiben nur die kleinen Fehlerterme und die Nachricht. Da die Fehler klein sind, kann Alice runden und erhält $m$ zurück.)

### Beispiel (für Folien)

Statt riesiger Matrizen, hier mit kleinen Zahlen (Dimension 1, Modulo 100):

*   **Public ($A$):** 42
*   **Alice Secret ($s$):** 3 (klein)
*   **Alice Error ($e$):** 1 (klein)
*   **Alice Public Key ($b$):** $42 \cdot 3 + 1 = 127 \equiv 27 \bmod 100$

Alice veröffentlicht: $(A=42, b=27)$.

**Bob verschlüsselt Nachricht $m=1$ (codiert als 50):**
*   Bob Secret ($s'$): 2 (klein)
*   Bob Errors ($e', e''$): 1, -1
*   $u = 42 \cdot 2 + 1 = 85$
*   $v = 27 \cdot 2 + (-1) + 50 = 54 + 49 = 103 \equiv 3 \bmod 100$
Bob sendet $(u=85, v=3)$.

**Alice entschlüsselt:**
*   $v - s \cdot u = 3 - (3 \cdot 85) = 3 - 255 = -252 \equiv 48 \bmod 100$
*   Alice rundet $48$ zur nächsten "großen" Zahl (0 oder 50). $48 \approx 50$.
*   Decodiert: Nachricht $m=1$.

## Impact on Project

LWE ist die Grundlage für Gitter-Verschlüsselung, die von Kyber verwendet wird.
*   Kyber nutzt **Module-LWE**: Das ist exakt das obige Lindner-Peikert Schema, aber $A, s, e$ sind keine Zahlen/Vektoren, sondern Polynome.
*   Das Prinzip ($b = As+e$, $u=A^Ts'+e'$, etc.) bleibt mathematisch identisch.

## Resources and Quotes

https://www.youtube.com/watch?v=K026C5YaB3A

## Open Questions
