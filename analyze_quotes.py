import sqlite3

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()


### Query 1 Get total number of quotations on the website

def print_total_no_of_quotes():
    total_quotes = cursor.execute("SELECT count(*) FROM quotes")
    for row in total_quotes:
        print("Total no. of quotations on the website :",row[0])
        print()
        

### Query 2 Get total number of quotes by a given author



def print_no_of_quotes_by_author():
    author = "Albert Einstein"

    cursor.execute("SELECT count(*)\
        FROM (SELECT *  FROM quotes LEFT JOIN \
        authors ON quotes.author_id = authors.id )\
        WHERE name = :author\
       ",{"author":author})


    quotes_by_author = cursor.fetchall()
   
    for row in quotes_by_author:
        print("No of quotations by {} :".format(author),row[0])
        print()
   



### Query 3 Minimum, Maximum, and Average no. of tags on the quotations

def print_max_min_avg_of_tags():
    cursor.execute("SELECT MIN(no_of_tags),MAX(no_of_tags),AVG(no_of_tags)\
        FROM (SELECT count(tag_id) as no_of_tags,quotes.id as quote  \
            FROM quotes LEFT JOIN \
            quote_tag ON quotes.id = quote_tag.quote_id \
            GROUP BY quote)\
       ")

    min_max_avg_of_tags = cursor.fetchall()

    for item in min_max_avg_of_tags:
        print("Minimum tags on a quotation: ",item[0])
        print("Maximum tags on a quotation: ",item[1])
        print("Average tags on the quotations: ",item[2])
        print()


### Query4 Authors who authored the maximum number of quotations

def find_top_authors(limit_value):
    cursor.execute("SELECT count(quote_id) as no_of_quotes,name\
            FROM (SELECT quotes.id AS quote_id,authors.name  \
            FROM quotes LEFT JOIN authors ON\
            quotes.author_id = authors.id)\
            GROUP BY name \
            ORDER BY no_of_quotes DESC\
            LIMIT :top_number",{"top_number":limit_value})

    top_authors = cursor.fetchall()
    
    return top_authors


def print_top_authors():
    top_number = 5
    top_authors = find_top_authors(top_number)
    print("Top {} Authors and no. of quotes:".format(top_number))
   
    for row in top_authors:
        print(row[1],"-",row[0])


def get_all_results():
    print_total_no_of_quotes()
    print_no_of_quotes_by_author()
    print_max_min_avg_of_tags()
    print_top_authors()


get_all_results()
    
connection.close()