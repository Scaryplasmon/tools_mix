import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from PIL import Image

def directory_to_dict(path):
    name = os.path.basename(path)
    if os.path.isdir(path):
        return {name: [directory_to_dict(os.path.join(path, name)) for name in os.listdir(path)]}
    else:
        return name

def browse_button(is_input=True):
    filename = filedialog.askdirectory()
    if is_input:
        input_path_entry.delete(0, 'end')
        input_path_entry.insert('end', filename)
    else:
        output_path_entry.delete(0, 'end')
        output_path_entry.insert('end', filename)
    print_hierarchy()

def print_hierarchy():
    directory = input_path_field.get()
    structure = directory_to_dict(directory)
    struc_json_string = json.dumps(structure, indent=4)

    output_text.delete(1.0, 'end')
    output_text.insert('end', struc_json_string)

def resize_images():
    input_dir = input_path_field.get()
    output_dir = output_path_field.get()
    size = (int(width_field.get()), int(height_field.get()))

    for file in os.listdir(input_dir):
        if file.endswith(".png"):
            image_path = os.path.join(input_dir, file)
            img = Image.open(image_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(os.path.join(output_dir, file))

    output_text.insert('end', "\nComplete")

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, 'end'))

root = tk.Tk()
d_font = ('Comic Sans MS', 11, 'bold')

root.title("Image Resizer Tool")
root.configure(bg='yellow')

input_path_field = tk.StringVar()
output_path_field = tk.StringVar()

tk.Label(root, text="Input Path: ", bg='yellow', font=d_font).pack()
input_path_entry = tk.Entry(root, textvariable=input_path_field, width=80)
input_path_entry.pack(fill='x')

tk.Label(root, text="Output Path: ", bg='yellow', font=d_font).pack()
output_path_entry = tk.Entry(root, textvariable=output_path_field, width=80)
output_path_entry.pack(fill='x')

button_frame = tk.Frame(root, bg='yellow')
button_frame.pack(fill='x')

browse_input_btn = tk.Button(button_frame, text="Browse Input", command=lambda: browse_button(True), bg='black', fg='white', font=d_font)
browse_input_btn.pack(side='left')

browse_output_btn = tk.Button(button_frame, text="Browse Output", command=lambda: browse_button(False), bg='black', fg='white', font=d_font)
browse_output_btn.pack(side='left')

tk.Label(root, text="Width: ", bg='yellow', font=d_font).pack(side='left')
width_field = tk.Entry(root, width=10)
width_field.pack(side='left')

tk.Label(root, text="Height: ", bg='yellow', font=d_font).pack(side='left')
height_field = tk.Entry(root, width=10)
height_field.pack(side='left')

resize_btn = tk.Button(root, text="Resize Images", command=resize_images, bg='black', fg='white', font=d_font)
resize_btn.pack()

output_text = ScrolledText(root, wrap='word')
output_text.pack(fill='both', expand=True)

copy_btn = tk.Button(root, text="Copy Json to Clipboard", command=copy_to_clipboard, bg='black', fg='white', font=d_font)
copy_btn.pack()

root.mainloop()
