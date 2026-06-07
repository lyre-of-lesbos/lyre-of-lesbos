import math
import random

# 1. Σταθεροί Κόμβοι (WGS84)
fixed_nodes = {
    'A': (39.253118, 25.969156),  # Μαντείο Ορφέα
    'D': (39.196404, 26.305275),  # Ιερό των Μέσσων
    'E': (39.368500, 26.174800),  # Αρχαία Μήθυμνα
    'F': (39.111200, 26.562300)   # Ακρόπολη Μυτιλήνης
}

# 2. Γεωγραφικό Πλαίσιο Λέσβου για την παραγωγή τυχαίων σημείων
# Ορίζουμε ένα ορθογώνιο που περιλαμβάνει το νησί
LAT_MIN, LAT_MAX = 39.000000, 39.400000
LON_MIN, LON_MAX = 25.800000, 26.600000

STADIO_KM = 0.1775  # 1 Πυθικό Στάδιο = 177.5 μέτρα
TOLERANCE = 0.01    # Αυστηρή ανοχή σφάλματος 1% (όπως στη μελέτη)

# Στόχοι αποστάσεων σε στάδια για τους μεταβλητούς άξονες (Μοντέλο Σκοτεινό Βουνό)
TARGETS = {
    'AB': 60,   # Μαντείο -> Ερεσός
    'BC': 122,  # Ερεσός -> Φίλια
    'CF': 217,  # Φίλια -> Μυτιλήνη
    'AC': 90    # Μαντείο -> Φίλια
}

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def run_monte_carlo(iterations=10000):
    successful_attempts = 0
    
    print(f"Έναρξη Προσομοίωσης Monte Carlo με {iterations:,} επαναλήψεις...")
    
    for i in range(iterations):
        # Παραγωγή τυχαίας θέσης για τον Κόμβο Β (Ερεσός)
        b_lat = random.uniform(LAT_MIN, LAT_MAX)
        b_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Παραγωγή τυχαίας θέσης για τον Κόμβο C (Φίλια)
        c_lat = random.uniform(LAT_MIN, LAT_MAX)
        c_lon = random.uniform(LON_MIN, LON_MAX)
        
        # Υπολογισμός των 4 μεταβλητών αποστάσεων σε στάδια
        dist_AB = haversine_distance(fixed_nodes['A'][0], fixed_nodes['A'][1], b_lat, b_lon) / STADIO_KM
        dist_BC = haversine_distance(b_lat, b_lon, c_lat, c_lon) / STADIO_KM
        dist_CF = haversine_distance(c_lat, c_lon, fixed_nodes['F'][0], fixed_nodes['F'][1]) / STADIO_KM
        dist_AC = haversine_distance(fixed_nodes['A'][0], fixed_nodes['A'][1], c_lat, c_lon) / STADIO_KM
        
        # Έλεγχος αν οι τυχαίες αποστάσεις πέφτουν μέσα στο όριο ανοχής (±1%) των στόχων
        check_AB = abs(dist_AB - TARGETS['AB']) / TARGETS['AB'] <= TOLERANCE
        check_BC = abs(dist_BC - TARGETS['BC']) / TARGETS['BC'] <= TOLERANCE
        check_CF = abs(dist_CF - TARGETS['CF']) / TARGETS['CF'] <= TOLERANCE
        check_AC = abs(dist_AC - TARGETS['AC']) / TARGETS['AC'] <= TOLERANCE
        
        # Αν ΚΑΙ οι 4 άξονες "κλειδώσουν" ταυτόχρονα στις σωστές αναλογίες
        if check_AB and check_BC and check_CF and check_AC:
            successful_attempts += 1
            
        # Οπτική πρόοδος ανά 25% των επαναλήψεων
        if (i + 1) % (iterations // 4) == 0:
            print(f"Πρόοδος: {((i + 1) / iterations) * 100:.0f}% ολοκληρώθηκε...")

    # Υπολογισμός της τιμής p-value
    p_value = successful_attempts / iterations
    
    print("\n" + "="*50)
    print("ΑΠΟΤΕΛΕΣΜΑΤΑ ΠΡΟΣΟΜΟΙΩΣΗΣ")
    print("="*50)
    print(f"Συνολικές Προσπάθειες: {iterations:,}")
    print(f"Επιτυχείς Συμπτώσεις: {successful_attempts}")
    print(f"Στατιστική Πιθανότητα (p-value): {p_value:.6f}")
    
    if p_value < 0.01:
        print("Συμπέρασμα: Η διάταξη είναι ΕΞΑΙΡΕΤΙΚΑ ΣΠΑΝΙΑ (p < 0.01).")
        print("Η πιθανότητα να προκύψει αυτό το σχήμα στην τύχη είναι πρακτικά μηδενική.")
    else:
        print("Συμπέρασμα: Το σχήμα θα μπορούσε να είναι τυχαίο.")

# Εκτέλεση της προσομοίωσης
if __name__ == "__main__":
    # Ξεκινάμε με 10.000 για ταχύτητα. Μπορείς να το αυξήσεις σε 100.000 ή 1.000.000
    run_monte_carlo(iterations=10000)
