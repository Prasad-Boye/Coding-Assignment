from re import A
from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import urljoin


def get_quote_author_details(quotesData,url):
    page_quotes_list = []
    authors_list = []
    
    for quote_info in quotesData:
        quote_details = get_quote_info(quote_info)
        author_details = get_author_details_url(quote_info,url)
        page_quotes_list.append(quote_details) 
        authors_list.append(author_details)
        
    return page_quotes_list,authors_list

def get_quote_info(quote_info):
    quote_content = quote_info.find("span", class_="text").text.strip()
    author= quote_info.find("small", class_="author").text.strip()
    tags = get_tags(quote_info)
    quote_details = get_quote_details(quote_content,author,tags)
    
    return quote_details


def get_author_details_url(quote_info,url):
    about_container = quote_info.find("span",class_=lambda x: x != 'text')
    about_element = about_container.find('a')
    autor_details_url = about_element.get('href')
    updated_url = urljoin(url, autor_details_url)
    
    return updated_url


def get_tags(quote_info):
    all_tags = quote_info.find_all("a", class_="tag")
    tags = []
    for tag in all_tags:
        tags.append(tag.text.strip())

    return tags


def get_quote_details(quote_content,author,tags):
    quote = quote_content.replace('”', '').replace('“','')
    quote_details = {"quote":quote,"author":author.replace('-',' '),"tags":tags}
    
    return quote_details

def get_author_details(page_content,url):
    name = page_content.find("h3",class_='author-title').text.replace('-'," ")
    author_born_date = page_content.find("span", class_="author-born-date").text
    author_born_location = page_content.find('span', class_='author-born-location').text
    born = author_born_date + author_born_location
    author_details = {"name": name.strip(), "born":born.strip(),"reference" : url}
    
    return author_details

def get_author_quote_lists(page_content,url):
    quotesData = page_content.find_all("div", class_="quote")
    quotes_list,author_urls = get_quote_author_details(quotesData,url)
    
    return quotes_list,author_urls

def get_page_content(url):
    response = requests.get(url)
    page_content = BeautifulSoup(response.text, 'lxml')
    
    return page_content

def get_next_page_url(next_btn_container,url):
    next = next_btn_container.find('a')
    next_page_url = next.get('href')
    updated_url = urljoin(url, next_page_url)
    
    return updated_url

def get_next_btn_container(page_content):
    next_btn_container = page_content.find('li', class_='next')
    
    return next_btn_container


def get_all_pages_data(url):
    
    page_data = {}
    page_content = get_page_content(url)
    next_btn_container = get_next_btn_container(page_content)
    page_data[url] = page_content
   
    while next_btn_container != None:
        updated_url = get_next_page_url(next_btn_container,url)
        page_content = get_page_content(updated_url)
        next_btn_container = get_next_btn_container(page_content)
        page_data[updated_url] = page_content
              
    return page_data


def write_data_into_json_file(quotes,authors):
    author_quotes = {"quotes":quotes,"authors":authors}
    file = open('quotes.json','w')
    file.write(json.dumps(author_quotes))
    file.close()


def scrape_website():
    url = 'http://quotes.toscrape.com/'
    page_data = get_all_pages_data(url)
    author_urls_list = []
    quotes = []
    authors = []
    
    for url,page_content in page_data.items():
        quotes_list,authors_urls = get_author_quote_lists(page_content,url)
        quotes += quotes_list
        author_urls_list += authors_urls
    
    author_urls_list = list(set(author_urls_list))
    for author_url in author_urls_list:
        author_page_content = get_page_content(author_url)
        author_details = get_author_details(author_page_content,author_url)
        authors.append(author_details)
    
    write_data_into_json_file(quotes,authors)
    
scrape_website()

