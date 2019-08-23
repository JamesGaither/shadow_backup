# base libraries
import os
import argparse
import configparser
import datetime
import hashlib
import shutil
import exifread
from datetime import datetime
from pathlib import Path
import subprocess

# custom modules
from modules.dbhandler import dbhandler

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--process", action="store_true",
                    help="reads all photos for processing")
parser.add_argument("-a", "--archive", action="store_true",
                    help="pushes non-archived photos to archive")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="prints detailed information to terminal")
args = parser.parse_args()

# Pull Config info
config = configparser.ConfigParser()
config.read('config/main.ini')
p_in = Path(config['PATH']['p_in'])
p_storage = Path(config['PATH']['p_storage'])
db = dbhandler(Path(config['GENERAL']['db_path']))
sevenz_path = Path(config['ARCHIVE']['sevenz_path'])
vol_size = config['ARCHIVE']['vol_size']
archive_pw = config['ARCHIVE']['password']
archive_out = Path(config['ARCHIVE']['output'])
work_folder= Path(config['PATH']['work_folder'])

archive_name = "1"   #Temp solution need to rotate
allpics = []

###Build out Functions###

# Pulls a date taken from photo (if any)
def get_date_taken(path):
    f = open(path, 'rb')
    exif_tags = exifread.process_file(f, stop_tag='DateTimeOriginal')
    exif_datetag = exif_tags['EXIF DateTimeOriginal']
    print(exif_datetag)
    return str(exif_datetag)

#Pulls pictures in from to-process folder and processes them
def process():
    for subdir, dirs, files in os.walk(os.path.join(p_storage, p_in)):
        for file in files:
            allpics.append(os.path.join(subdir, file))
    for pic in allpics:
        original_name, extension = os.path.splitext(pic)
        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()
        new_name = hash + extension.lower()
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

        # Check if picture has been processed
        if db.hashcheck(hash):
            continue

        # Write updates to DB
        if config['DEVELOPMENT']['quickentry'] == 'no':
            tag_list = input("Enter tags seperated by a space "
                             f"of photo: {original_name}: ").split()
        else:
            tag_list = []
        filepath_id = db.insert_filepath(filepath)
        photo_id = db.insert_photo(new_name, hash,
                                   date_taken, filepath_id)
        if tag_list:
            for tag in tag_list:
                tag_id = db.insert_tag(tag)
                db.insert_phototag(photo_id, tag_id)

        # Handle the filesystem side of the photo
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        if args.verbose:
            print(f"Moving{pic} to {filepath}")
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


if __name__ == '__main__':

    if args.process:
        process()
    if args.archive:
        archive()
