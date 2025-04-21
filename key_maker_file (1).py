import hashlib
import json
from cryptography.fernet import Fernet
from tkinter import Tk, Label, Entry, Button, filedialog
from datetime import datetime

# Define a valid Base64 key for Fernet encryption
SECRET_KEY = b'Y2hvb3NlQVN0cm9uZ0JhU2U2NEVuY3J5cHRpb25LZXk='  # Replace with the same key as in Activator
cipher = Fernet(SECRET_KEY)

def generate_activation_data(name, email, duration_days):
    """
    Generate activation data including the activation code.
    """
    issue_date = datetime.now().strftime("%Y-%m-%d")
    data = {
        "name": name,
        "email": email,
        "duration_days": duration_days,
        "issue_date": issue_date,
    }
    data_string = json.dumps(data, separators=(",", ":")) + "MySecretKey"
    activation_code = hashlib.sha256(data_string.encode()).hexdigest()[:16]
    data["activation_code"] = activation_code
    return data

def save_encrypted_file(data):
    """
    Encrypt the activation data and save it to a file.
    """
    data_json = json.dumps(data)
    encrypted_data = cipher.encrypt(data_json.encode())

    file_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key")])
    if file_path:
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        print(f"Encrypted activation file saved to {file_path}")

def on_generate():
    name = name_entry.get()
    email = email_entry.get()
    duration_days = duration_entry.get()

    if not name or not email or not duration_days.isdigit():
        result_label.config(text="Please fill all fields correctly!", fg="red")
        return

    data = generate_activation_data(name, email, int(duration_days))
    save_encrypted_file(data)
    result_label.config(text="Activation file generated and saved!", fg="green")

# Build the GUI
root = Tk()
root.title("Key Maker")

Label(root, text="Name:").grid(row=0, column=0, pady=5)
name_entry = Entry(root)
name_entry.grid(row=0, column=1, pady=5)

Label(root, text="Email:").grid(row=1, column=0, pady=5)
email_entry = Entry(root)
email_entry.grid(row=1, column=1, pady=5)

Label(root, text="Duration (Days):").grid(row=2, column=0, pady=5)
duration_entry = Entry(root)
duration_entry.grid(row=2, column=1, pady=5)

generate_button = Button(root, text="Generate & Save Activation File", command=on_generate)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

root.mainloop()