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

## Impact on Project

LWE ist die Grundlage für Gitter-Verschlüsselung, die von Kyber verwendet wird

## Resources and Quotes

https://www.youtube.com/watch?v=K026C5YaB3A

## Open Questions
