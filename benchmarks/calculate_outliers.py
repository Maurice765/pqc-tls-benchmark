import json
import statistics
import os

def load_results():
    # Versuche die Datei in verschiedenen Pfaden zu finden
    paths = [
        "benchmarks/results/saved_results/results.json",
        "benchmarks/results/results.json",
        "results/saved_results/results.json", 
        "results/results.json", 
        "results.json"
    ]
    for p in paths:
        if os.path.exists(p):
            print(f"Lade Ergebnisse aus: {p}")
            with open(p, 'r') as f:
                return json.load(f)
    print("Fehler: Keine results.json gefunden.")
    return []

def calculate_outliers_stats(data):
    if not data:
        return 0, 0.0, 0.0, 0.0
    
    n = len(data)
    if n < 2:
        return 0, 0.0, sum(data), sum(data)
    
    sorted_data = sorted(data)
    
    # Quartile berechnen
    try:
        quantiles = statistics.quantiles(sorted_data, n=4)
        q1 = quantiles[0]
        q3 = quantiles[2]
    except AttributeError:
        mid = n // 2
        q1 = statistics.median(sorted_data[:mid])
        if n % 2 == 0:
            q3 = statistics.median(sorted_data[mid:])
        else:
            q3 = statistics.median(sorted_data[mid+1:])
            
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    
    outliers = [x for x in data if x < lower_bound or x > upper_bound]
    cleaned = [x for x in data if x >= lower_bound and x <= upper_bound]
    
    outlier_count = len(outliers)
    outlier_pct = (outlier_count / n) * 100
    total_sum = sum(data)
    cleaned_sum = sum(cleaned)
    cleaned_count = len(cleaned)
    
    return outlier_count, outlier_pct, total_sum, cleaned_sum, cleaned_count

def process_outliers(json_data):
    print(f"\nBerechnung der Ausreißer (Methode: 1.5 * IQR) & Durchschnittszeiten")
    
    # Sortieren nach Latenz, Loss
    json_data.sort(key=lambda x: (x.get('latency_ms', 0), x.get('packet_loss_percent', 0), x['algorithm']))

    # Definition der Gruppen
    groups = {
        "Level 1": ["mlkem512", "P-256", "p256_mlkem512"],
        "Level 3": ["mlkem768", "P-384", "p384_mlkem768"],
        "Level 5": ["mlkem1024", "P-521", "p521_mlkem1024"],
        "ECDH": ["P-256", "P-384", "P-521"],
        "Kyber": ["mlkem512", "mlkem768", "mlkem1024"],
        "Hybrid": ["p256_mlkem512", "p384_mlkem768", "p521_mlkem1024"],
        "All": ["mlkem512", "P-256", "p256_mlkem512", "mlkem768", "P-384", "p384_mlkem768", "mlkem1024", "P-521", "p521_mlkem1024"]
    }

    # Gruppieren nach Szenario (Lat, Loss) für Aggregation
    current_scenario = None
    scenario_data = []

    # Globale Zähler für Gesamtauswertung
    global_stats = {name: {
        'hs_total': 0, 'hs_outliers': 0, 
        'tx_total': 0, 'tx_outliers': 0,
        'hs_time_sum': 0.0, 'tx_time_sum': 0.0,
        'hs_cleaned_sum': 0.0, 'hs_cleaned_count': 0,
        'tx_cleaned_sum': 0.0, 'tx_cleaned_count': 0
    } for name in groups}

    def process_scenario_aggregates(lat, loss, entries):
        # Aggregation für das aktuelle Szenario berechnen
        # print("-" * 110) # Suppressed per-scenario output
        for group_name, algos in groups.items():
            
            found = False
            for entry in entries:
                if entry["algorithm"] in algos:
                    found = True
                    hs_raw = entry.get("handshake_raw", [])
                    tx_raw = entry.get("transfer_raw", [])
                    
                    # Statistiken berechnen
                    hs_cnt, hs_pct, hs_sum, hs_cl_sum, hs_cl_cnt = calculate_outliers_stats(hs_raw)
                    tx_cnt, tx_pct, tx_sum, tx_cl_sum, tx_cl_cnt = calculate_outliers_stats(tx_raw)
                    
                    # Add to globals
                    global_stats[group_name]['hs_total'] += len(hs_raw)
                    global_stats[group_name]['hs_outliers'] += hs_cnt
                    global_stats[group_name]['tx_total'] += len(tx_raw)
                    global_stats[group_name]['tx_outliers'] += tx_cnt
                    global_stats[group_name]['hs_time_sum'] += hs_sum
                    global_stats[group_name]['tx_time_sum'] += tx_sum
                    
                    global_stats[group_name]['hs_cleaned_sum'] += hs_cl_sum
                    global_stats[group_name]['hs_cleaned_count'] += hs_cl_cnt
                    global_stats[group_name]['tx_cleaned_sum'] += tx_cl_sum
                    global_stats[group_name]['tx_cleaned_count'] += tx_cl_cnt
            
            # if found:
                # print(f"SUM {group_name:<21} | {lat:<5} | {loss:<5} ...") 
        # print("-" * 110)

    for entry in json_data:
        algo = entry["algorithm"]
        lat = entry.get("latency_ms", 0)
        loss = entry.get("packet_loss_percent", 0)
        
        # Check if scenario changed
        scenario_key = (lat, loss)
        if current_scenario != scenario_key:
            if current_scenario is not None:
                process_scenario_aggregates(current_scenario[0], current_scenario[1], scenario_data)
            current_scenario = scenario_key
            scenario_data = []
        
        scenario_data.append(entry)

    # Letztes Szenario verarbeiten
    if current_scenario is not None:
        process_scenario_aggregates(current_scenario[0], current_scenario[1], scenario_data)

    # Globale Zusammenfassung ausgeben
    print("\n" + "=" * 80)
    print(f"GLOBAL SUMMARY (All Scenarios Combined)")
    print(f"{'Group':<25} | {'Outliers (HS)':<20} | {'Outliers (TX)':<20}")
    print("-" * 80)
    for group_name, stats in global_stats.items():
        hs_total = stats['hs_total']
        hs_outliers = stats['hs_outliers']
        tx_total = stats['tx_total']
        tx_outliers = stats['tx_outliers']
        
        hs_pct = (hs_outliers / hs_total * 100) if hs_total > 0 else 0
        tx_pct = (tx_outliers / tx_total * 100) if tx_total > 0 else 0
        
        hs_str = f"{hs_pct:5.1f}% ({hs_outliers}/{hs_total})"
        tx_str = f"{tx_pct:5.1f}% ({tx_outliers}/{tx_total})"
        
        print(f"{group_name:<25} | {hs_str:<20} | {tx_str:<20}")
    print("=" * 80 + "\n")

    print(f"GLOBAL SUMMARY (Average Times - Raw vs Cleaned)")
    print(f"{'Group':<25} | {'Avg HS (s)':<12} | {'Cleaned HS':<12} | {'Avg TX (s)':<12} | {'Cleaned TX':<12}")
    print("-" * 90)
    for group_name, stats in global_stats.items():
        hs_total = stats['hs_total']
        tx_total = stats['tx_total']
        hs_sum = stats['hs_time_sum']
        tx_sum = stats['tx_time_sum']
        
        hs_cl_sum = stats['hs_cleaned_sum']
        hs_cl_cnt = stats['hs_cleaned_count']
        tx_cl_sum = stats['tx_cleaned_sum']
        tx_cl_cnt = stats['tx_cleaned_count']
        
        hs_avg = (hs_sum / hs_total) if hs_total > 0 else 0.0
        tx_avg = (tx_sum / tx_total) if tx_total > 0 else 0.0
        
        hs_cl_avg = (hs_cl_sum / hs_cl_cnt) if hs_cl_cnt > 0 else 0.0
        tx_cl_avg = (tx_cl_sum / tx_cl_cnt) if tx_cl_cnt > 0 else 0.0
        
        print(f"{group_name:<25} | {hs_avg:<12.4f} | {hs_cl_avg:<12.4f} | {tx_avg:<12.4f} | {tx_cl_avg:<12.4f}")
    print("=" * 90 + "\n")


if __name__ == "__main__":
    data = load_results()
    if data:
        process_outliers(data)
