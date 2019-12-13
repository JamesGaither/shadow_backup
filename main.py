###############################################################################
# Module: main.py
# Purpose: Main program of ShadowBackup. See Readme for further detail
# Written by James Gaither
# www.jamesgaither.com
###############################################################################

# Base Libraries
import os
import argparse
import configparser
import hashlib
import shutil
import exifread
import sys
from datetime import datetime
from pathlib import Path
import subprocess

# custom modules
from modules.dbhandler import dbhandler
from modules.gui import gui

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--process", action="store_true",
                    help="reads all photos for processing")
parser.add_argument("-a", "--archive", action="store_true",
                    help="pushes non-archived photos to archive")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="prints detailed information to terminal")
parser.add_argument("-i", "--inserttags", action="store_true",
                    help="activates the gui for inputting tags")
parser.add_argument("--pullphoto", action="store_true",
                    help="pull photo based on tags given")
parser.add_argument("-t", "--tags", nargs='+',
                    help="list of tags to pull with")
args = parser.parse_args()

# Pull Config info
config = configparser.ConfigParser()
config.read('config/main.ini')
p_in = Path(config['PATH']['p_in'])
p_storage = Path(config['PATH']['p_storage'])
results_path = Path(config['PATH']['results'])
db_path = Path(config['GENERAL']['db_path'])
sevenz_path = Path(config['ARCHIVE']['sevenz_path'])
vol_size = config['ARCHIVE']['vol_size']
archive_pw = config['ARCHIVE']['password']
archive_out = Path(config['ARCHIVE']['output'])
work_folder = Path(config['PATH']['work_folder'])

db = dbhandler(db_path)
valid_extensions = ['.cr2', '.jpg', '.jpeg', '.png']
archive_name = "1"   # Temp solution need to rotate
allpics = []


# Pulls a date taken from photo (if any)
def get_date_taken(path):
    f = open(path, 'rb')
    exif_tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
    exif_datetag = exif_tags['EXIF DateTimeOriginal']
    return str(exif_datetag)


# Pulls pictures in from to-process folder and processes them
def process():
    for subdir, dirs, files in os.walk(p_in):
        for file in files:
            allpics.append(os.path.join(subdir, file))
    for pic in allpics:
        original_name, extension = os.path.splitext(pic)
        if extension.lower() not in valid_extensions:
            if args.verbose:
                print(f"{pic} does not have a valid photo extension")
            continue
        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()
        new_name = hash + extension.lower()

        # Check if picture has been processed
        hashcheck = db.hashcheck(hash)
        if hashcheck:
            if args.verbose:
                print(f"{pic} has already been processed with photo ID:"
                      f"{hashcheck}")
            continue

        try:
            date_taken = datetime.strptime(get_date_taken(pic),
                                           '%Y:%m:%d %H:%M:%S')
            filepath = os.path.join(p_storage,
                                    datetime.strftime(date_taken, '%Y'),
                                    datetime.strftime(date_taken, '%m'),
                                    datetime.strftime(date_taken, '%d'))
        except Exception as e:
            if args.verbose:
                print(f"Error raised on import of EXIF tag for {pic}")
                print(f"Error: {e}")
            date_taken = None
            filepath = os.path.join(p_storage, 'nodate')

        # Write updates to DB
        filepath_id = db.insert_filepath(filepath)
        db.insert_photo(new_name, hash, date_taken, filepath_id)

        # Handle the filesystem side of the photo
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if args.verbose:
            print(f"Moving {pic} to {filepath}")
        shutil.move(pic, os.path.join(filepath, new_name))


# Push unarchived photos to archive
def archive():
    if args.verbose:
        print("Begin archiving")
    nonarchived_files = db.archive_query()
    for photo_path in nonarchived_files:
        shutil.copy(photo_path, work_folder)
    archive_fullpath = os.path.join(archive_out, archive_name)
    archive_command = (r'"{}" a -v"{}" -t7z -mhe=on -mx9 -p"{}" "{}" "{}"'
                       .format(sevenz_path, vol_size, archive_pw,
                               archive_fullpath, Path(work_folder)))
    subprocess.run(archive_command)
    for subdir, dirs, file in os.walk(work_folder):
        for archive_picture in file:
            db.insert_archive(archive_picture, str(archive_fullpath))


# Pull a photo to a given directory given a lsit of tags
def pull_photo():
    if not args.tags:
        sys.exit("Must specify tags to search using argument \"-t\" followed "
                 "by at least one tag to search")
    tag_list = args.tags
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    results = db.pull_photo(tag_list)
    print(f"Search yielded {len(results)} results")
    for i in results:
        shutil.copy(i, results_path)


if __name__ == '__main__':
    if args.process:
        process()
    if args.archive:
        print("archiving has been temporarily disabled")
        # archive()
    if args.inserttags:
        gui = gui(db_path)
        gui.photo_display()
        gui.window.mainloop()

    # Testing pull photos
    if args.pullphoto:
        pull_photo()
