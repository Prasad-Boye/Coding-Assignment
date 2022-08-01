import sqlite3

connection = sqlite3.connect('quotes.db')
# query1 = connection.execute("SELECT count(id) FROM quote_author")
# for row in query1:
#     print("Total no. of quotations on the website :",row[0])

print("Enter Author Name :")
author = input()
    
query2 = connection.execute("SELECT * FROM (SELECT count(id),* FROM quote_author GROUP BY author_name) WHERE author_name=:author ",{"author":author })

for row in query2:
    print(type(row))
    print("Total no. of quotations by {}:" .format(author),row[0])

    
    
connection.close()