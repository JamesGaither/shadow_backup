# Tkinter testing script
# This is semi-operational
# Only can edit pictures in the DB already??

from PIL import Image, ImageTk
import tkinter as tk

# Import Custom Modules
from dbhandler import dbhandler

# Scan DB for any non-tagged photos and return them
db = dbhandler('C:/Users/james.gaither/Projects/temp/photo/testing_1.db')

# Todo: a better method?
notag_query = db.notag_query()
photoid_list = notag_query[0]
untagged_photo = notag_query[1]

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
    global photo_number
    if tag_input.get():
        print(type(tag_input.get()))
        for tag in tag_input.get().split():
            tag_id = db.insert_tag(tag)
            db.insert_phototag(photoid_list[photo_number], tag_id)
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

    # Adjust image to a smaller size for display
    img = Image.open(untagged_photo[photo_number])
    image_width, image_height = img.size
    img_ratio = image_width / image_height
    print(img_ratio)
    new_img_height = 500
    img = img.resize((int(new_img_height * img_ratio), new_img_height),
                     Image.ANTIALIAS)
    small_img = ImageTk.PhotoImage(img)

    # Build and display the image in a label
    imgLabel = tk.Label(window, image=small_img)
    imgLabel.image = small_img
    imgLabel.grid(row=0, column=0)

    # Display known tags
    tags = "testtag1 testtag2 testag3"
    tag_label = tk.Label(window, text=tags)
    tag_label.grid(row=1, column=1, sticky="N")


window = tk.Tk()
window.title("Shadow Backup Tag Editor")
tk.Button(text="Previous", command=previous_photo).grid(row=2, column=1)
tk.Button(text="Insert", command=insert_tag).grid(row=2, column=2)
tk.Button(text="Next", command=next_photo).grid(row=2, column=3)
tag_input = tk.Entry(width=50)
tag_input.grid(row=2, column=0)

# Start up display
# window.wm_attributes("-topmost", 1)
photo_display()
window.mainloop()
