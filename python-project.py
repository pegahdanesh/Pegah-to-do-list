from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from datetime import datetime
import os
import webbrowser  # To open GitHub link in the browser

root = Tk()
root.title('Pegah To-Do List')
root.geometry("600x700")
root.config(bg="#ffe6f0")  # Set a pastel pink background

# Define a decorative Font
my_font = Font(
    family="Brush Script MT",  # Girlish, curvy font
    size=24,
    weight='bold')

# Create a Frame
my_frame = Frame(root, bg="#ffe6f0")
my_frame.pack(pady=20)

# Create Listbox with soft colors
my_list = Listbox(my_frame,
                  font=my_font,
                  width=35,  # Adjust width for timestamp display
                  height=6,
                  background="#fff0f6",  # Light pink
                  foreground="#663399",  # Soft purple text
                  borderwidth=3,
                  highlightthickness=0,
                  selectbackground="#ffb6c1",  # Lighter pink for selection
                  activestyle="none")
my_list.pack(side=LEFT, fill=BOTH)

# Create a scrollbar for the listbox
my_scrollbar = Scrollbar(my_frame)
my_scrollbar.pack(side=RIGHT, fill=Y)

# Add scrollbar to listbox
my_list.config(yscrollcommand=my_scrollbar.set)
my_scrollbar.config(command=my_list.yview)

# Frame for search box and search button
search_frame = Frame(root, bg="#ffe6f0")
search_frame.pack(pady=10)

# Search entry box (same size as the task entry box)
search_entry = Entry(search_frame, font=("Comic Sans MS", 18), width=24, borderwidth=3, fg="#663399")  # No placeholder text
search_entry.grid(row=0, column=0, padx=(0, 5))

# Add search button
search_button = ttk.Button(search_frame, text="🔍 Search", command=lambda: search_item(), style="TButton")
search_button.grid(row=0, column=1)

# Frame for entry and Add button
entry_frame = Frame(root, bg="#ffe6f0")
entry_frame.pack(pady=10)

# Entry box for adding new tasks (same size as the search box)
my_entry = Entry(entry_frame, font=("Comic Sans MS", 18), width=24, borderwidth=3, fg="#663399")
my_entry.grid(row=0, column=0, padx=(0, 5))

# Add button placed next to the entry box
add_button = ttk.Button(entry_frame, text="➕ Add", command=lambda: add_item(), style="TButton")
add_button.grid(row=0, column=1)

# Button Frame for organizing other buttons
button_frame = Frame(root, bg="#ffe6f0")
button_frame.pack(pady=20)

# Initialize a list to store tasks with their timestamps
tasks_with_time = []

# File to save tasks
task_file = "tasks.txt"

# Functions (delete, add, cross, uncross, delete crossed, search, clear)
def delete_item():
    selected_task_index = my_list.curselection()[0]
    my_list.delete(ANCHOR)
    tasks_with_time.pop(selected_task_index)

def add_item():
    if my_entry.get() != "":
        task = my_entry.get()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tasks_with_time.append((task, timestamp))  # Store task with timestamp
        my_entry.delete(0, END)
        update_task_list()

def update_task_list():
    # Sort tasks by timestamp to ensure chronological order
    tasks_with_time.sort(key=lambda x: x[1])
    # Clear the Listbox and add tasks back in the sorted order
    my_list.delete(0, END)
    for task, time in tasks_with_time:
        my_list.insert(END, f"{task} ({time})")

def cross_off_item():
    my_list.itemconfig(my_list.curselection(), foreground="#dedede")
    my_list.select_clear(0, END)

def uncross_item():
    my_list.itemconfig(my_list.curselection(), foreground="#663399")
    my_list.select_clear(0, END)

def delete_crossed_items():
    count = 0
    while count < my_list.size():
        if my_list.itemcget(count, "foreground") == "#dedede":
            my_list.delete(count)
            tasks_with_time.pop(count)  # Remove the corresponding task
        else:
            count += 1

def search_item():
    search_term = search_entry.get().lower()
    for i in range(my_list.size()):
        task_info = my_list.get(i).lower()
        if search_term in task_info:
            my_list.selection_clear(0, END)
            my_list.selection_set(i)
            my_list.see(i)
            return

# Save tasks to a file
def save_tasks():
    with open(task_file, "w") as f:
        for task, time in tasks_with_time:
            f.write(f"{task}|{time}\n")
    print("Tasks saved to file.")

# Clear stored tasks
def clear_tasks():
    global tasks_with_time
    tasks_with_time = []  # Clear the list
    my_list.delete(0, END)  # Clear the listbox
    if os.path.exists(task_file):
        os.remove(task_file)  # Remove the file
    print("Stored tasks cleared.")

# Load tasks from file (if exists)
def load_tasks():
    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            for line in f.readlines():
                task, time = line.strip().split("|")
                tasks_with_time.append((task, time))
        update_task_list()

# Create a more girlish style for buttons
style = ttk.Style()
style.configure("TButton", font=("Comic Sans MS", 12), padding=6, relief="flat", background="#f4c2c2", borderwidth=0)
style.map("TButton", background=[("active", "#ffb6c1")])

# Modern buttons with girly colors
delete_button = ttk.Button(button_frame, text="🗑️Delete", command=delete_item, style="TButton")
cross_off_button = ttk.Button(button_frame, text="✔️ Cross Off", command=cross_off_item, style="TButton")
uncross_button = ttk.Button(button_frame, text="↩️ Uncross", command=uncross_item, style="TButton")
delete_crossed_button = ttk.Button(button_frame, text="❌ Delete Crossed", command=delete_crossed_items, style="TButton")
clear_button = ttk.Button(button_frame, text="🧹 Clear Tasks", command=clear_tasks, style="TButton")  # Clear button added
save_button = ttk.Button(button_frame, text="💾 Save", command=save_tasks, style="TButton")  # Save button added

# Arrange buttons in two rows with spacing and padding
clear_button.grid(row=0, column=0, padx=10, pady=10)  # Clear button placed on top
delete_button.grid(row=0, column=1, padx=10, pady=10)
cross_off_button.grid(row=0, column=2, padx=10, pady=10)
uncross_button.grid(row=1, column=0, padx=10, pady=10)
delete_crossed_button.grid(row=1, column=1, padx=10, pady=10)
save_button.grid(row=1, column=2, padx=10, pady=10)  # Save button arranged below

# Load existing tasks from file when the app starts
load_tasks()

# Function to display About Me information in a new window
def show_about_me():
    # Create a new window
    about_me_window = Toplevel(root)
    about_me_window.title("About Me")
    about_me_window.geometry("400x300")
    about_me_window.config(bg="#ffe6f0")

    # Add information text
    info_label = Label(about_me_window, text="Pegah Danesh\nBiomedical Engineering Student", font=("Comic Sans MS", 16), bg="#ffe6f0", fg="#663399")
    info_label.pack(pady=20)

    # Add GitHub link as a button
    github_button = Button(about_me_window, text="Visit my GitHub", font=("Comic Sans MS", 14), bg="#ffb6c1", fg="#663399", command=lambda: webbrowser.open("https://github.com/pegahdanesh"))
    github_button.pack(pady=10)

# Add the About Me button to the button frame
about_me_button = ttk.Button(button_frame, text="👤 About Me", command=show_about_me, style="TButton")
about_me_button.grid(row=2, column=1, padx=10, pady=10)  # Positioned in the bottom center

root.mainloop()
