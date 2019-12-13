# Shadow Backup

Shadow Backup is a WIP photo backup and indexing tool written in python3.

## Website

Visit the following sites for more info
https://github.com/JamesGaither/shadow_backup/
https://jamesgaither.com/projects

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

Shadow Backup aims to be a piece in your arsenal of photo management tools by utilizing:

1. Your OS file system to manage the disk write of the photos
2. SQLite as the DataBase of choice for managing indexes of the photos for the fastest pull times for your photos
3. 7Zip (might change in the future) handles archiving and encrypting your photos for uploading to a backup server.

## How to use Shadow Backup

It is suggested to only use Shadow Backup if you are familiar with Python at this point (though this will be available for none-python users in the future). The general process is described below.

1. Have python 3.8, pip, pipenv, and 7zip
2. Clone the project from github to your local machine
3. copy main.ini.sample to main.ini and fill out the needed information
4. run `pipenv sync` to install needed python packages (or `pipenv install` if it doesn't work)
5. Start using the project. Run all commands under pipenv e.g. `pipenv run main.py`
6. For all arguments and options, run `pipenv run main.py -h`
