from bs4 import BeautifulSoup
import requests
import sys
from requests_html import HTMLSession

def shazaminfo(url):
    print(url)
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=3)
    soup = BeautifulSoup(response.html.html, "lxml")
    name = soup.find("h1", {'class':'title line-clamp-2'}).text
    artist = soup.find("h2", {'class':'artist ellip'}).text
    artist = artist.replace(" ","")

    divs = soup.find_all("div", {'class':'video-container'})
    for div in divs:
        ytlink = (div['data-href'])
    url1 = ytlink.split("?")
    session.close()
    return url1[0],name,artist


if __name__ == "__main__":
    print(shazaminfo(sys.argv[1]))
#print(shazaminfo("https://www.shazam.com/track/603087900/bubblin"))
