import sqlite3
import json

#Establishing connection with the database
connection = sqlite3.connect('quotes.db')

def create_quotes_table():
    connection.execute('''CREATE TABLE quote
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        quote_content TEXT NOT NULL,
        author_name VARCHAR(200)
        );''')
    
def create_tag_table():
    connection.execute('''CREATE TABLE tag
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        tag_name TEXT NOT NULL UNIQUE);''')

def create_quote_tag_table():
    connection.execute('''CREATE TABLE quote_tag(
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
        tag_id INTEGER,
        quote_id INTEGER,
        FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
        FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE
        );''')

def populate_quote_author_table(quote_content,author_name):
    connection.execute("INSERT OR IGNORE INTO \
        quote_author (quote_content,author_name)\
        VALUES (:quote_content,:author_name)",\
        {"quote_content":quote_content,"author_name":author_name})

def populate_tag_table(tag_name):
    connection.execute("INSERT OR IGNORE INTO tag (tag_name) \
        VALUES (:tag_name)",{"tag_name":tag_name})
            
def populate_quote_tag_table(quote,tag):
    connection.execute("INSERT INTO quote_tag(tag_id,quote_id)\
        SELECT tag_item.tag_id, quote_item.quote_id\
        FROM (SELECT id as tag_id\
        FROM tag\
        WHERE tag_name = :tag) as tag_item,\
        (SELECT id as quote_id\
        FROM quote_author\
        WHERE quote_content = :quote) as quote_item\
        ",{"tag":tag,"quote" :quote})


def get_each_tag(tags):
    for tag in tags:
        populate_tag_table(tag)
        populate_quote_tag_table(each['quote'],tag)


with open('quotes.json') as json_file:
    data = json.load(json_file)
    for each in data['quotes']:
        populate_quote_author_table(each['quote'],each['author'])
        get_each_tag(each['tags'])
    




connection.commit()
connection.close()