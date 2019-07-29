import sqlite3

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
                CREATE TABLE if NOT EXISTS archivepath (
                archive_id INTEGER PRIMARY KEY AUTOINCREMENT,
                archive_path TEXT UNIQUE)''')
        self.c.execute('''
                CREATE TABLE if NOT EXISTS photo (
                photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                hash TEXT UNIQUE,
                date_taken TEXT,
                filepath_id INTEGER,
                archive_id INTEGER,
                incloud BOOLEAN,
                FOREIGN KEY (filepath_id) REFERENCES filepath(filepath_id)
                FOREIGN KEY (archive_id) REFERENCES archivepath(archive_id))''')
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
        self.c.execute("SELECT photo_id FROM photo WHERE hash=?", (hash,))
        row = self.c.fetchone()
        if row:
            print("hash in DB for photo_id:", row[0])
            return "hash in DB"

    def insert_filepath(self, folder_path):
        self.c.execute('''
                INSERT or IGNORE into filepath(filepath)
                VALUES(?)''', (folder_path,))
        self.conn.commit()
        self.c.execute('''
                SELECT filepath_id from filepath WHERE filepath=?
                ''', (folder_path,))
        return self.c.fetchone()[0]

    def insert_photo(self, name, hash, date_taken=None,
                     filepath_id=None):
        self.c.execute('''
                INSERT into photo
                (name, hash, date_taken, filepath_id, incloud)
                VALUES(?,?,?,?)
                ''', (name, hash, date_taken, filepath_id, 0))

        self.conn.commit()
        return self.c.lastrowid

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

    #WIP archiving photos
    def insert_archive(self, photo_name, archive_path):
        return

#WIP to pull photos where tag is input
    def pull_tag(self, search_tags):
        query = f'''
                select filepath.filepath
                from filepath
                join photo on filepath.filepath_id = photo.filepath_id
                join photo_tag on photo.photo_id = photo_tag.photo_id
                join tag on photo_tag.tag_id = tag.tag_id
                where tag.tag in ({','.join(['?']*len(search_tags))})'''
        return self.c.execute(query, search_tags)

# Strictly for testing below
if __name__ == '__main__':
    db = dbhandler(r'c:\Users\james.gaither\projects\shadow_backup\test.db')