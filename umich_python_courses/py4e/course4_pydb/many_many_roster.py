import json
import sqlite3
import sqlite_utils as sqlutils

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Do some setup
sqlutils.initialize_db(cur, 'User', [{'field_name': 'id',
                                      'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'
                                      },
                                     {'field_name': 'name',
                                      'field_type': 'TEXT UNIQUE'
                                      }
                                     ])

sqlutils.initialize_db(cur, 'Course', [{'field_name': 'id',
                                        'field_type': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE'
                                        },
                                       {'field_name': 'title',
                                        'field_type': 'TEXT UNIQUE'
                                        }
                                       ])

sqlutils.initialize_db(cur, 'Member', [{'field_name': 'user_id',
                                        'field_type': 'INTEGER'
                                        },
                                       {'field_name': 'course_id',
                                        'field_type': 'INTEGER'
                                        },
                                       {'field_name': 'role',
                                        'field_type': 'INTEGER'
                                        },
                                       {'field_name': 'PRIMARY KEY',
                                        'field_type': '(user_id, course_id)'
                                        }
                                       ])

fname = 'roster_data.json'

# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]

    sqlutils.insert_into_table(cur, 'User', [('name', name)])
    user_id = sqlutils.get_pkey_from_lkey(cur, 'User', 'id', 'name', name)

    sqlutils.insert_into_table(cur, 'Course', [('title', title)])
    course_id = sqlutils.get_pkey_from_lkey(cur, 'Course', 'id', 'title', title)

    sqlutils.insert_into_table(cur, 'Member', [('user_id', user_id),
                                               ('course_id', course_id),
                                               ('role', role)
                                               ])

conn.commit()
