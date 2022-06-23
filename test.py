from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
video_url = "https://www.shazam.com/track/603087900/bubblin"
# Initialize an HTML Session
session = HTMLSession()
# Get the html content
response = session.get(video_url)
# Execute JavaScript
response.html.render(sleep=3)

soup = BeautifulSoup(response.html.html, "lxml")
name = soup.find("h1", {'class':'title line-clamp-2'}).text
artist = soup.find("h2", {'class':'artist ellip'}).text
artist = artist.replace(" ","")
print(artist)
# divs = soup.find_all("h1", {'class':'title line-clamp-2'})
# for div in divs:
#     print(div)
    #print (div['h1'])
divs = soup.find_all("div", {'class':'video-container'})
for div in divs:
    ytlink = (div['data-href'])
url = ytlink.split("?")
print(url[0])
