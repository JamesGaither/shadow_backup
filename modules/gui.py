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


def previous_photo():
    global photo_number
    if photo_number == 0:
        print("end of que")
        return
    photo_number -= 1
    photo_display()


def insert_tag():
    if tag_input.get():
        print("input=", tag_input.get())
    tag_input.delete(0, 'end')
    next_photo()


def next_photo():
    global untagged_photo_count
    global photo_number
    if photo_number == (untagged_photo_count - 1):
        print("end of que")
        return
    photo_number += 1
    photo_display()


def photo_display():
    global photo_number
    img = Image.open(untagged_photo[photo_number])
    img = img.resize((300, 300), Image.ANTIALIAS)
    small_img = ImageTk.PhotoImage(img)
    imgLabel = tk.Label(window, image=small_img)
    imgLabel.image = small_img
    imgLabel.grid(row=0, column=0)


window = tk.Tk()
window.title("Shadow Backup Tag Editor")
tk.Button(text="Previous", command=previous_photo).grid(row=2, column=1)
tk.Button(text="Insert", command=insert_tag).grid(row=2, column=2)
tk.Button(text="Next", command=next_photo).grid(row=2, column=3)
tag_input = tk.Entry(width=50)
tag_input.grid(row=2, column=0)
photo_display()
window.mainloop()
