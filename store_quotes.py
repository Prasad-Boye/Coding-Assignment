import sqlite3
import json

#Establishing connection with the database
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()


def create_quotes_table():
    cursor.execute("DROP TABLE IF EXISTS quotes")
    table = """ CREATE TABLE quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote TEXT NOT NULL,
        author_id INT
        ); """

    cursor.execute(table)
    
    
def create_author_table():
    cursor.execute("""DROP TABLE IF EXISTS authors""")
    table = """ CREATE TABLE authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100),
        born VARCHAR(200),
        reference VARCHAR(200)
        ); """
        
    cursor.execute(table)


def create_tag_table():
    cursor.execute("""DROP TABLE IF EXISTS tags""")
    table = """ CREATE TABLE tags
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag VARCHAR(100) UNIQUE); """
        
    cursor.execute(table)

def create_quote_tag_table():
    cursor.execute("DROP TABLE IF EXISTS quote_tag")
    table = """ CREATE TABLE quote_tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag_id INT,
        quote_id INT,
        FOREIGN KEY (tag_id) REFERENCES tag(id),
        FOREIGN KEY (quote_id) REFERENCES quote(id)
        ); """

    cursor.execute(table)


def populate_quote_table(quote,author,author_dict):
    author_id = author_dict[author]
    connection.execute("INSERT INTO \
        quotes (quote,author_id)\
        VALUES (:quote,:author_id)",
        {"quote":quote,"author_id":author_id})

def populate_author_table(details):
    name = details['name']
    born = details['born']
    reference = details['reference']
    
    connection.execute("INSERT INTO \
        authors (name,born,reference)\
        VALUES (:name,:born,:reference)",\
        {"name":name,"born":born,"reference":reference})

def populate_tag_table(tag):
    connection.execute("INSERT OR IGNORE INTO tags (tag) \
        VALUES (:tag)",{"tag":tag})

def populate_quote_tag_table(tag_id,quote_id):
    connection.execute("INSERT INTO quote_tag (tag_id,quote_id) \
        VALUES (:tag_id,:quote_id)",{"tag_id":tag_id,"quote_id":quote_id})
    
def add_tag_data(tag,tag_dict,quote_count,tag_count):
    tag_count += 1
    if tag not in tag_dict:
        tag_dict[tag] = tag_count
    tag_id = tag_dict[tag]
    populate_tag_table(tag)
    populate_quote_tag_table(tag_id,quote_count)
    
    return tag_dict,tag_count
    

def fill_quote_tag_tables(quotes,author_dict):
    tag_dict = {}
    tag_count = 0
    quote_count = 0
    
    for each in quotes:
        populate_quote_table(each['quote'],each['author'],author_dict)
        quote_count += 1
        for tag in each['tags']:
           tag_dict,tag_count =  add_tag_data(tag,tag_dict,quote_count,tag_count)


def populate_tables(data):
    author_dict = {}
    author_count = 0

    for details in data['authors']:
        populate_author_table(details)
        author_count += 1
        author_dict[details['name']] = author_count
    
    fill_quote_tag_tables(data['quotes'],author_dict)
    

def store_quotes():
    create_quotes_table()
    create_author_table()
    create_tag_table()
    create_quote_tag_table()
    
    with open('quotes.json') as json_file:
        data = json.load(json_file)
        populate_tables(data)
            

store_quotes()

connection.commit()
connection.close()