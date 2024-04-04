import sys
from bs4 import BeautifulSoup
import requests
import math

def list_of_pairs(n):
    """ Get first n datasets

    Output: list of (dataset title, url)
    """
    link = "https://catalog.data.gov/dataset/?q=&sort=views_recent+desc&page=1"
    response2 = requests.get(link)
    soup2 = BeautifulSoup(response2.text, "lxml")
    h3 = soup2.find_all('h3', class_="dataset-heading")
    page_vol = len(h3)

    fullpages = math.floor(n/page_vol)
    lastpage = math.ceil(n/page_vol)
    remain = n%page_vol
    list_of_pairs = []
    # On all full pages
    for i in range(fullpages):
        link = "https://catalog.data.gov/dataset/?q=&sort=views_recent+desc&page="+str(i+1)
        response2 = requests.get(link)
        soup2 = BeautifulSoup(response2.text, "lxml")
        h3s = soup2.find_all('h3', class_="dataset-heading")
        for j in range(len(h3s)):
            link = 'https://catalog.data.gov'+h3s[i].find('a', href=True)['href']
            title = h3s[j].find('a').text
            pair = (title,link)
            list_of_pairs.append(pair)

    # On the last page, for the remainings
    if remain != 0:
        link = "https://catalog.data.gov/dataset/?q=&sort=views_recent+desc&page="+str(lastpage)
        response2 = requests.get(link)
        soup2 = BeautifulSoup(response2.text, "lxml")
        h3s = soup2.find_all('h3', class_="dataset-heading")
        remain_pairs = []
        for i in range(len(h3s)):
            link = 'https://catalog.data.gov'+h3s[i].find('a', href=True)['href']
            title = h3s[i].find('a').text
            pair = (title,link)
            remain_pairs.append(pair)
        list_of_pairs += remain_pairs[0:remain]
    return list_of_pairs
    

if __name__ == "__main__":
    n = int(sys.argv[1])
    pairs = list_of_pairs(n)
    for title, url in pairs:
        print(title, url)


