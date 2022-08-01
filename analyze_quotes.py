import sqlite3

### Get total number of quotations on the website
connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

query1 = connection.execute("SELECT count(id) FROM quote_author")
for row in query1:
    print("Total no. of quotations on the website :",row[0])


### Get total number of quotes by a given author

print("Enter Author Name :")
author = input()

query2 = cursor.execute("SELECT * \
    FROM (SELECT count(author_name),author_name \
        FROM quote_author \
        GROUP BY author_name)\
    WHERE author_name=:author ",{"author":author })

data = cursor.fetchall()

if(data):
    for row in data:
        print("Total no. of quotations by {}:".format(author),row[0])
else:
    print("Total no. of quotations by {}: 0".format(author))
    
    
### Minimum, Maximum, and Average no. of tags on the quotations


### Authors who authored the maximum number of quotations

print("Enter a number:")
top_number = input()

query4 = cursor.execute("SELECT * \
    FROM (SELECT count(author_name) as no_of_quotes,author_name \
        FROM quote_author \
        GROUP BY author_name \
        ORDER BY no_of_quotes DESC, author_name\
        LIMIT :top_number)",{"top_number":top_number})

data = cursor.fetchall()

print("Top {} contributors List:".format(top_number))
for row in data:
    print(row[1],"-",row[0])

    
connection.close()