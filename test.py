from bs4 import BeautifulSoup
import requests, re
from time import sleep


html_url = requests.get("https://www.fanfiction.net/s/8175132/1/").text
soup = BeautifulSoup(html_url, 'lxml')

damian_categories = []

chapter_text = soup.find("div", {"id": "storytext"})

print(chapter_text)