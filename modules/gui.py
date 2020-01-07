###############################################################################
# Module: gui.py
# Purpose: GUI interface for inputting tags in Shadow_Backup
# Written by James Gaither
# www.jamesgaither.com
###############################################################################

# Import Base Modules
from PIL import Image, ImageTk
import tkinter as tk

# Import Custom Modules
from .dbhandler import dbhandler


class gui(object):

    def __init__(self, db_path):

        # Build initial DB connections
        self.db = dbhandler(db_path)
        self.notag_query = self.db.notag_query()

        # Set variables
        self.photoid_list = self.notag_query[0]
        self.untagged_photo = self.notag_query[1]
        self.untagged_photo_count = len(self.untagged_photo)
        self.photo_number = 0

        # Build the display window
        self.window = tk.Tk()
        self.window.geometry(f'950x{self.window.winfo_screenheight()}')
        self.window.title("Shadow Backup Tag Editor")
        self.window.config(background='#303030')
        self.back_button = tk.Button(text="<<", fg='white', command=lambda:
                                     self.change_photo('back'), width=49,
                                     height=2, activebackground='#424242',
                                     activeforeground='white', bg='#424242')
        self.back_button.grid(row=0, column=0, sticky='W')

        self.input_button = tk.Button(text="Insert",
                                      command=self.insert_tag, height=2,
                                      background='#424242', fg='white')
        self.input_button.grid(row=4, column=3, sticky='S')

        self.fwd_button = tk.Button(text=">>", fg='white', command=lambda:
                                    self.change_photo('forward'), width=49,
                                    height=2, activebackground='#424242',
                                    activeforeground='white', bg='#424242')
        self.fwd_button.grid(row=0, column=1, sticky='E')

        self.tag_input = tk.Text(self.window, width=25, height=2,
                                 background='#424242')
        self.tag_input.grid(row=4, column=2, sticky='S')

        self.delete_photo = tk.Button(text="Delete Photo", height=2,
                                      background='#424242', fg='white')
        self.delete_photo.grid(row=1, column=2, columnspan=2, sticky='new')

    def insert_tag(self):
        if self.tag_input.get('1.0', 'end'):
            for tag in self.tag_input.get('1.0', 'end').split():
                tag_id = self.db.insert_tag(tag)
                self.db.insert_phototag(self.photoid_list[self.photo_number],
                                        tag_id)
        self.tag_input.delete('1.0', 'end')
        if self.photo_number < (self.untagged_photo_count - 1):
            self.change_photo('forward')

    def change_photo(self, direction):
        if direction == 'forward':
            self.photo_number += 1
        elif direction == "back":
            self.photo_number -= 1
        else:
            print('unknown direction')
            return
        imgLabel.grid_forget()
        self.photo_display()

    def photo_display(self):
        global imgLabel

        # Adjust the directional button states depending on photo location

        if self.photo_number >= (self.untagged_photo_count - 1):
            self.fwd_button.config(state='disabled')
        else:
            self.fwd_button.config(state='active')
        if self.photo_number <= 0:
            self.back_button.config(state='disabled')
        else:
            self.back_button.config(state='active')

        # Adjust image to a smaller size for display
        img = Image.open(self.untagged_photo[self.photo_number])
        image_width, image_height = img.size
        img_ratio = image_height / image_width
        new_img_width = 700
        new_img_height = int(new_img_width * img_ratio)
        if new_img_height > self.window.winfo_screenheight():
            new_img_height = self.window.winfo_screenheight() - 80
        img = img.resize((new_img_width, new_img_height),
                         Image.ANTIALIAS)
        small_img = ImageTk.PhotoImage(img)

        # Build and display the image in a label
        imgLabel = tk.Label(self.window, image=small_img)
        imgLabel.image = small_img
        imgLabel.grid(row=1, column=0, columnspan=2, rowspan=4, sticky='NWSE')

        # Display Photo name
        photo_name = self.db.pull_name(self.photoid_list[self.photo_number])
        photo_name_label = tk.Label(self.window, text=photo_name,
                                    background='#424242', anchor='w',
                                    relief="sunk", fg='white')
        photo_name_label.grid(row=0, column=2, columnspan=2, sticky='NWSE')

        # Display all known tags. Not in use for now.

        # tag_label = tk.Label(window, text=tags, background='#424242',
        #                     anchor='nw',borderwidth=2, relief="sunk",
        #                     fg='white')
        # tag_label.grid(row=1, column=2, columnspan=2, sticky='NWSE')


# Start up display
if __name__ == "__main__":
    gui = gui()
    gui.photo_display()
    gui.window.mainloop()
