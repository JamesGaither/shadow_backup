# Shadow Backup
A WIP photo backup and indexing tool written in python3. Currently semi-operational.
More details at the following links
https://github.com/JamesGaither/shadow_backup/
https://jamesgaither.com/projects

### What does this software plan to do and how is this different?
This software's overall goal is to give the user a simple, clean, fully transparent method to manage a large number of photos. Much of the software that is out there to manage photos try to be an all in one method to manage your photos and typically charge for all the features it adds. Shadow Backup aims to be different by not offering an all in one solution that replicates readily available software that does it's job exceptionally well. It is designed around how I like to manage photos and also designed around my skill-level. Some ideas I want (such as full GUI support) are not listed below as my skills in UI is just not good enough yet. Some key goals of this are listed below (Planned, not all implemented yet):

1. Having photos tagged with key information that I want to put there.
2. Be able to retrieve any subset of photos using any tag(s) I want.
3. Maintain all my photos locally for easy off-line access, but also be able to download my photos from a disaster storage and not have to re-index them(hence using a sqlite DB).
4. Have an easy method to upload photos to any online backup system (or eventually to a remote server at a friend/family house). While the current system I use puts these into AWS deep glacier a key aspect I was shooting for was allowing that service to change without rewritting a huge section of code. This is why I use 7Z to compress, package, and encrypt photos into chunks. I can upload these chunks to whatever I want knowing that my photos are not just floating out in cyberspace for anyone to see.
5. Not rewrite code that others have available online that has been tested multiple times and proven.  This is why I use 7z for compression, encryption, and packaging. I could write a module that does this, but to what means? It would not be nearly as good as 7z and not nearly as tested. With this in mind though, I wanted to ensure this program could work on Windows as well as Linux since I use both.
6. Ensure maximum privacy by ensuring anything leaving your computer is encrypted fully.

### What tools does Shadow Backup need to run?
Shadow Backup aims to be a piece in your arsenal of photo management tools by utilizing:
1. Your OS file sytem to manage the disk write of the photos
2. SQLite as the DataBase of choice for managing indexs of the photos for the fastest pull times for your photos
3. 7Zip(might change in the future) handles archiving and encrypting your photos for uploading to a backup server.

### What is the current state? When will this be complete?
As I am writing this in my spare time between a full time job, it will take some time before I say it is complete. It is currently in an Alpha state with version tagged copies being those open for release if you want to work with it. I highly suggest only people familiar with Python even try to use it at this early state, but as I build it out I would like to open it up for anyone to use.
I am open to suggestions, so either send me a message or drop a pull request for an added feature. Do remember, this is very much a WIP, so I have several ideas that I plan to implement in due course.
