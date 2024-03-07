import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips

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
    # input_field.delete(0, 'end')
    input_field.set(filename)

def browse_button_file(input_field_var):
    filename = filedialog.askopenfilename()  # Ask for a file instead of a directory for videos
    input_field_var.set(filename)

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

def create_grid_image(input_dir, output_dir, rows, cols, pixel_size, output_text):
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    images = [Image.open(f) for f in image_files]
    images = [img.resize((pixel_size, pixel_size), Image.Resampling.LANCZOS) for img in images]

    grid_width = cols * pixel_size
    grid_height = rows * pixel_size
    grid_image = Image.new('RGB', (grid_width, grid_height))

    for index, image in enumerate(images):
        if index >= rows * cols:
            break
        row = index // cols
        col = index % cols
        grid_image.paste(image, (col * pixel_size, row * pixel_size))

    grid_image.save(os.path.join(output_dir, 'grid_image.png'))
    output_text.insert('end', "\nGrid Image Created")

def crop_all_videos_in_folder(input_dir, output_dir, x, y, width, height, output_text):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # List all video files in the input directory
    for file in os.listdir(input_dir):
        if file.lower().endswith(".mp4"):
            input_path = os.path.join(input_dir, file)
            output_path = os.path.join(output_dir, "cropped_" + file)  # Add 'cropped_' prefix to output filename
            try:
                # Load the video file
                video = VideoFileClip(input_path)
                # Crop it
                cropped_video = video.crop(x1=x, y1=y, width=width, height=height)
                # Write the cropped video to the output directory
                cropped_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
                cropped_video.close()  # Properly close the video file to free up resources
                video.close()  # Close the original video file as well
                output_text.insert('end', f"\nVideo {file} cropped and saved to {output_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
                continue

def merge_videos_in_folder(input_dir, output_dir, output_text):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Gather all mp4 files in the input directory
    video_files = [os.path.join(input_dir, f) for f in sorted(os.listdir(input_dir)) if f.lower().endswith(".mp4")]

    # Load all videos into MoviePy VideoFileClip objects
    clips = [VideoFileClip(f) for f in video_files]

    # Concatenate all video clips
    final_clip = concatenate_videoclips(clips)

    # Define the output file path
    output_file = os.path.join(output_dir, "merged_video.mp4")

    # Write the concatenated clip to the output file
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=30)

    # Close all clips to free up resources
    for clip in clips:
        clip.close()
    final_clip.close()

    # Notify the user that the merging is complete
    output_text.insert('end', f"\nMerged video saved to {output_file}")
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

# Fourth tab (Video Cropper)
tab4 = ttk.Frame(tab_control)
tab_control.add(tab4, text='Video Cropper')
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

# Video Cropper Components
input_video_path = tk.StringVar()
output_video_path = tk.StringVar()
x_offset = tk.IntVar()
y_offset = tk.IntVar()
crop_width = tk.IntVar()
crop_height = tk.IntVar()

def browse_video_input_dir():
    dirname = filedialog.askdirectory()
    input_video_path.set(dirname)

def browse_video_output_dir():
    dirname = filedialog.askdirectory()
    output_video_path.set(dirname)

tk.Label(tab4, text="Video Path: ").pack()
input_video_entry = tk.Entry(tab4, textvariable=input_video_path, width=80).pack(fill='x')
tk.Button(tab4, text="Input Folder", command=browse_video_input_dir).pack()
tk.Label(tab4, text="Output Path: ").pack()
tk.Button(tab4, text="Output Folder", command=browse_video_output_dir).pack()
output_video_entry = tk.Entry(tab4, textvariable=output_video_path, width=80).pack(fill='x')

tk.Label(tab4, text="X Offset: ").pack()
x_offset_entry = tk.Entry(tab4, textvariable=x_offset)
x_offset_entry.pack()
tk.Label(tab4, text="Y Offset: ").pack()
y_offset_entry = tk.Entry(tab4, textvariable=y_offset)
y_offset_entry.pack()
tk.Label(tab4, text="Width: ").pack()
crop_width_entry = tk.Entry(tab4, textvariable=crop_width)
crop_width_entry.pack()
tk.Label(tab4, text="Height: ").pack()
crop_height_entry = tk.Entry(tab4, textvariable=crop_height)
crop_height_entry.pack()



def crop_videos():
    x = int(x_offset_entry.get())
    y = int(y_offset_entry.get())
    width = int(crop_width_entry.get())
    height = int(crop_height_entry.get())
    crop_all_videos_in_folder(input_video_path.get(), output_video_path.get(), x, y, width, height, output_text_4)

crop_btn = tk.Button(tab4, text="Crop Videos", command=crop_videos)
crop_btn.pack()
merge_btn = tk.Button(tab4, text="Merge Videos", command=lambda: merge_videos_in_folder(input_video_path.get(), output_video_path.get(), output_text_4))
merge_btn.pack()

output_text_4 = ScrolledText(tab4, wrap='word')
output_text_4.pack(fill='both', expand=True)

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

tk.Label(tab3, text="Rows: ", bg='yellow', font=d_font).pack(side='left')
rows_field = tk.Entry(tab3, width=10)
rows_field.pack(side='left')

tk.Label(tab3, text="Columns: ", bg='yellow', font=d_font).pack(side='left')
cols_field = tk.Entry(tab3, width=10)
cols_field.pack(side='left')

tk.Label(tab3, text="Pixel Size: ", bg='yellow', font=d_font).pack(side='left')
pixel_size_field = tk.Entry(tab3, width=10)
pixel_size_field.pack(side='left')

create_grid_btn = tk.Button(tab3, text="Create Grid Image", command=lambda: create_grid_image(input_path_field_3.get(), output_path_field_3.get(), int(rows_field.get()), int(cols_field.get()), int(pixel_size_field.get()), output_text_3), bg='black', fg='white', font=d_font)
create_grid_btn.pack()

root.mainloop()

