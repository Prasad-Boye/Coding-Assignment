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


# def populate_quote_tag_tables(quotes):
#     for each in quotes:
#         populate_quote_table(each['quote'],each['author'])
#         for tag in each['tags']:
#             populate_tag_table(tag)
 


def filter_data(data):
    quote_tag_dict = {}
    author_dict = {}
    author_count = 0
    tag_count = 0
    quote_count = 0
    
    for details in data['authors']:
        populate_author_table(details)
        author_count += 1
        author_dict[details['name']] = author_count
    
    for each in data['quotes']:
        populate_quote_table(each['quote'],each['author'],author_dict)
        quote_count += 1
        for tag in each['tags']:
            tag_count += 1
            
            populate_tag_table(tag)
            


def store_quotes():
    create_quotes_table()
    create_author_table()
    create_tag_table()
    
    with open('quotes.json') as json_file:
        data = json.load(json_file)
        filter_data(data)
            

store_quotes()

connection.commit()
connection.close()