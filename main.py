from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_letters = [random.choice(letters) for n in range(nr_letters)]
    password_symbols = [random.choice(symbols) for n in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for n in range(nr_numbers)]
    password_list = password_numbers + password_symbols + password_letters

    random.shuffle(password_list)

    password = ""
    for char in password_list:
      password += char

    if len(password_entry.get()) >0:
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)
    else:
        password_entry.insert(0, password)
        pyperclip.copy(password)

# ---------------------------- SEARCH BUTTON ------------------------------- #
def find_password():
    try:
        data = open("saved_data.json", "r")
        info = json.load(data)
        tite = info[web_entry.get()]
        messagebox.showinfo(title= web_entry.get(), message= f"Email: {tite['email']}\nPassword: {tite['password']}")
    except FileNotFoundError:
        messagebox.showerror(message= "There is no data at all, please enter info first")
    except KeyError:
        messagebox.showerror(message="The name of the website does not exist")
    finally:
        data.close()
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {
        web_entry.get(): {
            "email": email_entry.get(),
            "password": password_entry.get()
        }
    }
    is_ok = messagebox.askokcancel(title=web_entry.get(), message= f"These are the details entered: \nEmail: {email_entry.get()} \nPassword: {password_entry.get()} \nis it ok to save?")
    if is_ok and (password_entry.get() == "" or web_entry.get() == "" or email_entry.get() == ""):
        messagebox.showwarning(title= "Error!", message= "hey! don't leave any of the fields empty")
    elif is_ok:
        try:
            with open("saved_data.json", "r") as data_file:
                jdata = json.load(data_file)
                jdata.update(new_data)
            with open("saved_data.json", "w") as data_file:
                json.dump(jdata, data_file, indent = 4 )
                web_entry.delete(0 , END)
                email_entry.delete(0 , END)
                password_entry.delete(0 , END)
        except FileNotFoundError:
            with open("saved_data.json", "w") as data_file:
                json.dump(new_data, data_file, indent = 4 )
                web_entry.delete(0 , END)
                email_entry.delete(0 , END)
                password_entry.delete(0 , END)
        data_file.close()



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
canvas = Canvas(width = 200, height =200)
window.config(padx = 50, pady = 50)
image = PhotoImage(file = "logo.png")
canvas.create_image(100, 100, image = image)
canvas.grid(column = 1, row = 0)

web_label = Label(text = "Website", font = "bold")
web_label.grid(column = 0, row = 1)

web_entry = Entry(width = 32)
web_entry.focus()
web_entry.grid(column = 1, row = 1)

email_label = Label(text = "Email / Username", font = "bold")
email_label.grid(column = 0, row = 2)

email_entry = Entry(width = 50)
email_entry.grid(column = 1, row = 2, columnspan = 2)

password_label = Label(text = "Password :", font= "bold")
password_label.grid(column = 0, row = 3)

password_entry = Entry(width = 32)
password_entry.grid(column = 1, row = 3)

password_button = Button(text = "Generate Passeord", command= generate_password)
password_button.grid(column = 2, row = 3)

add_button = Button(text = "Add", width = 44, command= save)
add_button.grid(column = 1, row = 4, columnspan = 2)

search_button = Button(text = "Search", width = 14, command= find_password)
search_button.grid(column = 2, row = 1)
window.mainloop()