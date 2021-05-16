import xml.etree.ElementTree as ET
import sqlite3


def initialize_db(db_cur, tableName, db_schema):
    """ Create a table tableName using schema specified in db_records. Any existing table with same name dropped.
    db_cur: cursor to sqlite db
    tableName: name of table to create in db
    db_records is a list of dict. the dict contains keys field_name, field_type defining the fields
    """
    db_cur.execute('DROP TABLE IF EXISTS {table}'.format(table=tableName))

    # construct required table schema string
    schema_str = "CREATE TABLE {table} ({fields})"
    fields = ['{} {}'.format(field['field_name'], field['field_type']) for field in db_schema]
    schema_str = schema_str.format(table=tableName, fields=",".join(fields))

    db_cur.execute(schema_str)


def insert_into_table(db_cur, tableName, db_records):
    """
    Insert a new, unique record into tableName table using db_cur sqlite cursor
    db_records is a list of tuples. the tuples contain key/val pairs for
    each field and data value to be inserted
    """
    insert_sql_str = "INSERT OR IGNORE INTO {table} ({fields}) VALUES ( {values} )"
    fields = ",".join([tup[0] for tup in db_records])
    values = [tup[1] for tup in db_records]

    sql_str = insert_sql_str.format(table=tableName,
                                    fields=fields,
                                    values=','.join(['?']*len(values)))
    db_cur.execute(sql_str, values)


def get_pkey_from_lkey(db_cur, tableName, pkey_field, lkey_field, lkey_value):
    """ A simple SELECT that gets id (primary key) for given logical key/val
    db_cur: cursor to sqlite db
    Returns the primary key value
    """
    sql_str = 'SELECT {id} FROM {table} WHERE {lkey} = ? '.format(id=pkey_field,
                                                                  table=tableName,
                                                                  lkey=lkey_field)
    db_cur.execute(sql_str, (lkey_value,))
    return db_cur.fetchone()[0]


conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor()

# Make some fresh tables
initialize_db(cur, 'Artist', [{'field_name': 'id',
                               'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'},
                              {'field_name': 'name',
                               'field_type': 'TEXT UNIQUE'}
                              ])

initialize_db(cur, 'Genre', [{'field_name': 'id',
                              'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'},
                             {'field_name': 'name',
                              'field_type': 'TEXT UNIQUE'}
                             ])

initialize_db(cur, 'Album', [{'field_name': 'id',
                              'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'},
                             {'field_name': 'artist_id',
                             'field_type': 'INTEGER'},
                             {'field_name': 'title',
                              'field_type': 'TEXT UNIQUE'}
                             ])

initialize_db(cur, 'Track', [{'field_name': 'id',
                              'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'},
                             {'field_name': 'title',
                              'field_type': 'TEXT UNIQUE'},
                             {'field_name': 'len',
                             'field_type': 'INTEGER'},
                             {'field_name': 'count',
                              'field_type': 'INTEGER'},
                             {'field_name': 'rating',
                              'field_type': 'INTEGER'},
                             {'field_name': 'album_id',
                              'field_type': 'INTEGER'},
                             {'field_name': 'genre_id',
                              'field_type': 'INTEGER'}
                             ])

fname = 'Library.xml'

# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>
def lookup(d, key):
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None


stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))

for entry in all:
    if lookup(entry, 'Track ID') is None:
        continue

    track_name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry, 'Genre')

    if track_name is None or artist is None or album is None or genre is None:
        continue

    insert_into_table(cur, 'Artist', [('name', artist)])
    artist_id = get_pkey_from_lkey(cur, 'Artist', 'id', 'name', artist)

    insert_into_table(cur, 'Genre', [('name', genre)])
    genre_id = get_pkey_from_lkey(cur, 'Genre', 'id', 'name', genre)

    insert_into_table(cur, 'Album', [('title', album),
                                     ('artist_id', artist_id)
                                     ])
    album_id = get_pkey_from_lkey(cur, 'Album', 'id', 'title', album)

    insert_into_table(cur, 'Track', [('title', track_name),
                                     ('len', length),
                                     ('count', count),
                                     ('rating', rating),
                                     ('album_id', album_id),
                                     ('genre_id', genre_id)
                                     ])

conn.commit()

# run the following query on resulting database
# shows how related tables are joined using f_keys to generate composite data
# SELECT Track.title, Artist.name, Album.title, Genre.name
#     FROM Track JOIN Genre JOIN Album JOIN Artist
#     ON Track.genre_id = Genre.ID and Track.album_id = Album.id
#         AND Album.artist_id = Artist.id
#     ORDER BY Artist.name LIMIT 3