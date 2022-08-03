from re import A
from tkinter import END
from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urljoin

def get_author_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    author_name = soup.find("h3",class_='author-title').text
    author_born_date = soup.find("span", class_="author-born-date").text
    author_born_location = soup.find('span', class_='author-born-location').text
    born = author_born_date + author_born_location
    refernece = url
    author_details = {"name": author_name, "born":born,"refernece" : refernece}
    return author_details
    

def get_author_details_url(quote_details,url):
    author_details_element = quote_details.find("span",class_=lambda x: x != 'text')
    autor_details_url_element = author_details_element.find('a')
    autor_details_url =autor_details_url_element.get('href')
    url = urljoin(url, autor_details_url)
    
    return get_author_details(url)
    

def get_quote_details(quotesData,url):
    page_quotes_list = []
    
    for quote_details in quotesData:
        scrape_quote_details(quote_details,page_quotes_list)
        author_details = get_author_details_url(quote_details,url)
        
    return page_quotes_list,author_details


def scrape_quote_details(quote_details,page_quotes_list):
    quote_content = quote_details.find("span", class_="text")
    author= quote_details.find("small", class_="author")
    tags = scrape_tags(quote_details)
    quote_summary = get_results(quote_content,author,tags)
    page_quotes_list.append(quote_summary)
    
    return page_quotes_list


def scrape_tags(quote_details):
    all_tags = quote_details.find_all("a", class_="tag")
    tags = []
    for tag in all_tags:
        tags.append(tag.text.strip())

    return tags


def get_results(quote_content,author,tags):
    quote = (quote_content.text.strip()).replace('”', '').replace('“','')
    quote_summary = {"quote":quote,"author":author.text,"tags":tags}
    
    return quote_summary


def get_next_page_url(next,url):
    next_page_url = next.get('href')
    url = urljoin(url, next_page_url)
    
    return url


def create_json_file(quotes,authors):
    author_quotes = {"quotes":quotes,"authors":authors}
    file = open('quotes.json','w')
    file.write(json.dumps(author_quotes))
    file.close()


def scrape_website(url,quotes,authors):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next = soup.select_one('li.next > a')
    quotesData = soup.find_all("div", class_="quote")
    quotes_list,author_details = get_quote_details(quotesData,url)
    quotes += quotes_list
    authors.append(author_details)

    if next != None:
        url=get_next_page_url(next,url,)
        scrape_website(url,quotes,authors)
    else:
        create_json_file(quotes,authors)
        pass
  
  
def initiate_web_scrapping():  
    url = 'http://quotes.toscrape.com/'
    quotes = []
    authors =[]
    scrape_website(url,quotes,authors)
    
initiate_web_scrapping()
    

