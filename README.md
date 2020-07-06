# Shadow Backup

Shadow Backup is a WIP photo backup and indexing tool written in python3.

## Website

[Main Website](https://jamesgaither.com/projects)  
[Download from Github](https://github.com/JamesGaither/shadow_backup/)

## Status

I am working on this project alone in my spare time between a full-time job, other hobbies, and other projects, so it will take a bit of time before it is complete. Currently it is in an early Alpha state and very much subject to change. I work on develop branch and push stable builds (or at least as stable as you can get in alpha) to master and try to tag what I consider major releases with tag numbers.  
I am open to any suggestions, so please drop me a message or even better a pull request to help out.

## Recent News (7/6/20)

* I have decided to drop pipenv support in favor of venv and a requirements.txt format. Pipenv at the moment just has too many issues and takes up too much of my time trying to keep it working on my system. venv just works as expected.
* Major overhaul in progress for how tags are edited. I have decided to drop my attempt at a GUI and instead implement an update function. This allows the user to pull any photos to a working directory, make any changes they want, and then run update. This will (using the photo name) match the entry in the db, hash the photo, if changed, it will remove the old photo from the archive, make any updates to the DB, and store the new photo in archive.
* With the update to the tag section, I have decided the tags with added to the metadata of the photos as well as the DB. This means on tag entry, it will write the tags to the metadata, and on update will pull the tag info from the metadata. (WIP)

## What Shadow Backup does and how it's different from what is on the market

This software's overall goal is to give the user a simple, clean, fully transparent method to manage any number of photos. Much of the software that is out there to manage photos try to be an all in one method to manage your photos and typically charge for all the features it adds. Shadow Backup aims to be different by not offering an all in one solution that replicates readily available software that does its job exceptionally well. It is designed around how I like to manage photos. Some key design goals of Shadow Backup are listed below along with their implementation status:

1. Have the index listed separately from the photos to accommodate ease of backup and cross platform support [implemented via SQLite]
2. Ensure maximum privacy by ensuring:
    1. All code is run locally on your machine with no statistics tracking or any such privacy breeching methods [implemented]
    2. Backups (whether they leave your computer or not) are encrypted [implemented]
    3. A fully open codebase so you might review all code that is run [implemented]
3. Pull any subset of photos via tags [Partially implemented]
4. Not rewrite code that others have available online that has been tested multiple times and proven.
5. Have access for any developer to expand on the core functionality of Shadow Backup [implemented by using SQLite DB for indexing]

## How to use Shadow Backup

It is suggested to only use Shadow Backup if you are familiar with Python at this point (though the goal is to make shadow backup available for non python users in the future).  
Shadow backup is meant to be used as a photo archive tool. it was designed with the expectation that you will edit any photos before running them through it. Currently, Shadow backup does not handle updating photos that were already processed very well. A general process I followed for designing Shadow Backup is listed below:  

1. Upload a fresh batch of photos to an input folder
2. make any needed edits using your editor of choice (I use GIMP) and delete any photos you don't want
3. upload the batch of photos using shadow backup and the -t option to tag new photos with something that describes that batch (e.g. summer_vacation_2019)  

Below is how to install Shadow Backup:  

1. Have python 3.8, pip, and the ability to install needed packages
2. Clone the project from github to your local machine
3. Copy main.ini.sample to main.ini and fill out the needed information
4. Better instructions to come

### Arguments

Shadow backup takes a variety of arguments that allow it to do different things. See below for a full list  
-h, --help: Displays all implemented arguments and their descriptions.  
-p, --process: Runs the main program. This option takes photos from the input folder and processes them, adds the info to the DB and moves them to the processed folder.  
-v, --verbose: Added to any other argument for a more verbose output with greater details.  
-i, --inserttags: Only run alone. This activates the GUI for adding tags.  
--pullphoto: Pulls photos to the results directory based on the tags given (requires -i option). The tags are summed in results. Meaning, given arguments tag1 and tag2, only photos with the tag tag1 AND tag2 will be pulled. This copies the photo from the archive to the results, so you might use the results folder as you see fit.  
-t, --tags: Give tags as an argument separated by a space. This option when combined with --pullphoto will pull the photos with the corresponding tags. When used with the -p option, will label all new photos with the tags given (great option for processing those vacation pictures)  
-e, --exclude: Give tags as an argument separated by a space. Use with the "--pullphoto" option to exclude all photos that include one or more of the listed tags from the search.
