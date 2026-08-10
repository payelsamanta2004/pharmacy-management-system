import tkinter as tk
from tkinter import messagebox
import gui


def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "admin" and password == "1234":
        messagebox.showinfo(
            "Login Success",
            "Welcome to Pharmacy Management System"
        )

        login_window.destroy()
        gui.open_gui()

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid Username or Password"
        )


login_window = tk.Tk()
login_window.title("Pharmacy Login")
login_window.geometry("400x300")


tk.Label(
    login_window,
    text="🏥 Pharmacy Login",
    font=("Arial", 20, "bold")
).pack(pady=20)


tk.Label(
    login_window,
    text="Username"
).pack()

username_entry = tk.Entry(login_window)
username_entry.pack()


tk.Label(
    login_window,
    text="Password"
).pack()

password_entry = tk.Entry(
    login_window,
    show="*"
)
password_entry.pack()


tk.Button(
    login_window,
    text="Login",
    width=15,
    bg="green",
    fg="white",
    command=login
).pack(pady=20)


login_window.mainloop()