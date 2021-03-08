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
