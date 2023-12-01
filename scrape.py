import requests
from bs4 import BeautifulSoup
import pprint

# created variables for 2 pages of Hacker News content
res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titleline > a')
subtext = soup.select('.subtext')
links2 = soup2.select('.titleline > a')
subtext2 = soup2.select('.subtext')

# combining links and subtexts
mega_links = links + links2
mega_subtext = subtext + subtext2

# sorting the list starting from the highest voted story
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key = lambda k:k['votes'], reverse = True)

# looping through the html file in Hacker News and returning the highest voted story
def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item[idx].getText()
        href = item[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})  
    return sort_stories_by_votes(hn)

# using pprint to making the dictionary more readable
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
