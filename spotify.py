from bs4 import BeautifulSoup
import requests
import sys
from requests_html import HTMLSession
import subprocess
import time

def spotif(url):
    #print(url)
    fol = "/usr/bin/curl " + url + " > spot.html"
    cmd2 = subprocess.Popen(fol,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out1, err = cmd2.communicate()   
    # Open the Spotify source code file
    time.sleep(3)
    with open("spot.html") as fp:
        soup = BeautifulSoup(fp,features="html.parser")
        title1 = str(soup.find('title'))
    #print(title1)    
    title2 = title1.replace("\n", "")    
    get1 = title2.split("|")
    get2 = get1[0].split("<title>")
    song = get2[1].split(" - ")
    artist = get2[1].split("by ")
    #print(song[0])
    #print(artist[1])
    artist = artist[1].split()
    return artist[0],song[0]


if __name__ == "__main__":
    print(spotif(sys.argv[1]))
#print(shazaminfo("https://www.shazam.com/track/603087900/bubblin"))