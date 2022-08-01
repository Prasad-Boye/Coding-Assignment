from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urljoin


def get_quote_details(quotes,quotesData):
    for quote_details in quotesData:
        quote_content = quote_details.find("span", class_="text")
        author= quote_details.find("small", class_="author")
        tags = get_tags(quote_details)
        results = get_results(quotes,quote_content,author,tags)

    return results

def get_tags(quote_details):
    all_tags = quote_details.find_all("a", class_="tag")
    tags = []
    for tag in all_tags:
        tags.append(tag.text.strip())

    return tags

def get_results(quotes,quote_content,author,tags):
    quote = quote_content.text
    stripped_length = len(quote)-1
    quotes.append({"quote":quote[1:stripped_length],"author":author.text.strip(),"tags":tags})
    
    return {"quotes":quotes}

def get_page_response(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next = soup.select_one('li.next > a')
    quotesData = soup.find_all("div", class_="quote")
    quotes_dict = get_quote_details(quotes,quotesData)
    
    return [next,soup,quotesData,quotes_dict]

def get_next_page_url(next,url):
    next_page_url = next.get('href')
    url = urljoin(url, next_page_url)
    
    return url

quotes = []
url = 'http://quotes.toscrape.com/'
   
while True:
    [next,soup,quotesData,quotes_dict] = get_page_response(url)
    if next != None:
        url=get_next_page_url(next,url)
    else:
        break    
    
# print(json.dumps(quotes_dict))
file = open('quotes.json','w')
file.write(json.dumps(quotes_dict))
file.close()