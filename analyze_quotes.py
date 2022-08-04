import sqlite3

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()


### Query 1 Get total number of quotations on the website

def get_total_no_of_quotes():
    total_quotes = cursor.execute("SELECT count(author_name) FROM quotes")
    for row in total_quotes:
        print("Total no. of quotations on the website :",row[0])
        print()
        

### Query 2 Get total number of quotes by a given author

def get_author_quotes(author):
    cursor.execute("SELECT * \
        FROM (SELECT count(author_name),author_name \
            FROM quotes GROUP BY author_name)\
        WHERE author_name=:author ",{"author":author})
    return cursor

def get_no_of_quotes_by_author():
    author = "Albert Einstein"

    cursor = get_author_quotes(author)
    quotes_by_author_count = cursor.fetchall()
   
    for row in quotes_by_author_count:
        print("Total no. of quotations on the website by {}:".format(author),row[0])
        print()



### Query 3 Minimum, Maximum, and Average no. of tags on the quotations

def get_max_min_avg_of_tags():
    cursor.execute("SELECT MIN(no_of_tags),MAX(no_of_tags),AVG(no_of_tags)\
            FROM (SELECT count(tag) as no_of_tags  FROM quotes LEFT JOIN \
            tags ON quotes.quote = tags.quote_content \
            GROUP BY quote)\
       ")

    min_max_avg_of_tags = cursor.fetchall()

    for item in min_max_avg_of_tags:
        print("Minimum tags on a quotation: ",item[0])
        print("Maximum tags on a quotation: ",item[1])
        print("Average tags on the quotations: ",item[2])
        print()


### Query4 Authors who authored the maximum number of quotations

def find_top_authors(number):
    cursor.execute("SELECT * \
        FROM (SELECT count(author_name) as no_of_quotes,author_name \
            FROM quotes \
            GROUP BY author_name \
            ORDER BY no_of_quotes DESC, author_name\
            LIMIT :top_number)",{"top_number":number})

    top_authors = cursor.fetchall()
    
    return top_authors


def get_top_authors():
    top_number = 5
    top_authors = find_top_authors(top_number)
    print("Top {} Authors and no. of quotes:".format(top_number))
   
    for row in top_authors:
        print(row[1],"-",row[0])


def get_all_results():
    get_total_no_of_quotes()
    get_no_of_quotes_by_author()
    get_max_min_avg_of_tags()
    get_top_authors()
    
get_all_results()
    
connection.close()