# Tkinter testing script
# This is semi-operational

import os
from PIL import Image, ImageTk
import tkinter as tk
from pathlib import Path
count = 0
all_pics = []
image_path = Path(r"C:/Users/james.gaither/Projects/temp/photo")
for subdir, dirs, files in os.walk(image_path):
    for file in files:
        all_pics.append(os.path.join(subdir, file))


###################

# Set variables
all_pics_count = len(all_pics)
photo_number = 0

def next_photo() :
    global photo_number

    # Set up entry for window
    #if tag_input.get():     #Non-operational
    #    print("input=", tag_input.get())
    tag_input = tk.Entry(width = 60)
    tag_input.grid(row = 2, column = 0)
    # Handle photo-side of display
    img = Image.open(all_pics[photo_number])
    img = img.resize((250,250), Image.ANTIALIAS)
    small_img = ImageTk.PhotoImage(img)
    imgLabel = tk.Label(window, image=small_img)
    imgLabel.image = small_img
    imgLabel.grid(row = 1, column = 0)
    photo_number += 1


window = tk.Tk()
window.title("Tag Editor")
#top_frame = tk.Frame(window).pack(side = "top")
#bottom_frame = tk.Frame(window).pack(side = "bottom")
tk.Label(text = "Insert your tags seperated by a space", 
          fg = "white", bg = "green").grid(row = 0, column = 0, columnspan = 2,
          sticky="W")
tk.Button(text = "insert", command = next_photo).grid(row = 2, column = 1)
next_photo()
window.mainloop()
