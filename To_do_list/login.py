import sqlite3
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import to_do_list

root = Tk()   
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

# SQLite connection
def create_table():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                    username TEXT PRIMARY KEY, 
                    password TEXT
                )''')
    conn.commit()
    conn.close()

# Function to handle Sign In
def signin():
    username = user.get()
    password = code.get()

    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    stored_password = cursor.fetchone()
    conn.close()

    if stored_password and password == stored_password[0]:
        root.withdraw()  # Close the login window
        to_do_list.open_todo_list(username)
    else: 
        messagebox.showerror("Invalid", "Invalid username or password")
    return

# Sign up window
def signup_command():
    window = Toplevel(root)
    window.title("Sign up")
    window.geometry('925x500+300+200')
    window.configure(bg = "#fff")
    window.resizable(False, False)

    def signup():
        username = user.get()
        password = code.get()
        confirm_password = confirm_code.get()

        if password == confirm_password:
            window.withdraw()
            try:
                conn = sqlite3.connect('user_data.db')
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username=?", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Username already exists")
                else:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                    conn.commit()
                    messagebox.showinfo("Signup", "Successfully signed up")
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error occurred: {e}")
        else:
            messagebox.showerror("Invalid", "Passwords do not match")

    def sign():
        window.destroy()

    img = Image.open("SignUp.jpg")
    img = ImageTk.PhotoImage(img)
    Label(window, image=img, border=0, bg= "white").place(x= 50, y =90)

    frame = Frame(window, width= 350, height=390, bg='#fff')
    frame.place(x=480,y=50)

    heading = Label(frame, text='Sign Up', fg="#57a1f8", bg="white", font=("Microsoft Yahei UI Light", 23, "bold"))
    heading.place(x=100, y=5)

    # Username Entry
    def on_enter_user(e):
        if user.get() == "Username":
            user.delete(0, 'end')
    def on_leave_user(e):
        if user.get() == "":
            user.insert(0, "Username")
    user = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 11))
    user.place(x=30, y=80)
    user.insert(0, "Username")
    user.bind("<FocusIn>",on_enter_user)
    user.bind("<FocusOut>", on_leave_user)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

    # Password Entry
    def on_enter_password(e):
        if code.get() == "Password":
            code.delete(0, 'end')
            code.config(show="*") 

    def on_leave_password(e):
        if code.get() == "":
            code.insert(0, "Password")
            code.config(show="") 

    code = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 11))
    code.place(x=30, y=150)
    code.insert(0, "Password")
    code.bind("<FocusIn>", on_enter_password)
    code.bind("<FocusOut>", on_leave_password)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

    # Confirm Password Entry
    def on_enter_confirm(e):
        if confirm_code.get() == "Confirm Password":
            confirm_code.delete(0, 'end')
            confirm_code.config(show="*")

    def on_leave_confirm(e):
        if confirm_code.get() == " ":
            confirm_code.insert(0, "Confirm Password")
    confirm_code = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft Yahei UI Light", 11))
    confirm_code.place(x=30, y=220)
    confirm_code.insert(0, "Confirm Password")
    confirm_code.bind("<FocusIn>",on_enter_confirm)
    confirm_code.bind("<FocusOut>", on_leave_confirm)

    Frame(frame, width=295, height=2, bg='black').place(x=25, y=247)

    Button(frame, width=39, pady=7, text="Sign up", bg="#57a1f8", fg="white", border=0, command=signup).place(x=35, y=280)
    label= Label(frame, text = "I have an account", fg="black", bg="white", font= ("Microsoft YaHei UI Light", 9))
    label.place(x=90, y=340)

    signin = Button(frame, width=6, text="Sign in", border=0, bg= "white", cursor="hand2", fg='#57a1f8', command=sign)
    signin.place(x=200, y=340)
    window.mainloop()

# Main Login UI
img = PhotoImage(file='login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg= 'white')
frame.place(x=480, y=70)

heading = Label(frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Username Entry
def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name = user.get()
    if name=="":
        user.insert(0, 'Username')
user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Password Entry
def on_enter(e):
    code.delete(0, 'end')
    code.config(show="*") 

def on_leave(e):
    name = code.get()
    if name=="": 
        code.insert(0, 'Password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light',11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text="Sign in", bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light',9))
label.place(x=75, y = 270)

sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup_command)
sign_up.place(x=215, y = 270)

# Create table if it doesn't exist
create_table()

root.mainloop()
