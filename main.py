from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
from json.decoder import JSONDecodeError

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_number = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_number + password_symbol + password_letter
    shuffle(password_list)
    password = "".join(password_list)

    password_input.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():

    website = web_input.get().title()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Empty fields", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as password_data:
                # reading old data
                data = json.load(password_data)
        except FileNotFoundError:
            with open("data.json", "w") as password_data:
                json.dump(new_data, password_data, indent=4)
        except JSONDecodeError:
            with open("data.json", "w") as password_data:
                json.dump(new_data, password_data, indent=4)
        else:
            # updating old data with new
            data.update(new_data)

            with open("data.json", "w") as password_data:
                # saving updated data
                json.dump(data, password_data, indent=4)
        finally:
            web_input.delete(0, END)
            password_input.delete(0, END)

# -------------------------- FIND PASSWORD ----------------------------- #


def find_password():

    website = web_input.get().title()
    try:
        with open("data.json", "r") as password_data:
            # reading old data
            data = json.load(password_data)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found!")
    else:
        if website in data:
            messagebox.showinfo(title=f"Website: {website}", message=f"Email: {data[website.title()]['email']}\n"
                                                                     f"Password: {data[website.title()]['password']}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists!")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_png = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_png)
canvas.grid(row=0, column=1)

web_label = Label(text="Website:")
web_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

web_input = Entry(width=21)
web_input.focus()
web_input.grid(row=1, column=1)

email_input = Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2)

password_input = Entry(width=21)
password_input.grid(row=3, column=1)

password_button = Button(text="Generate Password", command=generate_password)
password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=1, column=2)


window.mainloop()