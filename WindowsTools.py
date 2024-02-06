import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image

# Function to convert a directory path to a dictionary structure
def directory_to_dict(path):
    name = os.path.basename(path)
    if os.path.isdir(path):
        return {name: [directory_to_dict(os.path.join(path, name)) for name in os.listdir(path)]}
    else:
        return name

# Function to browse for a folder
def browse_button(input_field):
    filename = filedialog.askdirectory()
    input_field.delete(0, 'end')
    input_field.insert('end', filename)

# Function to print the directory structure
def print_hierarchy(input_field, output_text):
    directory = input_field.get()
    structure = directory_to_dict(directory)
    struc_json_string = json.dumps(structure, indent=4)

    output_text.delete(1.0, 'end')
    output_text.insert('end', struc_json_string)

# Function to resize images
def resize_images(input_dir, output_dir, size, output_text):
    for file in os.listdir(input_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, file)
            img = Image.open(image_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            img.save(os.path.join(output_dir, file))
    
    output_text.insert('end', "\nResize Complete")

# Function to flip images
def flip_images(input_dir, output_dir, output_text):
    for file in os.listdir(input_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, file)
            img = Image.open(image_path)
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            img.save(os.path.join(output_dir, os.path.splitext(file)[0] + "_FL.png"))
    
    output_text.insert('end', "\nFlip Complete")

# Function to copy text to clipboard
def copy_to_clipboard(output_text, root):
    root.clipboard_clear()
    root.clipboard_append(output_text.get(1.0, 'end'))


def split_image_grid(input_dir, output_dir, grid_size, output_text):
    for file in os.listdir(input_dir):
        if file.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(input_dir, file)
            img = Image.open(image_path)
            img_width, img_height = img.size

            # Calculate the number of grid boxes
            x_boxes = img_width // grid_size
            y_boxes = img_height // grid_size

            # Split the image into boxes and save them
            for i in range(y_boxes):
                for j in range(x_boxes):
                    box = (j * grid_size, i * grid_size, (j + 1) * grid_size, (i + 1) * grid_size)
                    grid_img = img.crop(box)
                    grid_img.save(os.path.join(output_dir, f"{os.path.splitext(file)[0]}_{i}_{j}.png"))

    output_text.insert('end', "\nImage Grid Split Complete")

# Main window
root = tk.Tk()
root.title("File Hierarchy and Image Resizer")
root.configure(bg='yellow')
d_font = ('Comic Sans MS', 11, 'bold')

# Create the tab control
tab_control = ttk.Notebook(root)

# First tab (File Hierarchy Printer)
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='File Hierarchy Printer')
tab_control.pack(expand=1, fill="both")

# Second tab (Image Resizer)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Image Resizer')
tab_control.pack(expand=1, fill="both")

# Third tab (Image Grid Splitter)
tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Image Grid Splitter')
tab_control.pack(expand=1, fill="both")

# File Hierarchy Printer Components
input_path_field_1 = tk.StringVar()
tk.Label(tab1, text="Path: ", bg='yellow', font=d_font).pack()
input_path_entry_1 = tk.Entry(tab1, textvariable=input_path_field_1, width=80)
input_path_entry_1.pack(fill='x')
browse_btn_1 = tk.Button(tab1, text="Browse", command=lambda: browse_button(input_path_entry_1), bg='black', fg='white', font=d_font)
browse_btn_1.pack()
print_btn_1 = tk.Button(tab1, text="Print", command=lambda: print_hierarchy(input_path_entry_1, output_text_1), bg='black', fg='white', font=d_font)
print_btn_1.pack()
output_text_1 = ScrolledText(tab1, wrap='word')
output_text_1.pack(fill='both', expand=True)
copy_btn_1 = tk.Button(tab1, text="Copy Json to Clipboard", command=lambda: copy_to_clipboard(output_text_1, root), bg='black', fg='white', font=d_font)
copy_btn_1.pack()

# Image Resizer Components
input_path_field_2 = tk.StringVar()
output_path_field_2 = tk.StringVar()
tk.Label(tab2, text="Input Path: ", bg='yellow', font=d_font).pack()
input_path_entry_2 = tk.Entry(tab2, textvariable=input_path_field_2, width=80)
input_path_entry_2.pack(fill='x')
tk.Label(tab2, text="Output Path: ", bg='yellow', font=d_font).pack()
output_path_entry_2 = tk.Entry(tab2, textvariable=output_path_field_2, width=80)
output_path_entry_2.pack(fill='x')
browse_input_btn_2 = tk.Button(tab2, text="Browse Input", command=lambda: browse_button(input_path_entry_2), bg='black', fg='white', font=d_font)
browse_input_btn_2.pack()
browse_output_btn_2 = tk.Button(tab2, text="Browse Output", command=lambda: browse_button(output_path_entry_2), bg='black', fg='white', font=d_font)
browse_output_btn_2.pack()
tk.Label(tab2, text="Width: ", bg='yellow', font=d_font).pack(side='left')
width_field_2 = tk.Entry(tab2, width=10)
width_field_2.pack(side='left')
tk.Label(tab2, text="Height: ", bg='yellow', font=d_font).pack(side='left')
height_field_2 = tk.Entry(tab2, width=10)
height_field_2.pack(side='left')
resize_btn_2 = tk.Button(tab2, text="Resize Images", command=lambda: resize_images(input_path_field_2.get(), output_path_field_2.get(), (int(width_field_2.get()), int(height_field_2.get())), output_text_2), bg='black', fg='white', font=d_font)
resize_btn_2.pack()
flip_btn_2 = tk.Button(tab2, text="Flip Images", command=lambda: flip_images(input_path_field_2.get(), output_path_field_2.get(), output_text_2), bg='black', fg='white', font=d_font)
flip_btn_2.pack()
output_text_2 = ScrolledText(tab2, wrap='word')
output_text_2.pack(fill='both', expand=True)
copy_btn_2 = tk.Button(tab2, text="Copy Json to Clipboard", command=lambda: copy_to_clipboard(output_text_2, root), bg='black', fg='white', font=d_font)
copy_btn_2.pack()


# Image Grid Splitter Components
input_path_field_3 = tk.StringVar()
output_path_field_3 = tk.StringVar()
tk.Label(tab3, text="Input Path: ", bg='yellow', font=d_font).pack()
input_path_entry_3 = tk.Entry(tab3, textvariable=input_path_field_3, width=80)
input_path_entry_3.pack(fill='x')
tk.Label(tab3, text="Output Path: ", bg='yellow', font=d_font).pack()
output_path_entry_3 = tk.Entry(tab3, textvariable=output_path_field_3, width=80)
output_path_entry_3.pack(fill='x')
browse_input_btn_3 = tk.Button(tab3, text="Browse Input", command=lambda: browse_button(input_path_entry_3), bg='black', fg='white', font=d_font)
browse_input_btn_3.pack()
browse_output_btn_3 = tk.Button(tab3, text="Browse Output", command=lambda: browse_button(output_path_entry_3), bg='black', fg='white', font=d_font)
browse_output_btn_3.pack()
tk.Label(tab3, text="Grid Size (px): ", bg='yellow', font=d_font).pack(side='left')
grid_size_field_3 = tk.Entry(tab3, width=10)
grid_size_field_3.pack(side='left')
split_btn_3 = tk.Button(tab3, text="Split Image into Grid", command=lambda: split_image_grid(input_path_field_3.get(), output_path_field_3.get(), int(grid_size_field_3.get()), output_text_3), bg='black', fg='white', font=d_font)
split_btn_3.pack()
output_text_3 = ScrolledText(tab3, wrap='word')
output_text_3.pack(fill='both', expand=True)
copy_btn_3 = tk.Button(tab3, text="Copy Output to Clipboard", command=lambda: copy_to_clipboard(output_text_3, root), bg='black', fg='white', font=d_font)
copy_btn_3.pack()

root.mainloop()

