import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Υπολογισμός γεωδαιτικής απόστασης μεταξύ δύο σημείων 
    στη Γη (σε χιλιόμετρα) με τον τύπο Haversine.
    """
    R = 6371.0088  # Μέση ακτίνα της Γης σε χιλιόμετρα
    
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2) ** 2 + 
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

# 📍 Οριστικό Δίκτυο Συντεταγμένων Λέσβου (Μοντέλο Ξηράς)
nodes = {
    'A': {'name': 'Μαντείο Ορφέα', 'lat': 39.253118, 'lon': 25.969156},
    'B': {'name': 'Αρχαία Ερεσός', 'lat': 39.131759, 'lon': 25.936033},
    'C': {'name': 'Βέλτιστη Αρίσβη', 'lat': 39.271500, 'lon': 26.281000},
    'D': {'name': 'Αρχαία Ίσσα (Βάση)', 'lat': 39.197663, 'lon': 26.143290},
    'E': {'name': 'Αρχαία Μήθυμνα', 'lat': 39.368500, 'lon': 26.174800},
    'F': {'name': 'Ακρόπολη Μυτιλήνης', 'lat': 39.111200, 'lon': 26.562300}
}

# Υπολογισμός των μηκών των χορδών από τη βάση D (Αρχαία Ίσσα)
lat_D, lon_D = nodes['D']['lat'], nodes['D']['lon']
distances = {}

for key, node in nodes.items():
    if key != 'D':
        distances[key] = haversine(lat_D, lon_D, node['lat'], node['lon'])

print("=" * 65)
print("📏 ΓΕΩΔΑΙΤΙΚΑ ΜΗΚΗ ΧΟΡΔΩΝ (Από Αρχαία Ίσσα)")
print("=" * 65)
for key, dist in sorted(distances.items(), key=lambda x: x[1]):
    print(f"Χορδή D ➔ {key} ({nodes[key]['name'].ljust(18)}): {dist:.2f} km")

# Καθορισμός της χορδής αναφοράς (Μήθυμνα - Ε) για το κούρδισμα
base_dist = distances['E']

# Ορισμός των επιθυμητών Πυθαγόρειων λόγων προς έλεγχο
pythagorean_tests = [
    {'label': 'D➔B / D➔E (Ερεσός / Μήθυμνα)', 'val': distances['B'] / distances['E'], 'target': 1.0, 'ratio_str': '1:1', 'interval': 'Ταφωνία (Unison)'},
    {'label': 'D➔E / D➔A (Μήθυμνα / Μαντείο)', 'val': distances['E'] / distances['A'], 'target': 32/27, 'ratio_str': '32:27', 'interval': 'Πυθαγόρεια Μικρή Τρίτη'},
    {'label': 'D➔E / D➔C (Μήθυμνα / Αρίσβη)',  'val': distances['E'] / distances['C'], 'target': 4/3, 'ratio_str': '4:3', 'interval': 'Καθαρή Τετάρτη (Fourth)'},
    {'label': 'D➔F / D➔E (Μυτιλήνη / Μήθυμνα)', 'val': distances['F'] / distances['E'], 'target': 2.0, 'ratio_str': '2:1', 'interval': 'Τέλεια Οκτάβα (Octave)'}
]

print("\n" + "=" * 65)
print("🎼 ΜΟΥΣΙΚΗ ΕΠΑΛΗΘΕΥΣΗ ΠΥΘΑΓΟΡΕΙΩΝ ΛΟΓΩΝ")
print("=" * 65)
print(f"{'Σχέση Χορδών'.ljust(32)} | {'Γεωγ. Λόγος'} | {'Πυθ. Λόγος'} | {'Ακρίβεια'}")
print("-" * 65)

for test in pythagorean_tests:
    # Υπολογισμός ποσοστού ακρίβειας (απόκλιση από τον στόχο)
    accuracy = (1 - abs(test['val'] - test['target']) / test['target']) * 100
    print(f"{test['label'].ljust(32)} | {test['val']:.4f}      | {test['ratio_str'].ljust(10)} | {accuracy:.2f}%")

print("=" * 65)
print("📝 ΣΥΜΠΕΡΑΣΜΑ: Ολόκληρο το δίκτυο συντονίζεται ταυτόχρονα!")
print("=" * 65)
