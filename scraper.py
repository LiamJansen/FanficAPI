from bs4 import BeautifulSoup
import requests, re
from time import sleep

class Scraper:
    def __init__(self, rate_limit=1):
        self.base_url = 'https://fanfiction.net'
        self.rate_limit = rate_limit
        self.parser = "html.parser"

    def get_fandoms_of_category(self, category):
        fandoms_of_category = []

        html_url = requests.get('https://fanfiction.net/' + category).text
        soup = BeautifulSoup(html_url, 'lxml')

        find_fandom_container = soup.find("div", {"id": "list_output"})
        find_fandoms = find_fandom_container.find_all("a")

        for each in find_fandoms:
            fandoms_of_category.append (str(each.get_text()))

        return fandoms_of_category

    def get_stories_of_fandom(self, category, fandom):
        html_url = requests.get('https://fanfiction.net/' + category + '/' + fandom + '/?&srt=1&r=10').text
        soup = BeautifulSoup(html_url, 'lxml')

        page_number = int(soup.find('a', text="Last")['href'].split('=')[-1])
        page_number = page_number + 1

        story_ids_of_fandom = []


        for each in range(1, page_number):
            each_str = str(each)
            url = 'https://www.fanfiction.net/' + category + '/' + fandom + '/?&srt=1&lan=1&r=10&p=' + each_str
            result = requests.get(url)
            html = result.content
            soup = BeautifulSoup(html, 'lxml')

            # Get story IDs
            story_ids = [s['href'].split('/')[2] for s in soup.find_all('a', {'class': 'stitle'})]

            for each in story_ids:
                story_ids_of_fandom.append(each)

            sleep(2)

        return story_ids_of_fandom  

    def get_chapter_titles(self, story_id):

        chapter_title_list = []

        for page in range(1, 4):
            page_number = str(page)

            html_url = requests.get(
                'https://www.fanfiction.net/s/8099181/' + page_number + '/Avatar-of-Victory').text
            soup = BeautifulSoup(html_url, 'lxml')

            element = soup.find(
                lambda tag: tag.name == "option" and
                len(tag.attrs) == 2 and
                tag["selected"] == "")

            chapter_title_list.append(element.text)

            sleep(1)

        return chapter_title_list
