# Shor's Algorithm

Algorithmus von Peter Shor, der 1994 vorgeschlagen wurde. Shor's Algorithmus ist eine für Quantencomputer effiziente Lösung um den diskreten Logarithmus zu lösen.

## Key Concepts

Der Algorithmus nutzt die Quanten-Fourier-Transformation um die Perioden der Funktion f(x) = a^x mod N zu finden. Diese Perioden können mit klassischen Rechnungen verwendet werden um den diskreten Logarithmus zu lösen.

## Mathematical Foundation

Um die Primfaktoren von einer Zahl N herauszufinden macht sich Shor's Algorithmus folgende Eigenschaft zu nutze:

N ist definiert als N = p * q, wobei p und q Primzahlen sind. Dabei gilt, dass es eine Zahl g gibt, die als g = p * c definiert ist, wodurch der ggT(N,g) = p ist. Sobald p gefunden ist ist q = N/p.

Die Zahl g zu erraten ist jedoch sehr unwahrscheinlich, weswegen folgende Eigenachaft genutzt wird: g^h = m * N + 1 (Beweis nicht angeguckt). Das umgeformt ergibt:
```
(g^(h/2)+1) * (g^(h/2)-1) = m * N
```

Die Idee ist also den ersten Schätzwert g in einen besseren zu verwandeln mit g^(h/2)+1 bzw. g^(h/2)-1. Die beiden Faktoren können Faktoren von p und q sein, doch mit ggT kann hier wieder mit N die originalen p und q ermittelt werden.

3 Probleme:
1. Ein Wert kann Faktor von N sein (a * N)
2. Ein Wert kann Faktor von m sein 
3. h (in g^(h/2)) könnte ungerade sein (ganze Zahlen!)

In 37.5% der Fällen tritt dies nicht auf (Beweis ausstehend) --> nach 10 gerattenen g's ist die Wahrscheinlichkeit p zu finden >99%

Echtes Problem: wie finden wir h? Mit Trial-and-Error auf einem normalen PC unrealistisch --> erst hier werden Quantencomputer relevant

(jetzt wirds schwammig)
In einen Quantencomputer (QC) können mehrere Inputs x gemacht werden (1,2,3,...,N) und es kann g^x gleichzeitig berechnet werden für jeden dieser Inputs (g¹, g², g³, ... g^N), Phänomen Superposition: x --> g^x --> x,g^x. Danach würde dieses Ergebnis ein weiteres mal genutzt um mit >m*N verglichen zu werden: x,g^x --> > m * N --> x, +r (R für Rest).

Messungen der Superpostítion würden jedoch kein gutes Ergebnis ergeben, weil nur ein zufälliger Wert gemessen und ausgegeben wird (Doppel-Spalt-Experiment bei Superposition). 

Nutzung von folgendem Konzept: 
```
g^h = m*N+1
g^42 = m_1*N+3
g^(42+h) = m_2*N+3
g^(42+2h) = m_3*N+3

leads to
g^x = m*N+r
g^(x+h) = m_2*N+r
```
h hat eine wiederholende Eigenschaft: r bleibt immer gleich
Eigenschaft der Superposition: wenn wir einen zufälligen Rest messen, dann bleiben nur die Superpositionen übrig, die auch diesen Rest ergeben, alle anderen vergehen
Die ergebenden Superpositionen sind dann deren Inputs, welche h voneinander getrennt sind (frequency --> Fouriertransformation)

QFT (Quanten-Fourier-Transformation) 
- Einzelner Input (z.B. 1) produziert eine Sinuskurve
- Größerer Input (z.B. 2) erzeugt Kurve mit höherer Frequenz
- Superposition als Input erzeugt eine Superposition mehrerer Superpositions-Kurven zusammenaddiert

Wenn als Input also die Superpositionen alle h voneinander getrennt sind erhalten wir eine Sinuskurve mit frequenz 1/h (stark vereinfacht erklärt)

Mit h können wir dann g berechnen und finden wir bereits erklärt p oder q


## Impact on Project

## Resources and Quotes

## Open Questions
