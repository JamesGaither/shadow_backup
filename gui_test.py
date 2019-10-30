# Tkinter testing script
# This is non-operational!!
import os
from PIL import Image, ImageTk
import tkinter as tk
from pathlib import Path

all_pics = []
image_path = Path(r"C:/Users/james.gaither/Projects/temp/photo")
for subdir, dirs, files in os.walk(image_path):
    for file in files:
        all_pics.append(os.path.join(subdir, file))

window=tk.Tk()
window.title('Input tags')
tag_input = tk.Entry(window)
button = tk.Button(window, text='Submit', width=25)
button.pack(side=tk.RIGHT)
window.mainloop()