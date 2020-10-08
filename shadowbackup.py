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
import logging
from datetime import datetime
from pathlib import Path

# custom modules
from modules.dbhandler import dbhandler
from modules.gui import gui

# Handle arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--process", action="store_true",
                    help="reads all photos for processing")
# parser.add_argument("-v", "--verbose", action="store_true",
#                    help="prints detailed information to terminal")
parser.add_argument("-i", "--inserttags", action="store_true",
                    help="activates the gui for inputting tags")
parser.add_argument("--pullphoto", action="store_true",
                    help="pull photo based on tags given, requires -t arg")
parser.add_argument("-t", "--tags", nargs='+',
                    help="list of tags to either pull photos or to insert with"
                    " option -p")
parser.add_argument("-e", "--exclude", nargs='+',
                    help="list of tags to exclude when pulling photos")
parser.add_argument("-u", "--update", action="store_true", help="Coming Soon")
args = parser.parse_args()

# Verify at lease one argument is given
if not any(vars(args).values()):
    parser.error('Must provide at least 1 argument')

# Setup logging
logfile = Path('shadow.log')
log_level = 'DEBUG'
logging.basicConfig(filename=logfile, datefmt="%Y-%m-%d %H:%M:%S",
                    format=('%(asctime)s  %(name)s %(levelname)-10s '
                            '%(message)-10s'))
logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
handler = logging.StreamHandler()
handler.setLevel('DEBUG')
logger.addHandler(handler)

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
update_path = os.path.join(base_path, Path(config['PATH']['update']))
db = dbhandler(db_path)
valid_extensions = ['.tif', '.cr2', '.jpg', '.jpeg', '.png']

# General variables
allpics = []
reject_count = 0


def reject(file):
    '''Moves a file that is rejected to the rejected path'''
    global reject_count
    reject_count += 1
    if not os.path.exists(reject_path):
        os.makedirs(reject_path)
    file_name = os.path.basename(file)
    shutil.move(file, f'{reject_path}/{file_name}.{reject_count}')


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
            logger.info(f"{pic} does not have a valid photo extension")
            reject(pic)
            continue

        # Check if picture has been processed
        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()
        hashcheck = db.hashcheck(hash)
        if hashcheck:
            logger.info(f"{pic} has already been processed with photo ID:"
                        f"{hashcheck}")
            reject(pic)
            continue

        try:
            date_taken = datetime.strptime(get_date_taken(pic),
                                           '%Y:%m:%d %H:%M:%S')
            sub_filepath = os.path.join(db_p_storage,
                                        datetime.strftime(date_taken, '%Y'),
                                        datetime.strftime(date_taken, '%m'))
        except Exception:
            logger.info(f"Error raised on import of EXIF tag for {pic}")
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
        else:
            tag_id = db.insert_tag('none')
            db.insert_phototag(photo_id, tag_id)

        # Handle the filesystem side of the photo
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        logger.info(f"Moving {pic} to {os.path.join(filepath,new_name)}")
        shutil.move(pic, os.path.join(filepath, new_name))


def pull_photo():
    '''Pull a photo to a given directory given a list of tags'''
    if not args.tags:
        parser.error("The --pullphoto argument requires the -t argument "
                     "followed by at least one tag to search")

    tag_list = args.tags
    exclude_tags = args.exclude
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    results = db.pull_photo(tag_list, exclude_tags)
    logger.info(f"Search yielded {len(results)} results")
    for i in results:
        shutil.copy(os.path.join(base_path, i), results_path)


def update():
    '''Pull photos from update directory and update existing images'''
    for subdir, dirs, files in os.walk(update_path):
        for file in files:
            allpics.append(os.path.join(subdir, file))
    for pic in allpics:
        path, extension = os.path.splitext(pic)
        name = os.path.split(pic)[1]
        extension = extension.lower()
        if extension not in valid_extensions:
            logger.info(f"{pic} does not have a valid photo extension")
            reject(pic)
            continue
        try:
            photo_id = db.pull_id(name)[0]
        except TypeError:
            logger.info(f'{name} has not been processed before, please process'
                        f' instead of updating')
            continue

        hash = hashlib.md5(open(pic, 'rb').read()).hexdigest()

        # Let's see if any changes were made
        if db.compare_hash(photo_id, hash):
            logger.info(f'{name} has not changed since last update')
            continue

        # hashcheck = db.hashcheck(hash)



if __name__ == '__main__':
    if args.process:
        process()
    if args.inserttags:
        gui = gui(db_path, base_path)
        gui.photo_display()
        gui.window.mainloop()
    if args.pullphoto:
        pull_photo()
    if args.update:
        update()
