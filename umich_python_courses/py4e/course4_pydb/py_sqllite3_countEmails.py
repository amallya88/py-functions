import sqlite3
import re

def get_emails_from_file(file_name):
    """ Parse file_name and create list of e-mail addresses matching search criteria
    example: From: stephen.marquard@uct.ac.za
    e-mail address extracted only if line starts with 'From: '
    """
    fh = open(file_name)
    emails = [line.split()[1] for line in fh if line.startswith('From: ')]
    return emails


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


def insert_email_domain_counts(db_conn, db_cur, tableName, lst_emails):
    """ Extract domains from email addresses and
    insert domain and number of emails received from domain into database
    db_conn: a connection to sqlite db
    db_cur: a cursor of db_conn
    tableName: name of email counts table. Table must have fields count and org
    lst_emails: list of email addresses that sent email to us
    """

    lst_domains = [re.findall('@(.+)', email)[0] for email in lst_emails]
    for domain in lst_domains:
        db_cur.execute('SELECT count FROM {table} WHERE org = ? '.format(table=tableName), (domain,))
        row = db_cur.fetchone()
        if row is None:
            db_cur.execute('''INSERT INTO {table} (org, count)
                        VALUES (?, 1)'''.format(table=tableName), (domain,))
        else:
            db_cur.execute('UPDATE {table} SET count = count + 1 WHERE org = ?'.format(table=tableName),
                           (domain,))
    db_conn.commit()


def main(db_conn, db_cur, tableName, db_schema):
    # initialize db table
    initialize_db(db_cur, tableName, db_schema)

    # parse file to get all emails
    lst_emails = get_emails_from_file('mbox.txt')

    # insert/update emails into db table
    insert_email_domain_counts(db_conn, db_cur, tableName, lst_emails)


if __name__ == "__main__":
    db_conn = sqlite3.connect('email_counts.sqlite')
    db_cur = db_conn.cursor()

    tableName = 'Counts'
    db_schema = [{'field_name': 'org',
                  'field_type': 'TEXT'},
                 {'field_name': 'count',
                  'field_type': 'INTEGER'}]

    # parse file to get all emails
    lst_emails = get_emails_from_file('mbox.txt')

    main(db_conn, db_cur, tableName, db_schema)

    # top 3 senders
    sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 3'
    for row in db_cur.execute(sqlstr):
        print(str(row[0]), row[1])

    db_conn.close()
