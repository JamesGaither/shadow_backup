###############################################################################
# Module: dbhandler.py
# Purpose: Handles database calls/writes for ShadowBackup
# Written by James Gaither
# www.jamesgaither.com
###############################################################################

# Base Libraries
import sqlite3
import os


class dbhandler:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

        self.c.execute('''
                CREATE TABLE if NOT EXISTS filepath (
                filepath_id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT UNIQUE)''')
        self.c.execute('''
                CREATE TABLE if NOT EXISTS tag (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT UNIQUE)''')
        self.c.execute('''
                CREATE TABLE if NOT EXISTS photo (
                photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hash TEXT UNIQUE,
                date_taken TEXT,
                filepath_id INTEGER,
                FOREIGN KEY (filepath_id) REFERENCES filepath(filepath_id))
                ''')
        self.c.execute('''
                CREATE TABLE if NOT EXISTS photo_tag (
                photo_id INTEGER,
                tag_id INTEGER,
                FOREIGN KEY (photo_id) REFERENCES photo(photo_id),
                FOREIGN KEY (tag_id) REFERENCES tag(tag_id),
                PRIMARY KEY (photo_id, tag_id))''')
        self.conn.commit()

    # Check if hash exists
    def hashcheck(self, hash):
        '''Check if hash exists returns photo_id if it does'''
        self.c.execute("SELECT photo_id FROM photo WHERE hash=?", (hash,))
        photo_id = self.c.fetchone()
        if photo_id:
            return photo_id[0]

    def insert_filepath(self, folder_path):
        self.c.execute('''
                INSERT or IGNORE into filepath(filepath)
                VALUES(?)''', (folder_path,))
        self.conn.commit()
        self.c.execute('''
                SELECT filepath_id from filepath WHERE filepath=?
                ''', (folder_path,))
        return self.c.fetchone()[0]

    def insert_photo(self, extension, hash, date_taken=None, filepath_id=None):
        self.c.execute('''
                INSERT into photo
                (hash, date_taken, filepath_id)
                VALUES(?,?,?)
                ''', (hash, date_taken, filepath_id))

        self.conn.commit()
        photo_id = self.c.lastrowid
        photo_name = str(photo_id) + extension
        self.c.execute('''
                UPDATE photo SET name=?
                WHERE photo_id=?''', (photo_name, photo_id))
        self.conn.commit()
        return photo_id, photo_name

    # This handles a single tag insert
    def insert_tag(self, tag):
        if not tag:
            return
        self.c.execute('''
                INSERT or IGNORE into tag(tag) VALUES(?)''', (tag,))
        self.conn.commit()
        self.c.execute('''
                SELECT tag_id from tag WHERE tag=?
                ''', (tag,))
        return self.c.fetchone()[0]

    # Function for linking photos to tag
    def insert_phototag(self, photo_id, tag_id):
        self.c.execute('''
                INSERT or IGNORE into photo_tag(photo_id, tag_id)
                VALUES(?,?)''', (photo_id, tag_id))
        self.conn.commit()

    # Pull a single filepath
    def pull_filepath(self, filepath_id):
        self.c.execute('''
        SELECT filepath from filepath
        WHERE filepath_id=?''', (filepath_id,))
        return self.c.fetchone()[0]

    # Pull photo list given a list of tags
    def pull_photo(self, search_tags, exclude_tags=None):
        photos_to_pull = {}
        for tag in search_tags:
            query = '''
                    SELECT filepath.filepath, photo.name, photo.photo_id
                        from filepath
                        JOIN photo on photo.filepath_id = filepath.filepath_id
                        JOIN photo_tag ON photo.photo_id = photo_tag.photo_id
                        JOIN tag ON photo_tag.tag_id = tag.tag_id
                    WHERE tag.tag = ?'''
            self.c.execute(query, (tag,))
            for p, n, pi in self.c.fetchall():
                if pi in photos_to_pull.keys():
                    continue
                photos_to_pull[pi] = os.path.join(p, n)

        # If exclude tags are given, handle those
        if exclude_tags:
            key_copy = list(photos_to_pull.keys())
            for photo_id in key_copy:
                self.c.execute('''
                    SELECT tag.tag from photo_tag
                        JOIN tag on tag.tag_id = photo_tag.tag_id
                    WHERE photo_tag.photo_id = ?''', (photo_id,))
                for pulled_tag in self.c.fetchall():
                    if pulled_tag[0] in exclude_tags:
                        try:
                            del photos_to_pull[photo_id]
                        except Exception:
                            continue
        photo_list = [v for v in photos_to_pull.values()]
        return photo_list

    # Pull all photos that have no tags
    def notag_query(self, base_path):
        notag_photo = []
        photoid_list = []
        self.c.execute('''
                select photo.photo_id, filepath.filepath, photo.name
                from photo
                    JOIN filepath on photo.filepath_id = filepath.filepath_id
                    LEFT JOIN photo_tag on photo.photo_id = photo_tag.photo_id
                WHERE photo_tag.photo_id is null''')
        for photo_id, filepath, photo_name in self.c.fetchall():
            photoid_list.append(photo_id)
            notag_photo.append(os.path.join(base_path, filepath, photo_name))
        return photoid_list, notag_photo

    def pull_name(self, photo_id):
        self.c.execute('''
                SELECT photo.name from photo
                WHERE photo_id=?''', (photo_id,))
        return self.c.fetchone()

    # WIP delete functionality
    def delete_photo(self, photo_name):
        print("non-functional for now")
        return


if __name__ == '__main__':
    db_path = r'C:\Users\james.gaither\Projects\shadow_backup\photo_test.db'
    tag_list = ['test2']
    exclude_tags = ['test2']
    db = dbhandler(db_path)
    for i in db.pull_photo(tag_list, exclude_tags):
        print(i)
