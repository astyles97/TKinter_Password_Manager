import random
import tkinter as tk
from tkinter import messagebox
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
              'y', 'z', '!', '@', '#', '$', '&', '%', '?', ':', ';', "*",
              "+", "_", "=", '-', ',', '.', '/', '[', ']']


def generate_password():
    """Makes a 12 character password of random characters also randomly capitalized. Adds generated password to entry
    field"""
    random_password = []
    for character in range(0, 17):
        selected_characters = random.choice(characters)
        random_password.append(
            ''.join(random.choice((str.upper, str.lower))(character) for character in selected_characters))
    password_entry.insert(0, "".join([str(item) for item in random_password]))
    pyperclip.copy(password_entry.get())

# ---------------------------- SAVE PASSWORD ------------------------------- #
# pull information from entries ( f"{}" )


def save():
    """adds the password from the entry field to the password list"""
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    pw_dict = {
         website: {
                    "email": email,
                    "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Field Missing", message="A field has been left empty")
    else:
        try:
            with open("receipts.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("receipts.json", "w") as file:
                json.dump(pw_dict, file, indent=4)
        else:
            data.update(pw_dict)
            with open("receipts.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)


def find_password():
    website = website_entry.get()
    with open("receipts.json") as file:
        data = json.load(file)
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Search", message=f"Website:{website} \n Email: {email} \n Password: {password}")
        elif website not in data:
            messagebox.showinfo(title="Not Found", message="This entry has not been saved.")

# ---------------------------- UI SETUP ------------------------------- #


window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white", highlightthickness=0)

canvas = tk.Canvas(width=200, height=200, bg="white", highlightthickness=0)
logo_png = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(column=1, row=0)

website_label = tk.Label(text="Website:", bg="white", fg="black")
website_label.grid(column=0, row=1)

website_entry = tk.Entry(bg="white", fg="black", highlightcolor="light grey", highlightthickness=1, width=25)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_label = tk.Label(text="Email/Username:", bg="white", fg="black")
email_label.grid(column=0, row=2)

email_entry = tk.Entry(bg="white", fg="black", highlightcolor="light grey", highlightthickness=1, width=35)
email_entry.insert(0, "astyles@protonmail.com")
email_entry.grid(column=1, row=2, columnspan=2)

password_label = tk.Label(text="Password:", bg="white", fg="black")
password_label.grid(column=0, row=3)

password_entry = tk.Entry(bg="white", fg="black", highlightcolor="light grey", highlightthickness=1, width=25)
password_entry.grid(column=1, row=3)

search_button = tk.Button(text="Search", bg="white", fg="black", command=find_password)
search_button.grid(column=2, row=1)

generate_button = tk.Button(text="Generate", bg="white", fg="black", highlightthickness=0, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = tk.Button(text="add", bg="white", fg="black", highlightthickness=0, width=32, command=save)
add_button.grid(column=1, row=4, columnspan=2)




window.mainloop()
