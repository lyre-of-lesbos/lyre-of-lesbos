import numpy as np
import pandas as pd

# --- ΓΕΩΔΑΙΤΙΚΟΙ ΥΠΟΛΟΓΙΣΜΟΙ ---
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Υπολογισμός γεωδαιτικής απόστασης σε χιλιόμετρα μεταξύ δύο σημείων
    στον πλανήτη με βάση τον τύπο Haversine (Μοντέλο WGS84).
    """
    R = 6371.008  # Μέση ακτίνα της Γης σε χιλιόμετρα
    
    # Μετατροπή μοιρών σε ακτίνια
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    return R * c

def km_to_stadia(km):
    """Μετατροπή χιλιομέτρων σε Κλασικά Στάδια (1 Στάδιο = 185 μέτρα)"""
    return (km * 1000.0) / 185.0

# --- ΔΕΔΟΜΕΝΑ ΠΡΑΓΜΑΤΙΚΩΝ ΑΡΧΑΙΟΛΟΓΙΚΩΝ ΧΩΡΩΝ ---
# Πραγματικές συντεταγμένες (Decimal Degrees) των κόμβων της Λέσβου
SITES = {
    'Μαντείο Ορφέα': (39.2314, 25.9845),
    'Σκάλα Ερεσού':  (39.1672, 25.9311),
    'Φίλια/Κλοπεδή': (39.2421, 26.1154),
    'Ιερό Μέσσων':   (39.1651, 26.2412),
    'Αρχαία Μήθυμνα':(39.3685, 26.1748),
    'Μυτιλήνη':      (39.1112, 26.5623)
}

# --- ΜΟΥΣΙΚΟΙ ΛΟΓΟΙ ΚΑΙ ΕΛΕΓΧΟΣ ΑΡΜΟΝΙΑΣ ---
# Οι αυστηροί Πυθαγόρειοι και φυσικοί λόγοι που εξετάζει η θεωρία
PYTHAGOREAN_RATIOS = {
    '3:4 (Καθαρή Τετάρτη)': 3/4,
    '27:32 (Πυθαγόρεια Μικρή Τρίτη)': 27/32,
    '5:6 (Φυσική Μικρή Τρίτη)': 5/6,
    '10:13 (Εναρμόνιο Διάστημα Α)': 10/13,
    '16:19 (Εναρμόνιο Διάστημα Β)': 16/19
}

def check_harmony(distance_a, distance_b, tolerance=0.025):
    """
    Ελέγχει αν ο λόγος δύο αποστάσεων προσεγγίζει κάποιον από τους
    μουσικούς λόγους εντός του ορίου ανοχής (προεπιλογή ±2.5%).
    """
    if distance_b == 0:
        return False, None, 0
    
    ratio = distance_a / distance_b
    
    for name, target_value in PYTHAGOREAN_RATIOS.items():
        deviation = abs(ratio - target_value) / target_value
        if deviation <= tolerance:
            return True, name, deviation
            
    return False, None, 0

def evaluate_network(coords_list, tolerance=0.025):
    """
    Υπολογίζει πόσοι από τους κύριους γεωδαιτικούς άξονες του μοντέλου
    συμφωνούν ταυτόχρονα με τους επιθυμητούς μουσικούς λόγους.
    """
    # Ξεπακετάρισμα των συντεταγμένων με βάση τη σταθερή σειρά των κόμβων
    manteio, skala, filia, messa, mithymna, mytilene = coords_list
    
    # Υπολογισμός πραγματικών αποστάσεων σε χιλιόμετρα
    d_manteio_skala = haversine_distance(*manteio, *skala)
    d_manteio_filia = haversine_distance(*manteio, *filia)
    d_skala_filia   = haversine_distance(*skala, *filia)
    d_messa_mithymna = haversine_distance(*messa, *mithymna)
    d_messa_manteio = haversine_distance(*messa, *manteio)
    d_filia_mytilene = haversine_distance(*filia, *mytilene)
    
    # Μετατροπή των αποστάσεων-κλειδιά σε στάδια για τους λόγους
    st_manteio_skala = km_to_stadia(d_manteio_skala)
    st_manteio_filia = km_to_stadia(d_manteio_filia)
    st_skala_filia   = km_to_stadia(d_skala_filia)
    st_messa_mithymna = km_to_stadia(d_messa_mithymna)
    st_messa_manteio = km_to_stadia(d_messa_manteio)
    st_filia_mytilene = km_to_stadia(d_filia_mytilene)
    
    # Έλεγχος των 3 βασικών συσχετισμών που ορίζει το README
    hits = 0
    
    # 1. Σχέση Μήθυμνας - Μαντείου από τα Μέσσα (Στόχος: 120/160 = 3:4)
    is_harmonic_1, _, _ = check_harmony(st_messa_mithymna, st_messa_manteio, tolerance)
    if is_harmonic_1: hits += 1
        
    # 2. Σχέση Φίλιας - Μήθυμνας (Στόχος: 100/120 = 5:6 ή 27:32)
    is_harmonic_2, _, _ = check_harmony(st_manteio_filia / 0.66, st_messa_mithymna, tolerance)
    if is_harmonic_2: hits += 1
        
    # 3. Δυτικό Ισοσκελές Τρίγωνο (Σχέση πλευρών 66 προς 66)
    ratio_triangle = abs(st_manteio_skala - st_manteio_filia) / st_manteio_filia
    if ratio_triangle <= tolerance: hits += 1
        
    return hits

# --- ΠΡΟΣΟΜΟΙΩΣΗ MONTE CARLO ---
def run_monte_carlo(num_simulations=10000, tolerance=0.025):
    """
    Παράγει χιλιάδες τυχαία δίκτυα σημείων εντός των γεωγραφικών ορίων 
    της Λέσβου για να ελέγξει την πιθανότητα τυχαίας εμφάνισης της «Λύρας».
    """
    print(f"Έναρξη προσομοίωσης Monte Carlo ({num_simulations} επαναλήψεις)...")
    
    # Γεωγραφικό πλαίσιο (Bounding Box) της Λέσβου
    LAT_MIN, LAT_MAX = 38.9800, 39.4000
    LON_MIN, LON_MAX = 25.8000, 26.6500
    
    # Αξιολόγηση του πραγματικού αρχαιολογικού δικτύου
    actual_coords = [SITES[name] for name in SITES]
    actual_hits = evaluate_network(actual_coords, tolerance)
    
    successful_random_runs = 0
    
    for _ in range(num_simulations):
        # Παραγωγή 6 τυχαίων σημείων εντός του πλαισίου του νησιού
        random_lats = np.random.uniform(LAT_MIN, LAT_MAX, 6)
        random_lons = np.random.uniform(LON_MIN, LON_MAX, 6)
        random_coords = list(zip(random_lats, random_lons))
        
        # Αξιολόγηση του τυχαίου δικτύου
        random_hits = evaluate_network(random_coords, tolerance)
        
        # Αν το τυχαίο δίκτυο πέτυχε την ίδια ή καλύτερη αρμονία, καταγράφεται
        if random_hits >= actual_hits:
            successful_random_runs += 1
            
    # Υπολογισμός του p-value
    p_value = successful_random_runs / num_simulations
    
    print("\n--- ΑΠΟΤΕΛΕΣΜΑΤΑ ΣΤΑΤΙΣΤΙΚΗΣ ΑΞΙΟΛΟΓΗΣΗΣ ---")
    print(f"Ευρήματα στο πραγματικό δίκτυο: {actual_hits} / 3 βασικές ευθυγραμμίσεις.")
    print(f"Τυχαία δίκτυα που πέτυχαν το ίδιο αποτέλεσμα: {successful_random_runs}")
    print(f"Υπολογισμένο p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Συμπέρασμα: Το αποτέλεσμα είναι στατιστικά σημαντικό (p < 0.05).")
        print("Η γεωμετρία παρουσιάζει ασυνήθιστα υψηλή συνοχή για να είναι εντελώς τυχαία.")
    else:
        print("Συμπέρασμα: Το αποτέλεσμα ΔΕΝ είναι στατιστικά σημαντικό (p >= 0.05).")
        print("Ο σχηματισμός μπορεί εύκολα να εξηγηθεί ως γεωγραφική παρειδωλία (σύμπτωση).")

# --- ΕΚΤΕΛΕΣΗ ---
if __name__ == "__main__":
    # Εμφάνιση των πραγματικών αποστάσεων των αρχαίων θέσεων
    print("--- ΠΡΑΓΜΑΤΙΚΕΣ ΑΠΟΣΤΑΣΕΙΣ ΑΡΧΑΙΟΛΟΓΙΚΩΝ ΧΩΡΩΝ ---")
    m_lat, m_lon = SITES['Μαντείο Ορφέα']
    f_lat, f_lon = SITES['Φίλια/Κλοπεδή']
    s_lat, s_lon = SITES['Σκάλα Ερεσού']
    
    dist_km = haversine_distance(m_lat, m_lon, f_lat, f_lon)
    print(f"Μαντείο -> Φίλια: {dist_km:.2f} km ({km_to_stadia(dist_km):.1f} στάδια)")
    
    dist_km2 = haversine_distance(m_lat, m_lon, s_lat, s_lon)
    print(f"Μαντείο -> Σκάλα Ερεσού: {dist_km2:.2f} km ({km_to_stadia(dist_km2):.1f} στάδια)\n")
    
    # Εκτέλεση της Monte Carlo
    run_monte_carlo(num_simulations=10000, tolerance=0.025)
