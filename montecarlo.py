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
    """Μετατροπή χιλιομέτρων σε Αιολικά Στάδια (1 Στάδιο = 177 μέτρα)"""
    return (km * 1000.0) / 177.0

def check_ratio(val1, val2, target_ratio, tolerance=0.01):
    """Έλεγχος αν ο λόγος δύο τιμών προσεγγίζει έναν στόχο εντός αυστηρού ορίου ανοχής"""
    if val2 == 0:
        return False
    current_ratio = val1 / val2
    return abs(current_ratio - target_ratio) / target_ratio <= tolerance

def run_simulation():
    # --- ΟΛΟΙ ΟΙ ΣΤΑΘΕΡΟΙ ΚΟΜΒΟΙ (Βάσει του μοντέλου των 177μ) ---
    nodes = {
        'A': (39.253118, 25.969156),  # Μαντείο Ορφέα
        'B': (39.141500, 25.922100),  # Κόμβος Β (Βέλτιστη Θέση 177μ)
        'C': (39.213100, 26.113200),  # Κόμβος C (Βέλτιστη Θέση Φίλιας 177μ)
        'D': (39.196404, 26.305275),  # Ιερό των Μέσσων
        'E': (39.368500, 26.174800),  # Αρχαία Μήθυμνα
        'F': (39.111200, 26.562300)   # Ακρόπολη Μυτιλήνης
    }
    
    # --- ΓΕΩΓΡΑΦΙΚΟ ΠΛΑΙΣΙΟ ΛΕΣΒΟΥ (Bounding Box για τον Monte Carlo έλεγχο) ---
    LAT_MIN, LAT_MAX = 39.05, 39.40
    LON_MIN, LON_MAX = 25.85, 26.65
    
    # Υπολογισμός πραγματικών αποστάσεων των κλειδωμένων αξόνων (σε Αιολικά Στάδια)
    dist_D_E = km_to_stadia(haversine(*nodes['D'], *nodes['E']))  # Μέσσα -> Μήθυμνα
    dist_D_A = km_to_stadia(haversine(*nodes['D'], *nodes['A']))  # Μέσσα -> Μαντείο
    dist_A_B = km_to_stadia(haversine(*nodes['A'], *nodes['B']))  # Μαντείο -> Κόμβος B
    dist_A_C = km_to_stadia(haversine(*nodes['A'], *nodes['C']))  # Μαντείο -> Κόμβος C
    dist_B_C = km_to_stadia(haversine(*nodes['B'], *nodes['C']))  # Κόμβος B -> Κόμβος C
    dist_C_F = km_to_stadia(haversine(*nodes['C'], *nodes['F']))  # Κόμβος C -> Μυτιλήνη
    
    print("=======================================================")
    print("   ΕΠΑΛΗΘΕΥΣΗ ΠΡΑΓΜΑΤΙΚΩΝ ΑΠΟΣΤΑΣΕΩΝ (ΑΙΟΛΙΚΑ ΣΤΑΔΙΑ)   ")
    print("=======================================================")
    print(f"1. Μέσσα -> Μήθυμνα:  {dist_D_E:.2f} St. (Θεωρητικό: 125, Σφάλμα: {abs(dist_D_E-125)/125*100:.2f}%)")
    print(f"2. Μέσσα -> Μαντείο:  {dist_D_A:.2f} St. (Θεωρητικό: 168, Σφάλμα: {abs(dist_D_A-168)/168*100:.2f}%)")
    print(f"3. Μαντείο -> Κόμβος B: {dist_A_B:.2f} St. (Θεωρητικό: 80,  Σφάλμα: {abs(dist_A_B-80)/80*100:.2f}%)")
    print(f"4. Μαντείο -> Φίλια(C): {dist_A_C:.2f} St. (Θεωρητικό: 71,  Σφάλμα: {abs(dist_A_C-71)/71*100:.2f}%)")
    print(f"5. Κόμβος B -> Φίλια(C): {dist_B_C:.2f} St. (Θεωρητικό: 101, Σφάλμα: {abs(dist_B_C-101)/101*100:.2f}%)")
    print(f"6. Φίλια(C) -> Μυτιλήνη: {dist_C_F:.2f} St. (Θεωρητικό: 228, Σφάλμα: {abs(dist_C_F-228)/228*100:.2f}%)")
    print("=======================================================\n")

    # Παράμετροι προσομοίωσης Monte Carlo
    N_SIMULATIONS = 10000
    success_count = 0
    TOLERANCE = 0.01  # Αυστηρό κριτήριο ανοχής 1%
    
    print(f"Έναρξη προσομοίωσης Monte Carlo ({N_SIMULATIONS} επαναλήψεις)...")
    print("Κρατάμε σταθερά τα A, D, E, F και μεταβάλλουμε τυχαία τους ενδιάμεσους κόμβους B και C.")
    
    for _ in range(N_SIMULATIONS):
        # Παραγωγή τυχαίων θέσεων για τους κόμβους B και C εντός του Bounding Box
        rand_B_lat = random.uniform(LAT_MIN, LAT_MAX)
        rand_B_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Τυχαίος Κόμβος C (Φίλια)
        rand_C_lat = random.uniform(LAT_MIN, LAT_MAX)
        rand_C_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Υπολογισμός των νέων αποστάσεων με τα τυχαία σημεία
        t_dist_A_B = km_to_stadia(haversine(*nodes['A'], rand_B_lat, rand_B_lon))
        t_dist_A_C = km_to_stadia(haversine(*nodes['A'], rand_C_lat, rand_C_lon))
        t_dist_B_C = km_to_stadia(haversine(rand_B_lat, rand_B_lon, rand_C_lat, rand_C_lon))
        t_dist_C_F = km_to_stadia(haversine(rand_C_lat, rand_C_lon, *nodes['F']))
        
        matches = 0
        
        # 1. Εναρμόνιος Λόγος Κεντρικού Άξονα (Σταθερός)
        if check_ratio(dist_D_E, dist_D_A, 125/168, TOLERANCE):
            matches += 1
            
        # 2. Έλεγχος πλευράς Μαντείο -> Τυχαίο B
        if check_ratio(t_dist_A_B, dist_D_E, 80/125, TOLERANCE):
            matches += 1
            
        # 3. Έλεγχος πλευράς Μαντείο -> Τυχαίο C
        if check_ratio(t_dist_A_C, dist_D_E, 71/125, TOLERANCE):
            matches += 1
            
        # 4. Έλεγχος τυχαίας Βάσης B -> C
        if check_ratio(t_dist_B_C, dist_D_E, 101/125, TOLERANCE):
            matches += 1
            
        # 5. Έλεγχος τυχαίας απόστασης C -> Μυτιλήνη
        if check_ratio(t_dist_C_F, dist_D_A, 228/168, TOLERANCE):
            matches += 1

        # Αν η τυχαία γεωμετρία καταφέρει να ικανοποιήσει τουλάχιστον 4 από τις εναρμόνιες ιδιότητες
        if matches >= 4:
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
        print("Η πιθανότητα να προκύψει αυτή η εναρμόνια Λύρα στην τύχη είναι μικρότερη από 1%!")
    else:
        print("Συμπέρασμα: Το αποτέλεσμα δεν θεωρείται στατιστικά σπάνιο για αυτή την ανοχή.")
    print("-------------------------------------------------------")

if __name__ == "__main__":
    run_simulation()

