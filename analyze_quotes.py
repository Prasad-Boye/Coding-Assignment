import sqlite3

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()


### Query 1 Get total number of quotations on the website

def get_total_no_of_quotes():
    query1_data = cursor.execute("SELECT count(id) FROM quote_author")
    for row in query1_data:
        print("Total no. of quotations on the website :",row[0])
        print()
        
get_total_no_of_quotes()


### Query 2 Get total number of quotes by a given author

def capitalize_author_name(letter,author,isCapital):
    if letter == " " or letter == ".":
        isCapital = True
        
    elif isCapital:
        letter = letter.capitalize()
        isCapital = False
    else:
        letter = letter.lower()
        
    author += letter
    
    return [author,isCapital]

def get_author_quotes(author):
    cursor.execute("SELECT * \
        FROM (SELECT count(author_name),author_name \
            FROM quote_author GROUP BY author_name)\
        WHERE author_name=:author ",{"author":author })
    return cursor

def get_no_of_quotes_by_author():
    print("Enter Author Name :")
    author_name = input()
    isCapital = True
    author = ''
    
    for letter in author_name:
        [author,isCapital] = capitalize_author_name(letter,author,isCapital)

    cursor = get_author_quotes(author)
    query2_data = cursor.fetchall()
    
    if(len(query2_data) > 0):
        for row in query2_data:
            print("Total no. of quotations by {}:".format(author),row[0])
            print()
    else:
        print("Oops! the entered author name is invalid. Please try again...")
        get_no_of_quotes_by_author()

get_no_of_quotes_by_author()




### Query 3 Minimum, Maximum, and Average no. of tags on the quotations

try:
    ### Created a View to find the number of quotations on each tag
    cursor.execute('''CREATE VIEW quote_tag_details AS \
    SELECT COUNT(tag_id) AS no_of_tags,quote_id \
    FROM (SELECT quote_author.id AS quote_id,quote_tag.tag_id \
        FROM quote_author LEFT JOIN quote_tag ON \
        quote_author.id = quote_tag.quote_id) \
    GROUP BY quote_id''')
    
except:
    pass

def get_max_min_avg_of_tags():
    cursor.execute("SELECT MIN(no_of_tags),MAX(no_of_tags),AVG(no_of_tags)\
        FROM quote_tag_details")

    query3_data = cursor.fetchall()

    for item in query3_data:
        print("Minimum tags on the quotations: ",item[0])
        print("Maximum tags on the quotations: ",item[1])
        print("Average tags on the quotations: ",item[2])
        print()
    
get_max_min_avg_of_tags()



### Query4 Authors who authored the maximum number of quotations

def print_top_authors(query4_data):
    for row in query4_data:
        print(row[1])

def get_top_authors(number):
    cursor.execute("SELECT * \
        FROM (SELECT count(author_name) as no_of_quotes,author_name \
            FROM quote_author \
            GROUP BY author_name \
            ORDER BY no_of_quotes DESC, author_name\
            LIMIT :top_number)",{"top_number":number})

    query4_data = cursor.fetchall()
    
    return query4_data
    
def find_top_authors():
    try:
    ### Reading Input from the User 
        print("Enter a positive number:")
        top_number = int(input())
        
        if(top_number > 50):
            top_number = 50

        if(top_number > 0):
            query4_data = get_top_authors(top_number)
            print("Top {} Authors List:".format(top_number))
            print_top_authors(query4_data)
        else:
            print("Please enter a valid positive number")
            find_top_authors()
            
    except:
        find_top_authors()

find_top_authors()


connection.close()