
import csv
import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext, StringVar
import webbrowser

# Function to load health data from a CSV file
def load_health_data(file_path):
    health_data = {}
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            symptom = row['symptom'].strip().lower()
            health_data[symptom] = {
                "diagnosis": row['diagnosis'].strip(),
                "treatment": row['treatment'].strip(),
                "causes": [cause.strip() for cause in row['causes'].split(';')]
            }
    return health_data

# Function to diagnose based on multiple symptoms
def health_diagnosis(symptoms, health_data):
    symptoms = [symptom.strip().lower() for symptom in symptoms.split(',')]
    diagnosis_result = ""
    for symptom in symptoms:
        diagnosis_info = health_data.get(symptom, None)
        if diagnosis_info:
            diagnosis_result += f"\nSymptom: {symptom.capitalize()}\n"
            diagnosis_result += f"  Diagnosis: {diagnosis_info['diagnosis']}\n"
            diagnosis_result += f"  Treatment: {diagnosis_info['treatment']}\n"
            diagnosis_result += f"  Probable Causes: {', '.join(diagnosis_info['causes'])}\n"
        else:
            diagnosis_result += f"\nSymptom: {symptom.capitalize()}\n"
            diagnosis_result += "  Diagnosis: Symptom not recognized. Please consult a healthcare professional.\n"
    return diagnosis_result

# Function to save patient data to a CSV file
def save_patient_data(data):
    with open('patient_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Function to handle diagnosis button click and log search
def on_diagnose_click():
    symptoms = entry.get()
    if not symptoms:
        messagebox.showwarning("Input Error", "Please enter at least one symptom.")
        return
    result = health_diagnosis(symptoms, health_data)
    
    # Save to search log
    with open('search_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([symptoms, result])
    
    text_result.config(state=tk.NORMAL)
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, result)
    text_result.config(state=tk.DISABLED)

# Function to open patient registration form
def open_register_patient():
    register_window = Toplevel(root)
    register_window.title("Register Patient")
    
    fields = {
        "Patient Name": StringVar(),
        "Age": StringVar(),
        "Sex": StringVar(),
        "Height": StringVar(),
        "Previously Diagnosed Diseases": StringVar(),
        "Currently Diagnosed Disease": StringVar(),
        "Symptoms": StringVar(),
        "Family History": StringVar()
    }
    
    for idx, (label_text, var) in enumerate(fields.items()):
        label = tk.Label(register_window, text=label_text, font=("Arial", 10))
        label.grid(row=idx, column=0, padx=5, pady=5)
        entry = tk.Entry(register_window, textvariable=var, width=40)
        entry.grid(row=idx, column=1, padx=5, pady=5)

    def on_save_data():
        data = [var.get() for var in fields.values()]
        if not all(data):
            messagebox.showwarning("Incomplete Data", "Please fill out all fields before saving.")
        else:
            save_patient_data(data)
            messagebox.showinfo("Data Saved", "Patient data saved successfully.")
            for var in fields.values():
                var.set("")

    def on_clear_all():
        for var in fields.values():
            var.set("")

    save_button = tk.Button(register_window, text="Save Data", command=on_save_data, bg="#008000", fg="white", font=("Arial", 10, "bold"))
    save_button.grid(row=len(fields), column=0, padx=5, pady=10)
    
    clear_button = tk.Button(register_window, text="Clear All", command=on_clear_all, bg="#978803", fg="white", font=("Arial", 10, "bold"))
    clear_button.grid(row=len(fields), column=1, padx=5, pady=10)

# Function to search and display patient's medical history
def search_patient_history():
    search_window = Toplevel(root)
    search_window.title("Search Patient History")
    
    search_label = tk.Label(search_window, text="Enter Patient Name:", font=("Arial", 10))
    search_label.grid(row=0, column=0, padx=5, pady=5)
    
    search_entry = tk.Entry(search_window, width=40)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    
    result_text = scrolledtext.ScrolledText(search_window, width=80, height=20, font=("Arial", 10))
    result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def on_search():
        name = search_entry.get().strip().lower()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a patient name to search.")
            return
        
        found = False
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)

        try:
            with open('patient_history.csv', mode='r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0].strip().lower() == name:
                        result_text.insert(tk.END, f"Patient Name: {row[0]}\n")
                        result_text.insert(tk.END, f"Age: {row[1]}\n")
                        result_text.insert(tk.END, f"Sex: {row[2]}\n")
                        result_text.insert(tk.END, f"Height: {row[3]}\n")
                        result_text.insert(tk.END, f"Previously Diagnosed Diseases: {row[4]}\n")
                        result_text.insert(tk.END, f"Currently Diagnosed Disease: {row[5]}\n")
                        result_text.insert(tk.END, f"Symptoms: {row[6]}\n")
                        result_text.insert(tk.END, f"Family History: {row[7]}\n\n")
                        found = True
                        break
            if not found:
                result_text.insert(tk.END, "No records found for this patient.")
        except FileNotFoundError:
            result_text.insert(tk.END, "No patient history file found.")
        
        result_text.config(state=tk.DISABLED)

    search_button = tk.Button(search_window, text="Search", command=on_search, bg="#4682b4", fg="white", font=("Arial", 10, "bold"))
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

# Function to open video tutorial link
def open_video_tutorial():
    webbrowser.open("https://www.youtube.com/watch?app=desktop&v=Plse2FOkV4Q")

# Function to open article link
def open_article_link():
    webbrowser.open("https://ncvbdc.mohfw.gov.in/index4.php?lang=1&level=0&linkid=407&lid=3683")

# Function to view search log
def view_search_log():
    log_window = Toplevel(root)
    log_window.title("Search Log")
    
    log_text = scrolledtext.ScrolledText(log_window, width=80, height=100, font=("Arial", 10))
    log_text.pack(padx=10, pady=10)

    try:
        with open('search_log.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                log_text.insert(tk.END, f"Search: {row[0]}\nResult: {row[1]}\n\n")
    except FileNotFoundError:
        log_text.insert(tk.END, "No search log file found.")

# Load the health data from the CSV file
file_path = 'health_data.csv'
health_data = load_health_data(file_path)

# Create the main application window
root = tk.Tk()
root.title("Interactive Health Diagnosis System")
root.configure(bg="#f0f8ff")

label = tk.Label(root, text="Enter your symptoms (comma-separated):", bg="#f0f8ff", fg="#00008b", font=("Arial", 12))
label.pack(pady=10)

entry = tk.Entry(root, width=50, font=("Arial", 12), bg="#f8f8ff", fg="#2f4f4f", bd=2)
entry.pack(pady=5)

# Custom colors for each button
button_colors = {
    "Diagnose": "#FF4500",
    "View Search Log": "#4682B4",
    "Register a Patient": "#039719",
    "Patient's Medical History": "#039719",
    "Video Tutorial to Identify Disease": "#110bd8",
    "Articles Regarding the Diseases": "#110bd8"
}

# Function to create hover effect for buttons
def on_enter(e):
    e.widget['background'] = '#2f4f4f'
    e.widget['foreground'] = 'white'

def on_leave(e):
    button_text = e.widget['text']
    e.widget['background'] = button_colors.get(button_text, "#4682b4")
    e.widget['foreground'] = 'white'

# Create button frame for upper buttons
frame1 = tk.Frame(root, bg="#f0f8ff")
frame1.pack(pady=5)

# Upper buttons
def create_button(text, command, frame):
    button = tk.Button(frame, text=text, command=command, bg=button_colors[text], fg="white", font=("Arial", 12, "bold"), bd=3)
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)
    button.pack(side=tk.LEFT, padx=5)

create_button("Diagnose", on_diagnose_click, frame1)
create_button("View Search Log", view_search_log, frame1)

# Output text area
text_result = tk.Text(root, height=20, width=50, state=tk.DISABLED, font=("Arial", 12), bg="#fafad2", fg="#556b2f", bd=2)
text_result.pack(pady=10)

# Lower button frame for additional buttons
frame2 = tk.Frame(root, bg="#f0f8ff")
frame2.pack(pady=5)
frame3 = tk.Frame(root, bg="#f0f8ff")
frame3.pack(pady=5)

# Lower buttons
create_button("Register a Patient", open_register_patient, frame2)
create_button("Patient's Medical History", search_patient_history, frame2)
create_button("Video Tutorial to Identify Disease", open_video_tutorial, frame3)
create_button("Articles Regarding the Diseases", open_article_link, frame3)

for widget in root.winfo_children():
    widget.pack_configure(padx=10)

root.mainloop()
