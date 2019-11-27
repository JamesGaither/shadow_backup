# Tkinter testing script
# This is semi-operational

import os
from PIL import Image, ImageTk
import tkinter as tk
from pathlib import Path

# Import Custom Modules
from dbhandler import dbhandler
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
    if tag_input.get():     
        print("input=", tag_input.get())
    tag_input.delete(0, 'end')
    # Handle photo-side of display
    img = Image.open(all_pics[photo_number])
    img = img.resize((300,300), Image.ANTIALIAS)
    small_img = ImageTk.PhotoImage(img)
    imgLabel = tk.Label(window, image=small_img)
    imgLabel.image = small_img
    imgLabel.grid(row = 0, column = 0)
    photo_number += 1


window = tk.Tk()
window.title("Tag Editor")
tk.Button(text = "Previous").grid(row = 2, column =1)
tk.Button(text = "Insert", command = next_photo).grid(row = 2, column = 2)
tag_input = tk.Entry(width = 50)
tag_input.grid(row = 2, column = 0)
next_photo()
window.mainloop()
