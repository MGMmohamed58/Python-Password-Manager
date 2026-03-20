import json
from tkinter import *
from tkinter import messagebox
import password  # Custom module for password generation

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_new_password():
    """Generates a random password and inserts it into the password entry."""
    random_password = password.generate()
    password_entry.delete(0, END)
    password_entry.insert(0, random_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get().lower()
    email = email_entry.get()
    pwd = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": pwd,
        }
    }

    if not website or not pwd or not email:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            # 1. Try to open and read existing data
            with open("data.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # 2. If file doesn't exist OR is empty/corrupt, use new_data as the base
            data = new_data
        else:
            # 3. If reading was successful, update the dictionary
            data.update(new_data)
        finally:
            # 4. In ALL cases, save the updated dictionary back to the file
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)

            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()

# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_data():
    website = website_entry.get().lower()

    if not website:
        messagebox.showerror(title="Oops", message="Please don't leave the website field empty!")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            messagebox.showerror(title="Error" , message= "This website is not saved")
        else:
            # If reading was successful
            if website in data:
                new_data = (data[website])
                messagebox.showinfo(title="Info" , message= f"Email : {new_data["email"]}\nPassword : {new_data["password"]} ")
            else:
                messagebox.showerror(title="Error" , message= "This website is not saved")
        finally:
            # 4. In ALL cases
            website_entry.focus()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# ------ LOGO ------ #
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# ------ LABELS ------ #
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# ------ ENTRIES ------ #
website_entry = Entry(width=32)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=32)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "example@gmail.com")  # Default email

password_entry = Entry(width=32)
password_entry.grid(row=3, column=1 ,columnspan = 2)

# ------ BUTTONS ------ #
generate_btn = Button(text="Generate Password", command=generate_new_password)
generate_btn.grid(row=3, column=3)

add_btn = Button(text="Add", width=36, command=save_data)
add_btn.grid(row=4, column=1, columnspan=2 , pady= 20)

search_btn = Button(text="Search", width = 12, command=search_data)
search_btn.grid(row=1, column=3)

window.mainloop()