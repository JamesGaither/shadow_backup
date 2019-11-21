# Tkinter testing script
# This is non-operational!!
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


print(all_pics[0])
def load_next_image():
    count += 1
    image = Image.open(all_pics[count])
    photo = ImageTk.PhotoImage(image)

    label.configure(image=photo)
#    label = Label(window, image=photo)
 #   label.image = photo
  #  label.pack()

image = Image.open(all_pics[count])
photo = ImageTk.PhotoImage(image)
label = Label(window, image=photo)
label.image = photo
label.pack()

labelframe = LabelFrame(window)
labelframe.pack(fill="both", expand="yes")
left = Label(labelframe)

button=Button(labelframe, padx = 5, pady = 5, text="Next",command = Click)
button.pack(side = RIGHT)

R1 = Radiobutton(labelframe, text="Choice 1", value=1)
R1.pack(side = LEFT)

R2 = Radiobutton(labelframe, text="Choice 2",  value=2)
R2.pack(side = LEFT)


left.pack()
window.mainloop()