import csv

# Function to read the CSV file and load health data into a list of dictionaries
def load_health_data(file_path):
    health_data = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            health_data.append(row)
    return health_data

# Function to search for a matching diagnosis based on input symptoms
def get_diagnosis(symptoms, health_data):
    results = []
    for data in health_data:
        # Check if all symptoms match any row in the CSV data
        if all(symptom.lower().strip() in data['Symptom'].lower() for symptom in symptoms):
            results.append({
                'Diagnosis': data['Diagnosis'],
                'Treatment': data['Treatment'],
                'Cause': data['Probable Cause']
            })
    return results
