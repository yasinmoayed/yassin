import hashlib
import json
from cryptography.fernet import Fernet
from tkinter import Tk, Button, filedialog, messagebox
from datetime import datetime, timedelta

# Define a valid Base64 key for Fernet encryption
SECRET_KEY = b'Y2hvb3NlQVN0cm9uZ0JhU2U2NEVuY3J5cHRpb25LZXk='  # Replace with your valid Fernet key
cipher = Fernet(SECRET_KEY)

def load_encrypted_file(file_path):
    """
    Load and decrypt the encrypted file.
    """
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return json.loads(decrypted_data)

def validate_activation_data(data):
    """
    Validate the activation data.
    """
    data_string = json.dumps({
        "name": data["name"],
        "email": data["email"],
        "duration_days": data["duration_days"],
        "issue_date": data["issue_date"],
    }, separators=(",", ":")) + "MySecretKey"
    expected_code = hashlib.sha256(data_string.encode()).hexdigest()[:16]

    if data["activation_code"] != expected_code:
        return False, "Invalid activation code!"

    # Check expiration date
    issue_date = datetime.strptime(data["issue_date"], "%Y-%m-%d")
    expiration_date = issue_date + timedelta(days=data["duration_days"])
    if datetime.now() > expiration_date:
        return False, "Activation code has expired!"

    return True, "Activation successful!"

def on_activate():
    file_path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return

    try:
        data = load_encrypted_file(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {str(e)}")
        return

    valid, message = validate_activation_data(data)
    if valid:
        messagebox.showinfo("Success", message)
        root.destroy()  # Close the window and proceed with the main program
    else:
        messagebox.showerror("Error", message)

# Build the GUI
root = Tk()
root.title("Activator")

activate_button = Button(root, text="Activate", command=on_activate)
activate_button.pack(pady=20)

root.mainloop()