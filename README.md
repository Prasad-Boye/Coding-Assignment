# Coding-Assignment
In this project I scrapped data from http://quotes.toscrape.com/page/1/ which contains quotes by different authors. Each quote has 0 or many tags associated with it.

There are multiple pages on the website so, I developed a command logic in crawl_quotes.py file that scrapes data from all the pages on the website.

The scrapped data is then stored in the quotes.json

I created a sqlite database to store the data in the quotes.json in the form of relational tables (quotes.db).

In analyze_quotes.py file I have written function logics that return:

Total no. of quotations on the website

No. of quotations authored by the given author’s name (user Input required) Example: “Albert Einstein”

Minimum, Maximum, and Average no. of tags on the quotations

Given a number N return top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes (user Input required)
