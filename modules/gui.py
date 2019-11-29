# Tkinter testing script
# This is semi-operational
# Only can edit pictures in the DB already??

from PIL import Image, ImageTk
import tkinter as tk

# Import Custom Modules
from dbhandler import dbhandler

# Scan DB for any non-tagged photos and return them
db = dbhandler('C:/Users/james.gaither/Projects/temp/photo/testing_1.db')
untagged_photo = db.notag_query()

# Set variables
untagged_photo_count = len(untagged_photo)
photo_number = 0


def next_photo():
    global photo_number

    # Handle entry and clear
    if tag_input.get():     
        print("input=", tag_input.get())
    tag_input.delete(0, 'end')

    # Handle photo-side of display
    img = Image.open(untagged_photo[photo_number])
    img = img.resize((300, 300), Image.ANTIALIAS)
    small_img = ImageTk.PhotoImage(img)
    imgLabel = tk.Label(window, image=small_img)
    imgLabel.image = small_img
    imgLabel.grid(row=0, column=0)
    photo_number += 1


window = tk.Tk()
window.title("Shadow Backup Tag Editor")
tk.Button(text="Previous").grid(row=2, column=1)
tk.Button(text="Insert", command=next_photo).grid(row=2, column=2)
tag_input = tk.Entry(width=50)
tag_input.grid(row=2, column=0)
next_photo()
window.mainloop()
