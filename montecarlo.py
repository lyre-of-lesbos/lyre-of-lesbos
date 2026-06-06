import math
import random

def haversine(lat1, lon1, lat2, lon2):
    """
    Υπολογισμός της γεωδαιτικής απόστασης μεταξύ δύο σημείων 
    στη Γη με τον αλγόριθμο Haversine (σε χιλιόμετρα).
    """
    R = 6371.0  # Ακτίνα της Γης σε km
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def km_to_stadia(km):
    """Μετατροπή χιλιομέτρων σε Κλασικά Στάδια (1 Στάδιο = 185 μέτρα)"""
    return (km * 1000.0) / 185.0

def check_ratio(val1, val2, target_ratio, tolerance=0.025):
    """Έλεγχος αν ο λόγος δύο τιμών προσεγγίζει έναν στόχο εντός ορίου ανοχής"""
    if val2 == 0:
        return False
    current_ratio = val1 / val2
    return abs(current_ratio - target_ratio) / target_ratio <= tolerance

def run_simulation():
    # --- ΣΤΑΘΕΡΟΙ ΚΟΜΒΟΙ (Βάσει των νέων δεδομένων σας) ---
    nodes_fixed = {
        'A': (39.253118, 25.969156),  # Μαντείο Ορφέα
        'D': (39.196404, 26.305275),  # Ιερό των Μέσσων
        'E': (39.368500, 26.174800),  # Αρχαία Μήθυμνα
        'F': (39.111200, 26.562300)   # Ακρόπολη Μυτιλήνης
    }
    
    # --- ΓΕΩΓΡΑΦΙΚΟ ΠΛΑΙΣΙΟ ΛΕΣΒΟΥ (Bounding Box για τυχαία σημεία) ---
    LAT_MIN, LAT_MAX = 39.05, 39.40
    LON_MIN, LON_MAX = 25.85, 26.65
    
    # Υπολογισμός πραγματικών αποστάσεων σταθερών αξόνων (σε Στάδια)
    dist_D_E = km_to_stadia(haversine(*nodes_fixed['D'], *nodes_fixed['E']))  # Μέσσα -> Μήθυμνα (~120)
    dist_D_A = km_to_stadia(haversine(*nodes_fixed['D'], *nodes_fixed['A']))  # Μέσσα -> Μαντείο (~160)
    
    print("--- Επαλήθευση Πραγματικών Σταθερών Αξόνων ---")
    print(f"Μέσσα -> Μήθυμνα: {dist_D_E:.2f} Στάδια (Θεωρητικό: 120, Απόκλιση: {abs(dist_D_E-120)/120*100:.2f}%)")
    print(f"Μέσσα -> Μαντείο: {dist_D_A:.2f} Στάδια (Θεωρητικό: 160, Απόκλιση: {abs(dist_D_A-160)/160*100:.2f}%)")
    print("-" * 47)

    # Παράμετροι προσομοίωσης
    N_SIMULATIONS = 10000
    success_count = 0
    TOLERANCE = 0.015  # Αυστηρή ανοχή 1.5% λόγω αυξημένης ακρίβειας των νέων σημείων
    
    print(f"Έναρξη προσομοίωσης Monte Carlo ({N_SIMULATIONS} επαναλήψεις)...")
    
    for _ in range(N_SIMULATIONS):
        # Παραγωγή 2 τυχαίων ενδιάμεσων κόμβων (B = Ερεσός, C = Φίλια)
        B_lat = random.uniform(LAT_MIN, LAT_MAX)
        B_lon = random.uniform(LON_MIN, LON_MAX)
        
        C_lat = random.uniform(LAT_MIN, LAT_MAX)
        C_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Υπολογισμός των μεταβαλλόμενων αποστάσεων του δικτύου
        dist_A_B = km_to_stadia(haversine(*nodes_fixed['A'], B_lat, B_lon))  # Μαντείο -> Ερεσός
        dist_A_C = km_to_stadia(haversine(*nodes_fixed['A'], C_lat, C_lon))  # Μαντείο -> Φίλια
        dist_B_C = km_to_stadia(haversine(B_lat, B_lon, C_lat, C_lon))      # Ερεσός -> Φίλια
        dist_C_F = km_to_stadia(haversine(C_lat, C_lon, *nodes_fixed['F']))  # Φίλια -> Μυτιλήνη
        
        # Έλεγχος σύμπτωσης Πυθαγόρειων Μουσικών Λόγων και Γεωμετρίας
        matches = 0
        
        # 1. Διά Τεσσάρων Συμφωνία (Μέσσα->Μήθυμνα / Μέσσα->Μαντείο = 120/160 = 3:4)
        if check_ratio(dist_D_E, dist_D_A, 0.75, TOLERANCE):
            matches += 1
            
        # 2. Αναλογία Δυτικού Τριγώνου (Βάση προς πλευρά Ερεσός->Φίλια / Μαντείο->Ερεσός = 97/55)
        if check_ratio(dist_B_C, dist_A_B, 97/55, TOLERANCE):
            matches += 1
            
        # 3. Σχέση Μαντείου προς Φίλια (68 στάδια) σε σχέση με Μέσσα->Μήθυμνα (120 στάδια)
        if check_ratio(dist_A_C, dist_D_E, 68/120, TOLERANCE):
            matches += 1
            
        # 4. Γεωμετρική σχέση Φίλια->Μυτιλήνη (223 στάδια) προς Μέσσα->Μαντείο (160 στάδια)
        if check_ratio(dist_C_F, dist_D_A, 223/160, TOLERANCE):
            matches += 1

        # Αν επιτυγχάνονται ταυτόχρονα οι γεωμετρικές/μουσικές ιδιότητες
        if matches >= 3:
            success_count += 1

    # Υπολογισμός τελικού p-value
    p_value = success_count / N_SIMULATIONS
    
    print("\n--- ΑΠΟΤΕΛΕΣΜΑΤΑ ΠΡΟΣΟΜΟΙΩΣΗΣ ---")
    print(f"Συνολικές συμπτώσεις (Successes): {success_count} στις {N_SIMULATIONS}")
    print(f"Υπολογισμένο p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("Συμπέρασμα: Το αποτέλεσμα είναι ΣΤΑΤΙΣΤΙΚΑ ΣΗΜΑΝΤΙΚΟ (p < 0.05).")
        print("Η διάταξη παρουσιάζει μια εξαιρετικά σπάνια μαθηματική σύμπτωση!")
    else:
        print("Συμπέρασμα: Το αποτέλεσμα ΔΕΝ είναι στατιστικά σημαντικό.")

if __name__ == "__main__":
    run_simulation()

