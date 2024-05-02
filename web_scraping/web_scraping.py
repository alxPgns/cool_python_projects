import requests
from bs4 import BeautifulSoup
import pprint


# function for pagination
def get_hn_page(page):
    res = requests.get(f'https://news.ycombinator.com/news?p={page}')
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup


page = 0
soup = get_hn_page(page)
# creating two lists from classes titleline and subtext
links = soup.select(".titleline")
subtext = soup.select(".subtext")


# function for extracting vote, title and link attributes
def clean_hacker_news(links, subtext):
    hn = []

    # we use enumerate instead of just "item", since we have to manipulate two lists at once
    for index, item in enumerate(links):
        vote = subtext[index].select(".score")
        title = links[index].getText()
        href = links[index].find('a').get('href', None)

        # if we have 0 votes (no vote) for an article of the page, we won't append
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))

            # append to the list only if upvotes > 99, to get the top articles
            if points > 99:
                hn.append({'title': title, 'link': href, 'vote': points})

    return sort_articles_by_votes(hn)


# function for sorting articles in descending order, by vote value
def sort_articles_by_votes(hn):
    sorted_list = sorted(hn, key=lambda d: d['vote'], reverse=True)
    return sorted_list


articles = clean_hacker_news(links, subtext)
pprint.pprint(articles)
