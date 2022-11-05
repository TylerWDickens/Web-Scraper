import string
import requests
import os
from bs4 import BeautifulSoup


def nature_article_scraper(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find('h1').text
    try:
        article = soup.find("div", {"class": "c-article-body"}).get_text().lstrip().replace("\r", "").replace("\n", "")
    except AttributeError:
        article = soup.find("div", {"class": "article-item__body"}).get_text().lstrip().replace("\r", "").replace("\n", "")

    return title, article


def nature_scraper(page_num, genre):
    url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={}" .format(page_num)
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')

    articles = soup.find_all('article')
    link_list = list()
    file_list = list()

    path = r"C:\Users\tdickens\Documents\Dev\Web Scraper\Web Scraper\task"

    for i in range(int(page_num)):
        cur_page = i + 1
        directory = 'Page_{}' .format(cur_page)
        if not os.path.exists(directory):
            os.makedirs(directory)

        for article in articles:
            article_type = article.find('span', {'data-test': 'article.type'}).text
            article_link = article.find('a', {"data-track-action": "view article"})
            if genre == article_type.strip():
                link_list.append("https://nature.com" + article_link.get('href'))

        for link in link_list:
            title, article = nature_article_scraper(link)
            filename = (''.join(title)).replace(' ', '_').strip(string.punctuation) + '.txt'

            with open(f"{directory}\{filename}", 'w', encoding='utf-8') as file:
                file.write(article)
                print(article)
            file_list.append(filename)

    return file_list


if __name__ == "__main__":
    page_number = input()
    type_of_article = input()
    print(nature_scraper(page_number, type_of_article))
    print("Saved all articles")
