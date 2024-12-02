import sqlite3
from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk

def open_todo_list(username): # username parameter
    todo_root = Toplevel()
    todo_root.title(f"{username}'s To-Do List")
    todo_root.geometry('925x650+300+100')
    todo_root.config(bg="#f7f7f7") 

    # SQLite connection setup
    def create_table():
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks(
                        username TEXT,
                        task TEXT,
                        date TEXT, 
                        completed TEXT DEFAULT 'Incomplete')''')
        conn.commit()
        conn.close()

    def load_tasks():
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute("SELECT task, date, completed FROM tasks WHERE username=?", (username,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def add_task():
        task = task_entry.get()
        date = deadline_picker.get_date()
        if task:
            conn = sqlite3.connect('todo_list.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (username, task, date) VALUES (?, ?, ?)", 
                           (username, task, date))
            conn.commit()
            conn.close()
            task_entry.delete(0, END)
            display_tasks()
        else:
            messagebox.showwarning("Warning", "You must enter a task.")

    def delete_task(task_name):
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE username=? AND task=?", (username, task_name))
        conn.commit()
        conn.close()
        display_tasks()

    def complete_task(task_name):
        conn = sqlite3.connect('todo_list.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed='Complete' WHERE username=? AND task=?", (username, task_name))
        conn.commit()
        conn.close()
        display_tasks()

    def edit_task(old_task):
        new_task = task_entry.get()
        deadline = deadline_picker.get_date()
        if new_task:
            conn = sqlite3.connect('todo_list.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE tasks SET task=?, date=? WHERE username=? AND task=?", 
                           (new_task, deadline, username, old_task))
            conn.commit()
            conn.close()
            task_entry.delete(0, END)
            display_tasks()
            reset_add_button()
        else:
            messagebox.showwarning("Warning", "You must enter a new task name.")

    def start_editing(task_name, task_deadline):
        task_entry.delete(0, END)
        task_entry.insert(0, task_name)
        deadline_picker.set_date(task_deadline)
        add_button.config(text="Save Edit", command=lambda: edit_task(task_name))

    def reset_add_button():
        add_button.config(text="Add Task", command=add_task)
    
    def display_tasks():
        for widget in task_frame.winfo_children():
            widget.destroy()

        # Add headers above the task list
        headers = ["Task", "Deadline", "Status", "Edit", "Complete", "Delete"]
        for col, header in enumerate(headers):
            header_label = Label(task_frame, text=header, font=('Arial', 12, 'bold'), width=10, anchor="w", bg="lightgray")
            header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        tasks = load_tasks()
        for index, (task, deadline, status) in enumerate(tasks, start=1):
            task_label = Label(task_frame, text=task, font=('Helvetica', 12), width=20, anchor="w")
            task_label.grid(row=index, column=0, padx=10, pady=5, sticky="w")

            deadline_label = Label(task_frame, text=deadline, font=('Helvetica', 12), width=10)
            deadline_label.grid(row=index, column=1, padx=10)

            status_label = Label(task_frame, text=status, font=('Helvetica', 12), width=10)
            if status == "Incomplete":
                status_label.config(fg="red")
            elif status == "Complete":
                status_label.config(fg="green")
            status_label.grid(row=index, column=2, padx=10)

            edit_button = Button(task_frame, text="✏️", font=("Helvetica", 10), width=4, height=1, 
                                 bg="#4CAF50", fg="white", relief="flat", command=lambda t=task, d=deadline: start_editing(t, d))
            edit_button.grid(row=index, column=3, padx=5)

            complete_button = Button(task_frame, text="✔️", font=("Helvetica", 10), width=4, height=1, 
                                     bg="#FF9800", fg="white", relief="flat", command=lambda t=task: complete_task(t))
            complete_button.grid(row=index, column=4, padx=5)

            delete_button = Button(task_frame, text="🗑️", font=("Helvetica", 10), width=4, height=1, 
                                   bg="#F44336", fg="white", relief="flat", command=lambda t=task: delete_task(t))
            delete_button.grid(row=index, column=5, padx=5)

    # UI setup
    Label(todo_root, text="To-Do List", font=("Helvetica", 24, "bold"), bg="#f7f7f7").pack(pady=20)

    # Adding an image
    img = Image.open("welcome.jpg").resize((150, 200))
    img = ImageTk.PhotoImage(img)
    img_label = Label(todo_root, image=img, bg="#f7f7f7")
    img_label.image = img  
    img_label.place(x=50, y=30)  

    # Entry, date picker, and buttons
    task_entry = Entry(todo_root, width=40, font=("Helvetica", 14), borderwidth=2, relief="solid")
    task_entry.pack(pady=10)

    Label(todo_root, text="Deadline:", font=("Helvetica", 12), bg="#f7f7f7").pack()
    deadline_picker = DateEntry(todo_root, width=12, background='darkblue', foreground='white', borderwidth=2, 
                                date_pattern="yyyy-mm-dd")
    deadline_picker.pack(pady=10)

    add_button = Button(todo_root, text="Add Task", command=add_task, font=("Helvetica", 14), bg="#4CAF50", fg="white", relief="flat")
    add_button.pack(pady=10)

    task_frame = Frame(todo_root, bg="#f7f7f7")
    task_frame.pack(pady=10)

    # Scrollable frame setup
    canvas = Canvas(todo_root)
    scroll_y = Scrollbar(todo_root, orient="vertical", command=canvas.yview)
    canvas.config(yscrollcommand=scroll_y.set)

    task_frame = Frame(canvas, bg="#f7f7f7")
    canvas.create_window((0, 0), window=task_frame, anchor="nw")
    
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scroll_y.pack(side=RIGHT, fill=Y)

    task_frame.bind(
        "<Configure>", 
        lambda e: canvas.config(scrollregion=canvas.bbox("all"))
    )

    create_table()
    display_tasks()

    todo_root.mainloop()
