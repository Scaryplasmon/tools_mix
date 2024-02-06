import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

def directory_to_dict(path):
    name = os.path.basename(path)
    if os.path.isdir(path):
        return {name: [directory_to_dict(os.path.join(path, name)) for name in os.listdir(path)]}
    else:
        return name

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()
    path_entry.delete(0, 'end')
    path_entry.insert('end', filename)
    print_hierarchy()

def print_hierarchy():
    directory = path_field.get()
    structure = directory_to_dict(directory)
    struc_json_string = json.dumps(structure, indent=4)

    output_text.delete(1.0, 'end')
    output_text.insert('end', struc_json_string)

def copy_to_clipboard():
    root.clipboard_clear()  # clear clipboard contents
    root.clipboard_append(output_text.get(1.0, 'end'))  # append new value to clipbaord

root = tk.Tk()

d_font = ('Comic Sans MS', 11, 'bold')

root.title("File Hierarchy Printer")
root.configure(bg='yellow')  # sets the background color to yellow

path_field = tk.StringVar()

tk.Label(root, text="Path: ", bg='yellow', font=d_font).pack()

path_entry = tk.Entry(root, textvariable=path_field, width=80)
path_entry.pack(fill='x')

button_frame = tk.Frame(root, bg='yellow')
button_frame.pack(fill='x')

browse_btn = tk.Button(button_frame, text="Browse", command=browse_button, bg='black', fg='white', font=d_font)
browse_btn.pack(side='left')

print_btn = tk.Button(button_frame, text="Print", command=print_hierarchy, bg='black', fg='white', font=d_font)
print_btn.pack()

output_text = ScrolledText(root, wrap='word')  # using scrolled text area
output_text.pack(fill='both', expand=True)

copy_btn = tk.Button(root, text="Copy Json to Clipboard", command=copy_to_clipboard, bg='black', fg='white', font=d_font)
copy_btn.pack()

root.mainloop()
