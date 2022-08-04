import sqlite3
import json

#Establishing connection with the database
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()


def create_quotes_table():
    cursor.execute("DROP TABLE IF EXISTS quotes")
    table = """ CREATE TABLE quotes (
        quote TEXT NOT NULL,
        author_name VARCHAR(50)
        ); """

    cursor.execute(table)
    
    
def create_author_table():
    cursor.execute("""DROP TABLE IF EXISTS authors""")
    table = """ CREATE TABLE authors (
        name VARCHAR(100) PRIMARY KEY UNIQUE,
        born VARCHAR(200),
        reference VARCHAR(200)
        ); """
        
    cursor.execute(table)


def create_tag_table():
    cursor.execute("""DROP TABLE IF EXISTS tags""")
    table = """ CREATE TABLE tags
        (tag VARCHAR(100),
        quote_content TEXT,
        FOREIGN KEY (quote_content) REFERENCES quotes(quote) ON DELETE CASCADE); """
        
    cursor.execute(table)


def populate_quote_table(quote,author):
    connection.execute("INSERT INTO \
        quotes (quote,author_name)\
        VALUES (:quote,:author_name)",
        {"quote":quote,"author_name":author})

def populate_author_table(name,born,reference):
    connection.execute("INSERT OR IGNORE INTO \
        authors (name,born,reference)\
        VALUES (:name,:born,:reference)",\
        {"name":name,"born":born,"reference":reference})

def populate_tag_table(tag,quote):
    connection.execute("INSERT INTO tags (tag,quote_content) \
        VALUES (:tag,:quote_content)",{"tag":tag,"quote_content":quote})


def get_each_tag(quote,tags):
    for tag in tags:
        populate_tag_table(tag,quote)


def get_quotes_data(quotes):
    for each in quotes:
        populate_quote_table(each['quote'],each['author'])
        get_each_tag(each['quote'],each['tags'])


def get_authors_data(authors):
    for item in authors:
        populate_author_table(item['name'],item['born'],item['reference'])          

def store_quotes():
    create_quotes_table()
    create_author_table()
    create_tag_table()
    
    with open('quotes.json') as json_file:
        data = json.load(json_file)
        get_quotes_data(data['quotes'])
        get_authors_data(data['authors'])
            

store_quotes()

connection.commit()
connection.close()