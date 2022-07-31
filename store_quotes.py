from ctypes import Union
import sqlite3
import json

connection = sqlite3.connect('quotes.db')

# connection.execute('''CREATE TABLE quote_author
#          (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#          quote_content TEXT NOT NULL,
#          author_name VARCHAR(200)
#          );''')

# connection.execute('''CREATE TABLE tag
#          (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#          tag_name TEXT NOT NULL UNIQUE);''')

# connection.execute('''CREATE TABLE quote_tag(
#   id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#   tag_id INTEGER,
#   quote_id INTEGER,
#   FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE,
#   FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE
# );''')

def add_quote(quote_content,author_name):
    connection.execute("INSERT OR IGNORE INTO quote_author (quote_content,author_name)\
        VALUES (:quote_content,:author_name)",{"quote_content":quote_content,"author_name":author_name})

def add_tag(tag_name):
    connection.execute("INSERT OR IGNORE INTO tag (tag_name) \
      VALUES (:tag_name)",{"tag_name":tag_name})
    
def add_quote_tag(quote,tag):
    connection.execute("INSERT INTO quote_tag(tag_id,quote_id)\
    SELECT t1.tag_id, t2.quote_id\
        FROM (SELECT id as tag_id,tag_name as tag\
        FROM tag\
        WHERE tag_name = :tag) as t1,\
        (SELECT id as quote_id, quote_content as quote\
        FROM quote_author\
        WHERE quote_content = :quote) as t2\
    ",{"tag":tag,"quote" :quote})


with open('quotes.json') as json_file:
    data = json.load(json_file)
 
    # print("Type:", type(data))

    for each in data['quotes']:
        # print(each['quote'])
        # print()
        quote = each['quote']
        author = each['author']
        add_quote(quote,author)
        for tag in each['tags']:
            add_tag(tag)
            add_quote_tag(quote,tag)
            

cursor = connection.execute("SELECT * FROM tag")
for row in cursor:
    print(row)

connection.close()