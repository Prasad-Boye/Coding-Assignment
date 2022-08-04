from re import A
from telnetlib import X3PAD
from tkinter import END
from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urljoin

def scrape_author_details(url,authors_list):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    author_name = soup.find("h3",class_='author-title').text
    author_born_date = soup.find("span", class_="author-born-date").text
    author_born_location = soup.find('span', class_='author-born-location').text
    born = author_born_date + author_born_location
    author_details = {"name": author_name, "born":born,"reference" : url}
    authors_list.append(author_details)
    
    return authors_list
    

def get_author_details_url(quote_info,url,authors_list):
    about_container = quote_info.find("span",class_=lambda x: x != 'text')
    about_element = about_container.find('a')
    autor_details_url = about_element.get('href')
    url = urljoin(url, autor_details_url)
    
    return scrape_author_details(url,authors_list)
    

def get_quote_info(quotesData,url):
    page_quotes_list = []
    authors_list = []
    
    for quote_info in quotesData:
        scrape_quote_info(quote_info,page_quotes_list)
        get_author_details_url(quote_info,url,authors_list)
        
    return page_quotes_list,authors_list


def scrape_quote_info(quote_info,page_quotes_list):
    quote_content = quote_info.find("span", class_="text")
    author= quote_info.find("small", class_="author")
    tags = scrape_tags(quote_info)
    quote_details = get_results(quote_content,author,tags)
    page_quotes_list.append(quote_details)
    
    return page_quotes_list


def scrape_tags(quote_info):
    all_tags = quote_info.find_all("a", class_="tag")
    tags = []
    for tag in all_tags:
        tags.append(tag.text.strip())

    return tags


def get_results(quote_content,author,tags):
    quote = (quote_content.text.strip()).replace('”', '').replace('“','')
    quote_details = {"quote":quote,"author":author.text,"tags":tags}
    
    return quote_details
    

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
    soup = BeautifulSoup(response.text, 'lxml')
    next_container = soup.find('li', class_='next')
    quotesData = soup.find_all("div", class_="quote")
    quotes_list,author_details = get_quote_info(quotesData,url)
    
    quotes += quotes_list
    authors += author_details

    if next_container != None:
        next = next_container.find('a')
        url=get_next_page_url(next,url)
        scrape_website(url,quotes,authors)
    else:
        create_json_file(quotes,authors)
        
  
  
def initiate_web_scrapping():  
    url = 'http://quotes.toscrape.com/'
    quotes = []
    authors =[]

    scrape_website(url,quotes,authors)
    
initiate_web_scrapping()
    

