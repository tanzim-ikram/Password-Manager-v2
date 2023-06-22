# Day-30: Project- Password Manager (Improved Version)
import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        except json.decoder.JSONDecodeError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            # Updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as password_file:
            password = json.load(password_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in password:
            email = password[website]["email"]
            password = password[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
            pyperclip.copy(password)
            messagebox.showinfo(title="Attention!!", message="Password copied to clipboard!")
        else:
            messagebox.showinfo(title=website, message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
# Website Label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
# Email Label
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
# Password Label
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
# Website Entry
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()
# Email Entry
email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "tanzim.ikram@gmail.com")
# Password Entry
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

# Buttons
# Search Button
search_button = Button(text="Search", width=14, highlightthickness=0, command=find_password)
search_button.grid(column=2, row=1)
# Generate Password Button
password_button = Button(text="Generate Password", width=14, highlightthickness=0, command=generate_password)
password_button.grid(column=2, row=3)
# Add Button
add_button = Button(text="Add", width=43, highlightthickness=0, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
