# Coding-Assignment
In this project I scrapped data from http://quotes.toscrape.com/page/1/ which contains quotes by different authors. Each quote has 0 or many tags associated with it.

There are multiple pages on the website so, I developed a command logic in crawl_quotes.py file that scrapes data from all the pages on the website.

Stored the scrapped data in the quotes.json file

I created a database to store the data in the quotes.json in the form of relational tables (quotes.db).

In analyze_quotes.py file I have written function logics that return:

1. Total no. of quotations on the website

2. No. of quotations authored by the given author’s name Example: “Albert Einstein” (***User Input required***)

3. Minimum, Maximum, and Average no. of tags on the quotations

4. Given a number N returns top N authors who authored the maximum number of quotations sorted in descending order of no. of quotes (***User Input required***)
