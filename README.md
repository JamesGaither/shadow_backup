# Shadow Backup

Shadow Backup is a WIP photo backup and indexing tool written in python3.

## Website

Visit the following sites for more info  
<https://github.com/JamesGaither/shadow_backup/>  
<https://jamesgaither.com/projects>

### Current State

As I am writing this in my spare time between a full-time job, it will take some time before I say it is complete. It is currently in an Alpha state with version tagged copies being those open for release if you want to work with it. I highly suggest only people familiar with Python even try to use it at this early state, but as I build it out, I would like to open it up for anyone to use.
I am open to suggestions, so either send me a message or drop a pull request for an added feature. Do remember, this is very much a WIP, so I have several ideas that I plan to implement in due course.

### What Shadow Backup does and how it's different from what is on the market

This software's overall goal is to give the user a simple, clean, fully transparent method to manage any number of photos. Much of the software that is out there to manage photos try to be an all in one method to manage your photos and typically charge for all the features it adds. Shadow Backup aims to be different by not offering an all in one solution that replicates readily available software that does its job exceptionally well. It is designed around how I like to manage photos. Some key design goals of Shadown Backup are listed below along with their implementation status:

1. Have the index listed seperatly from the photos to accommodate ease of backup and cross platform support [implemented via SQLite]
2. Ensure maximum privacy by:
    1. All code is run locally on your machine with no statistics tracking or any such privacy breeching methods [implemented]
    2. Backups (whether they leave your computer or not) are encrypted [implemented]
    3. A fully open codebase so you might review all code that is run [implemented]
3. Pull any subset of photos via tags [Partially implemented]
4. Not rewrite code that others have available online that has been tested multiple times and proven.
5. Have access for any developer to expand on the core functionality of Shadow Backup [implemented by using SQLite DB for indexing]

### Tools needed for Shadow Backup

1. Having photos tagged with key information that I want to put there.
2. Be able to retrieve any subset of photos using any tag(s) I want.
3. Maintain all my photos locally for easy off-line access, but also be able to download my photos from a disaster storage and not have to re-index them (hence using a sqlite DB).
4. Have an easy method to upload photos to any online backup system.
5. Not rewrite code that others have available online that has been tested multiple times and proven.  This is why I use 7z for compression, encryption, and packaging. I could write a module that does this, but to what means? It would not be nearly as good as 7z and not nearly as tested. With this in mind though, I wanted to ensure this program could work on Windows as well as Linux since I use both.
6. Ensure maximum privacy by ensuring anything leaving your computer is encrypted fully.

## How to use Shadow Backup

It is suggested to only use Shadow Backup if you are familiar with Python at this point (though this will be available for none-python users in the future). The general process is described below.

1. Have python 3.8, pip, pipenv, and 7zip
2. Clone the project from github to your local machine
3. copy main.ini.sample to main.ini and fill out the needed information
4. run `pipenv sync` to install needed python packages (or `pipenv install` if it doesn't work)
5. Start using the project. Run all commands under pipenv e.g. `pipenv run main.py`

### Arguments

Shadow backup takes a variety of aruments that allow it to do different things. See below for a full list  
-p, --process: Runs the main program. This option takes photos from the input folder and processes them, adds the info to the DB and moves them to the processed folder.  
-a, --archive: [WIP] Adds unprocessed photos to an encrypted archive. This feature is still in progress.  
-v, --verbose: Added to any other argument for a more verbose output with greater details.  
-i, --inserttags: Only run alone. This activates the GUI for adding tags.  
--pullphoto: Pulls photos to the results directory based on the tags given (requires -i option). The tags are summed in results. Meaning, given arguments tag1 and tag2, only photos with the tag tag1 AND tag2 will be pulled. This copies the photo from the archive to the results, so you might use the results folder as you see fit.  
-t, --tags: Give tags as an argument seperated by a space. This option when combined with --pullphoto will pull the photos with the coresponding tags. When used with the -p option, will label all new photos with the tags given (great option for processing those vacation pictures)
