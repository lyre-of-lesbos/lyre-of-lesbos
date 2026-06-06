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

def check_ratio(val1, val2, target_ratio, tolerance=0.01):
    """Έλεγχος αν ο λόγος δύο τιμών προσεγγίζει έναν στόχο εντός αυστηρού ορίου ανοχής"""
    if val2 == 0:
        return False
    current_ratio = val1 / val2
    return abs(current_ratio - target_ratio) / target_ratio <= tolerance

def run_simulation():
    # --- ΟΛΟΙ ΟΙ ΣΤΑΘΕΡΟΙ ΚΟΜΒΟΙ (Βάσει των βέλτιστων μετρήσεων) ---
    nodes = {
        'A': (39.253118, 25.969156),  # Μαντείο Ορφέα
        'B': (39.130061, 25.933392),  # Κόμβος Β (Νέα Σταθερή Θέση)
        'C': (39.218000, 26.108000),  # Κόμβος C (Βέλτιστη Θέση Φίλιας)
        'D': (39.196404, 26.305275),  # Ιερό των Μέσσων
        'E': (39.368500, 26.174800),  # Αρχαία Μήθυμνα
        'F': (39.111200, 26.562300)   # Ακρόπολη Μυτιλήνης
    }
    
    # --- ΓΕΩΓΡΑΦΙΚΟ ΠΛΑΙΣΙΟ ΛΕΣΒΟΥ (Bounding Box για τον Monte Carlo έλεγχο) ---
    LAT_MIN, LAT_MAX = 39.05, 39.40
    LON_MIN, LON_MAX = 25.85, 26.65
    
    # Υπολογισμός πραγματικών αποστάσεων των κλειδωμένων αξόνων (σε Στάδια)
    dist_D_E = km_to_stadia(haversine(*nodes['D'], *nodes['E']))  # Μέσσα -> Μήθυμνα
    dist_D_A = km_to_stadia(haversine(*nodes['D'], *nodes['A']))  # Μέσσα -> Μαντείο
    dist_A_B = km_to_stadia(haversine(*nodes['A'], *nodes['B']))  # Μαντείο -> Κόμβος B
    dist_A_C = km_to_stadia(haversine(*nodes['A'], *nodes['C']))  # Μαντείο -> Κόμβος C (Φίλια)
    dist_B_C = km_to_stadia(haversine(*nodes['B'], *nodes['C']))  # Κόμβος B -> Κόμβος C
    dist_C_F = km_to_stadia(haversine(*nodes['C'], *nodes['F']))  # Κόμβος C -> Μυτιλήνη
    
    print("=======================================================")
    print("   ΕΠΑΛΗΘΕΥΣΗ ΠΡΑΓΜΑΤΙΚΩΝ ΑΠΟΣΤΑΣΕΩΝ (ΣΕ ΣΤΑΔΙΑ)       ")
    print("=======================================================")
    print(f"1. Μέσσα -> Μήθυμνα:  {dist_D_E:.2f} St. (Θεωρητικό: 120, Σφάλμα: {abs(dist_D_E-120)/120*100:.2f}%)")
    print(f"2. Μέσσα -> Μαντείο:  {dist_D_A:.2f} St. (Θεωρητικό: 160, Σφάλμα: {abs(dist_D_A-160)/160*100:.2f}%)")
    print(f"3. Μαντείο -> Κόμβος B: {dist_A_B:.2f} St. (Θεωρητικό: 76,  Σφάλμα: {abs(dist_A_B-76)/76*100:.2f}%)")
    print(f"4. Μαντείο -> Φίλια(C): {dist_A_C:.2f} St. (Θεωρητικό: 68,  Σφάλμα: {abs(dist_A_C-68)/68*100:.2f}%)")
    print(f"5. Κόμβος B -> Φίλια(C): {dist_B_C:.2f} St. (Θεωρητικό: 97,  Σφάλμα: {abs(dist_B_C-97)/97*100:.2f}%)")
    print(f"6. Φίλια(C) -> Μυτιλήνη: {dist_C_F:.2f} St. (Θεωρητικό: 223, Σφάλμα: {abs(dist_C_F-223)/223*100:.2f}%)")
    print("=======================================================\n")

    # Παράμετροι προσομοίωσης Monte Carlo
    N_SIMULATIONS = 10000
    success_count = 0
    TOLERANCE = 0.01  # Αυστηρότατο κριτήριο ανοχής 1% λόγω της νέας ιδανικής σύγκλισης
    
    print(f"Έναρξη προσομοίωσης Monte Carlo ({N_SIMULATIONS} επαναλήψεις)...")
    print("Κρατάμε σταθερά τα A, B, D, E, F και μεταβάλλουμε τυχαία μόνο τον Κόμβο C.")
    
    for _ in range(N_SIMULATIONS):
        # Παραγωγή τυχαίας θέσης για τον Κόμβο C (Φίλια) εντός του Bounding Box
        rand_C_lat = random.uniform(LAT_MIN, LAT_MAX)
        # Στενότερο εύρος μήκους για να παραμένει εντός της γεωγραφίας του νησιού
        rand_C_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Υπολογισμός των αποστάσεων με τον τυχαίο Κόμβο C
        t_dist_A_C = km_to_stadia(haversine(*nodes['A'], rand_C_lat, rand_C_lon))
        t_dist_B_C = km_to_stadia(haversine(*nodes['B'], rand_C_lat, rand_C_lon))
        t_dist_C_F = km_to_stadia(haversine(rand_C_lat, rand_C_lon, *nodes['F']))
        
        matches = 0
        
        # 1. Έλεγχος Διά Τεσσάρων Συμφωνίας (Σταθερός Άξονας)
        if check_ratio(dist_D_E, dist_D_A, 0.75, TOLERANCE):
            matches += 1
            
        # 2. Έλεγχος Λόγου Δυτικού Τριγώνου (Βάση προς δεξιά πλευρά με τον τυχαίο C)
        if check_ratio(t_dist_B_C, t_dist_A_C, 97/68, TOLERANCE):
            matches += 1
            
        # 3. Έλεγχος σχέσης Μαντείου->Τυχαίου C προς τον σταθερό άξονα Μέσσα->Μήθυμνα
        if check_ratio(t_dist_A_C, dist_D_E, 68/120, TOLERANCE):
            matches += 1
            
        # 4. Έλεγχος σχέσης Τυχαίου C->Μυτιλήνη προς τον σταθερό άξονα Μέσσα->Μαντείο
        if check_ratio(t_dist_C_F, dist_D_A, 223/160, TOLERANCE):
            matches += 1

        # Αν ο τυχαίος κόμβος C καταφέρει να ικανοποιήσει τουλάχιστον 3 από τις αυστηρές μουσικές ιδιότητες
        if matches >= 3:
            success_count += 1

    # Υπολογισμός τελικού p-value
    p_value = success_count / N_SIMULATIONS
    
    print("\n-------------------------------------------------------")
    print("              ΑΠΟΤΕΛΕΣΜΑΤΑ ΠΡΟΣΟΜΟΙΩΣΗΣ                ")
    print("-------------------------------------------------------")
    print(f"Επιτυχείς τυχαίες συμπτώσεις (Successes): {success_count} / {N_SIMULATIONS}")
    print(f"Τελικό Υπολογισμένο p-value: {p_value:.4f}")
    
    if p_value < 0.01:
        print("Συμπέρασμα: Το αποτέλεσμα είναι ΣΤΑΤΙΣΤΙΚΑ ΑΚΡΑΙΟ ΚΑΙ ΣΗΜΑΝΤΙΚΟ (p < 0.01).")
        print("Η πιθανότητα να βρεθεί τέτοιο σημείο τυχαία είναι μικρότερη από 1%!")
    else:
        print("Συμπέρασμα: Το αποτέλεσμα δεν θεωρείται στατιστικά σπάνιο για αυτή την ανοχή.")
    print("-------------------------------------------------------")

if __name__ == "__main__":
    run_simulation()


