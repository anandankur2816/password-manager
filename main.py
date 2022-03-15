from tkinter import *
from tkinter import messagebox
import winsound
import random
import pyperclip
import json

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def gen_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    web_entry = website_entry.get()
    em_entry = email_entry.get()
    pas_entry = password_entry.get()
    new_data = {
        web_entry: {"email": em_entry, "Password": pas_entry}
    }
    if len(web_entry) == 0 or len(pas_entry) == 0 or len(em_entry) == 0:
        messagebox.askretrycancel(message="Please don't leave anything blank")
    else:
        is_ok = messagebox.askokcancel(title=website_entry.get(),
                                       message=f"These are the details that are entered User:{email_entry.get()}| "
                                               f"Pass:{password_entry.get()}")
        if is_ok:
            try:
                with open("pas.json", mode='r') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = new_data
            else:
                data.update(new_data)
            finally:
                with open("pas.json", mode='w') as file:
                    json.dump(data, file, indent=2)
                    # print(password_entry.get())
                    website_entry.delete(0, END)
                    password_entry.delete(0, END)
                    winsound.MessageBeep()
# ---------------------------- search ------------------------------- #


def search():
    msg = ""
    try:
        with open("pas.json", mode='r') as file:
            data = json.load(file)
            website = data[website_entry.get()]["email"]
            password = data[website_entry.get()]["Password"]
            msg = f"email:{website} \n password:{password}"
    except KeyError or FileNotFoundError:
        msg = "The website entry has not been recorded"
    finally:
        messagebox.showinfo(title="Info", message=msg)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=28)
website_entry.grid(row=1, column=1, columnspan=1)
website_entry.focus()
email_entry = Entry(width=53)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "anandankur2816@gmail.com")
password_entry = Entry(width=28)
password_entry.grid(row=3, column=1)

# Buttons
search_website_button = Button(text="Search", bg="Blue", width=20, command=search)
search_website_button.grid(column=2,row=1)
generate_password_button = Button(text="Generate Password", width=20, command=gen_password, bg=PINK)
generate_password_button.grid(row=3, column=2)
add_button = Button(text="Add", width=46, command=save, bg=GREEN)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
