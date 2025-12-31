# Shor's Algorithm

Algorithmus von Peter Shor, der 1994 vorgeschlagen wurde. Shor's Algorithmus ist eine für Quantencomputer effiziente Lösung um den diskreten Logarithmus oder das Primfaktorzerlegungsproblem zu lösen.

## Key Concepts

Der Algorithmus nutzt die Quanten-Fourier-Transformation um die Perioden der Funktion $f(x) = a^x \bmod N$ zu finden. Diese Perioden können mit klassischen Rechnungen verwendet werden um den diskreten Logarithmus zu lösen.

## Mathematical Foundation

Um die Primfaktoren von einer Zahl N herauszufinden macht sich Shor's Algorithmus folgende Eigenschaft zu nutze:

N ist definiert als $N = p \cdot q$, wobei $p$ und $q$ Primzahlen sind. Dabei gilt, dass es eine Zahl $g$ gibt, die als $g = p \cdot c$ definiert ist, wodurch der $\text{ggT}(N,g) = p$ ist. Sobald $p$ gefunden ist ist $q = N/p$.

Die Zahl $g$ zu erraten ist jedoch sehr unwahrscheinlich, weswegen folgende Eigenschaft genutzt wird: $g^h = m \cdot N + 1$ (Beweis nicht angeguckt). Das umgeformt ergibt:
$$
(g^{h/2}+1) \cdot (g^{h/2}-1) = m \cdot N
$$

Die Idee ist also den ersten Schätzwert $g$ in einen besseren zu verwandeln mit $g^{h/2}+1$ bzw. $g^{h/2}-1$. Die beiden Faktoren können Faktoren von $p$ und $q$ sein, doch mit $\text{ggT}$ kann hier wieder mit $N$ die originalen $p$ und $q$ ermittelt werden.

3 Probleme:
1. Ein Wert kann Faktor von $N$ sein ($a \cdot N$)
2. Ein Wert kann Faktor von $m$ sein 
3. $h$ (in $g^{h/2}$) könnte ungerade sein (ganze Zahlen!)

In 37.5% der Fällen tritt dies nicht auf (Beweis ausstehend) --> nach 10 gerattenen $g$'s ist die Wahrscheinlichkeit $p$ zu finden $>99\%$

Echtes Problem: wie finden wir $h$? Mit Trial-and-Error auf einem normalen PC unrealistisch --> erst hier werden Quantencomputer relevant

(jetzt wirds schwammig)
In einen Quantencomputer (QC) können mehrere Inputs $x$ gemacht werden $(1,2,3,\dots,N)$ und es kann $g^x$ gleichzeitig berechnet werden (Verschränkung von 2 Registern) für jeden dieser Inputs $(g^1, g^2, g^3, \dots, g^N)$, Phänomen Superposition: $x \to g^x \to (x,g^x)$. Danach würde dieses Ergebnis ein weiteres mal genutzt um mit $> m \cdot N$ verglichen zu werden: $(x,g^x) \to > m \cdot N \to (x, +r)$ ($r$ für Rest).

Messungen der Superpostítion würden jedoch kein gutes Ergebnis ergeben, weil nur ein zufälliger Wert gemessen und ausgegeben wird (Doppel-Spalt-Experiment bei Superposition). 

Nutzung von folgendem Konzept: 
$$
\begin{aligned}
g^h &= m \cdot N+1 \\
g^{42} &= m_1 \cdot N+3 \\
g^{42+h} &= m_2 \cdot N+3 \\
g^{42+2h} &= m_3 \cdot N+3
\end{aligned}
$$

Daraus folgt:
$$
\begin{aligned}
g^x &= m \cdot N+r \\
g^{x+h} &= m_2 \cdot N+r
\end{aligned}
$$
$h$ hat eine wiederholende Eigenschaft: $r$ bleibt immer gleich
Eigenschaft der Superposition: wenn wir einen zufälligen Rest messen, dann bleiben nur die Superpositionen übrig, die auch diesen Rest ergeben, alle anderen vergehen
Die ergebenden Superpositionen sind dann deren Inputs, welche $h$ voneinander getrennt sind (frequency --> Fouriertransformation)

QFT (Quanten-Fourier-Transformation) 
- Einzelner Input (z.B. 1) produziert eine Sinuskurve
- Größerer Input (z.B. 2) erzeugt Kurve mit höherer Frequenz
- Superposition als Input erzeugt eine Superposition mehrerer Superpositions-Kurven zusammenaddiert

Wenn als Input also die Superpositionen alle $h$ voneinander getrennt sind erhalten wir eine Sinuskurve mit Frequenz $1/h$ (stark vereinfacht erklärt)
Das Ergebnis ist auch meist nicht exakt $1/h$, sondern eine Annäherung die dann per Kettenbruchmethode (Continued Fractions) auf das exakte $h$ bestimmt werden kann

Mit $h$ können wir dann $g$ berechnen und finden wie bereits erklärt $p$ oder $q$


## Impact on Project

k.A.

## Resources and Quotes

https://www.youtube.com/watch?v=lvTqbM5Dq4Q (Quellen aus Videobeschreibung durchzulesen)

## Open Questions

- genauere Erklärung der QFT