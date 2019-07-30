# base libraries
import os
import argparse
import configparser
import datetime
import hashlib
import shutil
from datetime import datetime
from PIL import Image
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
args = parser.parse_args()

# Pull Config info
config = configparser.ConfigParser()
config.read('config/main.ini')
picpath = config['GENERAL']['picture_path']
p_in = config['GENERAL']['p_in']
db = dbhandler(Path(config['GENERAL']['db_path']))
sevenz_path = Path(config['ARCHIVE']['sevenz_path'])
vol_size = config['ARCHIVE']['vol_size']
archive_path = Path(config['ARCHIVE']['path'])
archive_pw = config['ARCHIVE']['password']
archive_out = Path(config['ARCHIVE']['output'])
allpics = []

###Build out Functions###

# Pulls a date taken from photo (if any)
def get_date_taken(path):
    return Image.open(path)._getexif()[36867]

#Pulls pictures in from to-process folder and processes them
def process():
    for subdir, dirs, files in os.walk(os.path.join(picpath, p_in)):
        for file in files:
            allpics.append(os.path.join(subdir, file))
    for pic in allpics:
        original_name, extension = os.path.splitext(pic)
        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()
        new_name = hash + extension.lower()
        try:
            date_taken = datetime.strptime(get_date_taken(pic),
                                           '%Y:%m:%d %H:%M:%S')
            filepath = os.path.join(picpath,
                                    datetime.strftime(date_taken, '%Y'),
                                    datetime.strftime(date_taken, '%m'),
                                    datetime.strftime(date_taken, '%d'))
        except:
            date_taken = None
            filepath = os.path.join(picpath, 'nodate')

        # Check if picture has been processed
        if db.hashcheck(hash):
            print(original_name, "has been processed before. skipping")
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
        shutil.move(pic, os.path.join(filepath, new_name))

# Push unprocessed photos to archive (WIP-likely to change and evolve with time)     
def archive():
    nonarchived_files = db.archive_query()
    for photo_path in nonarchived_files:
        shutil.copy(photo_path, Path(config['TEST']['temp_folder']))
   

    archive_command = r'"{}" a -v"{}" -t7z -mhe=on -p"{}" "{}" "{}"'.format(sevenz_path, vol_size, archive_pw, archive_out, Path(config['TEST']['temp_folder']))
    subprocess.run(archive_command)
    

    for subdir, dirs, file in os.walk(archive_path):
        for archive_picture in file:
            db.insert_archive(archive_picture, str(archive_out))





if __name__ == '__main__':
    if args.process:
        process()
    if args.archive:
        archive()
        