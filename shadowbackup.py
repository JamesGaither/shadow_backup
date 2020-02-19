###############################################################################
# Module: shadowbackup.py
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
                    help="pull photo based on tags given, requires -t arg")
parser.add_argument("-t", "--tags", nargs='+',
                    help="list of tags to either pull photos or to insert with"
                    " option -p")
parser.add_argument("-e", "--exclude", nargs='+',
                    help="list of tags to exclude when pulling photos")
args = parser.parse_args()

# Verify at lease one argument is given
if not any(vars(args).values()):
    parser.error('Must provide at least 1 argument')

# Pull Config info
config = configparser.ConfigParser()
config.read('config/main.ini')
base_path = Path(config['PATH']['base_path'])
p_in = os.path.join(base_path, Path(config['PATH']['p_in']))
p_storage = os.path.join(base_path, Path(config['PATH']['p_storage']))
db_p_storage = Path(config['PATH']['p_storage'])
results_path = os.path.join(base_path, Path(config['PATH']['results']))
db_path = os.path.join(base_path, Path(config['GENERAL']['db_path']))
work_folder = os.path.join(base_path, Path(config['PATH']['work_folder']))
reject_path = os.path.join(base_path, Path(config['PATH']['reject']))
sevenz_path = Path(config['ARCHIVE']['sevenz_path'])
vol_size = config['ARCHIVE']['vol_size']
archive_pw = config['ARCHIVE']['password']
archive_out = Path(config['ARCHIVE']['output'])


db = dbhandler(db_path)
valid_extensions = ['.cr2', '.jpg', '.jpeg', '.png']
archive_name = "1"
allpics = []


def reject(file):
    '''Moves a file that is rejected to the rejected path'''
    if not os.path.exists(reject_path):
        os.makedirs(reject_path)
    shutil.move(file, reject_path)


# Pulls a date taken from photo (if any)
def get_date_taken(path):
    f = open(path, 'rb')
    exif_tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
    exif_datetag = exif_tags['EXIF DateTimeOriginal']
    return str(exif_datetag)


# Pulls pictures in from input folder and processes them
def process():
    for subdir, dirs, files in os.walk(p_in):
        for file in files:
            allpics.append(os.path.join(subdir, file))
    for pic in allpics:
        original_name, extension = os.path.splitext(pic)
        extension = extension.lower()
        if extension not in valid_extensions:
            if args.verbose:
                print(f"{pic} does not have a valid photo extension")
            reject(pic)
            continue

        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()
        # #new_name = hash + extension.lower()

        # Check if picture has been processed
        hashcheck = db.hashcheck(hash)
        if hashcheck:
            if args.verbose:
                print(f"{pic} has already been processed with photo ID:"
                      f"{hashcheck}")
            reject(pic)
            continue

        try:
            date_taken = datetime.strptime(get_date_taken(pic),
                                           '%Y:%m:%d %H:%M:%S')
            sub_filepath = os.path.join(db_p_storage,
                                        datetime.strftime(date_taken, '%Y'),
                                        datetime.strftime(date_taken, '%m'),
                                        datetime.strftime(date_taken, '%d'))
        except Exception as e:
            if args.verbose:
                print(f"Error raised on import of EXIF tag for {pic}")
                print(f"Error: {e}")
            date_taken = None
            sub_filepath = os.path.join(db_p_storage, 'nodate')

        # Write updates to DB
        filepath = os.path.join(base_path, sub_filepath)
        filepath_id = db.insert_filepath(sub_filepath)
        photo_id, new_name = db.insert_photo(extension, hash, date_taken,
                                             filepath_id)
        if args.tags:
            tag_list = args.tags
            for tag in tag_list:
                tag_id = db.insert_tag(tag)
                db.insert_phototag(photo_id, tag_id)
        # Handle the filesystem side of the photo
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if args.verbose:
            print(f"Moving {pic} to {os.path.join(filepath,new_name)}")
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
                               archive_fullpath, work_folder))
    subprocess.run(archive_command)
    for subdir, dirs, file in os.walk(work_folder):
        for archive_picture in file:
            db.insert_archive(archive_picture, str(archive_fullpath))


# Pull a photo to a given directory given a list of tags
def pull_photo():
    if not args.tags:
        parser.error("The --pullphoto argument requires the -t argument "
                     "followed by at least one tag to search")

    tag_list = args.tags
    exclude_tags = args.exclude
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    results = db.pull_photo(tag_list, exclude_tags)
    print(f"Search yielded {len(results)} results")
    for i in results:
        shutil.copy(i, results_path)


if __name__ == '__main__':
    if args.process:
        process()
    if args.archive:
        archive()
    if args.inserttags:
        gui = gui(db_path, base_path)
        gui.photo_display()
        gui.window.mainloop()
    if args.pullphoto:
        pull_photo()
