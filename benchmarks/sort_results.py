import json
import statistics
import os

def load_results():
    # Versuche die Datei in results/results.json oder direkt im Ordner zu finden
    paths = ["results/saved_results/results.json"]
    for p in paths:
        if os.path.exists(p):
            print(f"Lade Ergebnisse aus: {p}")
            with open(p, 'r') as f:
                return json.load(f)
    print("Fehler: Keine results.json gefunden.")
    return []

def process_measurements(json_data):
    # Sortieren nach Latenz, Loss und dann Algorithmus für übersichtliche Ausgabe
    json_data.sort(key=lambda x: (x.get('latency_ms', 0), x.get('packet_loss_percent', 0), x['algorithm']))

    output_list = []

    for entry in json_data:
        algo = entry["algorithm"]
        lat = entry.get("latency_ms", 0)
        loss = entry.get("packet_loss_percent", 0)
        
        # Prüfen ob Rohdaten vorhanden sind
        if "handshake_raw" not in entry or not entry["handshake_raw"]:
            continue

        # 1. Zahlen sortieren (Aufsteigend)
        sorted_handshake = sorted(entry["handshake_raw"])
        sorted_transfer = sorted(entry.get("transfer_raw", []))
        
        # 2. Statistiken berechnen und Struktur bauen
        result_entry = {
            "algorithm": algo,
            "latency_ms": lat,
            "packet_loss_percent": loss,
            "handshake": {
                "raw_sorted": sorted_handshake,
                "min": min(sorted_handshake),
                "median": statistics.median(sorted_handshake),
                "max": max(sorted_handshake)
            }
        }

        if sorted_transfer:
            result_entry["transfer"] = {
                "raw_sorted": sorted_transfer,
                "min": min(sorted_transfer),
                "median": statistics.median(sorted_transfer),
                "max": max(sorted_transfer)
            }
        
        output_list.append(result_entry)

    # In Datei schreiben
    output_path = "results/saved_results/sorted_results.json"
    # Sicherstellen, dass Verzeichnis existiert (falls es abweicht)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(output_list, f, indent=2)
    
    print(f"Sortierte Ergebnisse gespeichert in: {output_path}")

if __name__ == "__main__":
    data = load_results()
    if data:
        process_measurements(data)
