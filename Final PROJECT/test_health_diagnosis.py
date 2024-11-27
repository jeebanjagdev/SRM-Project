import unittest
from health_diagnosis import load_health_data, get_diagnosis

class TestHealthDiagnosisSystem(unittest.TestCase):
    def setUp(self):
        # Mock data to use during testing
        self.mock_data = [
            {'Symptom': 'Fever', 'Diagnosis': 'Flu', 'Treatment': 'Rest', 'Probable Cause': 'Viral Infection'},
            {'Symptom': 'Cough', 'Diagnosis': 'Bronchitis', 'Treatment': 'Cough Syrup', 'Probable Cause': 'Bacterial Infection'}
        ]

    def test_get_diagnosis_single_symptom(self):
        symptoms = ['Fever']
        result = get_diagnosis(symptoms, self.mock_data)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Diagnosis'], 'Flu')

    def test_get_diagnosis_multiple_symptoms(self):
        symptoms = ['Cough']
        result = get_diagnosis(symptoms, self.mock_data)
        self.assertEqual(result[0]['Diagnosis'], 'Bronchitis')

    def test_no_match(self):
        symptoms = ['Headache']
        result = get_diagnosis(symptoms, self.mock_data)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
