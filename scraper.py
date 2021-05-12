from bs4 import BeautifulSoup
import requests, re
from time import sleep
import cloudscraper
import os.path

scraper = cloudscraper.CloudScraper(delay=5, browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False,
        "desktop": True,
    })
base_url = "https://www.fanfiction.net/"
    
genres = ("Adventure", "Angst", "Crime", "Drama", "Family", "Fantasy", "Friendship", "General", "Horror", "Humor", "Hurt", "Mystery", "Parody", "Poetry", "Romancy", "Sci-Fi", "Spiritual", "Supernatural", "Suspense", "Tragedy", "Western")

class Scraper:
    def get_categories(self):
        categories = []

        html_url = scraper.get(base_url).text
        soup = BeautifulSoup(html_url, "lxml")

        find_categories_container = soup.find(class_="dropdown-menu")
        find_categories = find_categories_container.find_all("a")

        for each in find_categories[1:]:
            if each.get_text() == "Crossovers":
                break
            categories.append({"title": each.get_text(), "route": each["href"]})

        return categories

    def get_fandoms_of_category(self, category):
        fandoms_of_category = []

        html_url = scraper.get(base_url + category).text
        soup = BeautifulSoup(html_url, "lxml")

        find_fandom_container = soup.find("div", {"id": "list_output"})
        find_fandoms = find_fandom_container.find_all("a")

        counting_objects = -1

        for each in find_fandoms:
            counting_objects = counting_objects + 1
            counting_objects_str = str(counting_objects)
            fandoms_of_category.append({"key": counting_objects_str, "title": str(each.get_text())})

        return fandoms_of_category

    def get_stories_of_fandom(self, category, fandom, page_number):
        stories_of_fandom = []

        html_url = scraper.get(base_url + category + "/" + fandom + "/?srt=1&r=10&p=" + page_number).text
        soup = BeautifulSoup(html_url, "lxml")

        stories = soup.find_all("div", {"class": "z-list zhover zpointer"})

        for each in stories:
            for title in each.find_all("a", {"class": "stitle"}):
                story_id = title["href"].split("/")[2] 
                title = title.get_text()
            for author in each.find_all("a", {"class": "stitle"}):
                author = author.next_sibling.next_sibling
                author = author.get_text()
            for description in each.find_all("div", {"z-padtop"}):
                for eacha in description.find_all("div"):
                    eacha.decompose()
                description = description.get_text()
            stories_of_fandom.append({"story_id": story_id,"title": title, "author": author, "description": description})

        return stories_of_fandom

    def scrape_chapter_content(self, story_id, chapter_number):
        chapter_array = []

        html_url = scraper.get(base_url + "s/" + story_id +"/" + chapter_number + "/").text
        soup = BeautifulSoup(html_url, "lxml")

        chapter_text = soup.find("div", {"id": "storytext"})
        chapter_text = str(chapter_text)
        # chapter_text = chapter_text.text
        chapter_array.append({"chapter_text": chapter_text})

        return chapter_array

    def story_metadata(self, story_id):
        metadata = []

        html_url = scraper.get(base_url + "s/" + story_id).text
        ffn_soup = BeautifulSoup(html_url, "lxml")

        soup_pre_story = ffn_soup.find("div", {"id": "pre_story_links"})
        if soup_pre_story.find("img"):
            fandom = soup_pre_story.select_one(".xcontrast_txt").text
            crossover = "yes"
        else:
            fandom = soup_pre_story.select_one(".xcontrast_txt:nth-of-type(2)").text
            crossover = "no"

        soup_prof_top = ffn_soup.find("div", {"id": "profile_top"})
        ffn_story_title = soup_prof_top.find("b", {"class": "xcontrast_txt"}).text
        ffn_story_author_name = soup_prof_top.find("a", {"class": "xcontrast_txt"}).text
        ffn_story_author_id = ""
        ffn_story_description = soup_prof_top.find("div", {"class": "xcontrast_txt"}).text

        soup_more_details = soup_prof_top.find("span", {"class": "xgray xcontrast_txt"}).text.split(" - ")

        ffn_story_rating = soup_more_details[0]
        language = soup_more_details[1]
        
        # ffn_author_id = (ffn_soup.find("div", {"id": "profile_top"}).find("a", href=True))["href"].split("/")

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith(genres):

                ffn_story_genre = soup_more_details[i].strip()

                break  # if found, exit the loop to prevent overwriting of the variable

            else:
                ffn_story_genre = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Chapters:"):

                ffn_story_chapter_count = soup_more_details[i].replace("Chapters:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_chapter_count = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Words:"):

                ffn_story_num_words = soup_more_details[i].replace("Words:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Reviews:"):

                ffn_story_num_rvws = soup_more_details[i].replace("Reviews:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

        else:
            ffn_story_num_rvws = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Favs:"):

                ffn_story_num_favs = soup_more_details[i].replace("Favs:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

            else:
                ffn_story_num_favs = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Follows:"):

                ffn_story_num_follows = soup_more_details[i].replace("Follows:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

            else:
                ffn_story_num_follows = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Updated:"):

                ffn_story_last_update_date = soup_more_details[i].replace("Updated:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

            else:
                ffn_story_last_update_date = "Not found"

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Published:"):

                ffn_story_publish_date = soup_more_details[i].replace("Published:", "").strip()

                break  # if found, exit the loop to prevent overwriting of the variable

        for i in range(0, len(soup_more_details)):
            if soup_more_details[i].startswith("Status: Complete"):

                ffn_story_status = "Complete"

                break  # if found, exit the loop to prevent overwriting of the variable

            else:
                ffn_story_status = "Incomplete"

        characters = soup_more_details

        while len(characters) > 4:
            characters.pop()

        try:
            if language and ffn_story_rating in characters:
                characters.remove(language)
                characters.remove(ffn_story_rating)
            if ffn_story_genre == "Not found":
                ffn_characters = characters[0]
            elif characters[1].startswith("Chapters"):
                ffn_characters = "Not found"
            else:
                ffn_characters = characters[1]
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        # # dates = [date for date in ffn_soup.find_all("span") if date.has_attr("data-xutime")]

        metadata.append({"story id": story_id,
        "fandom": fandom,
        "crossover" : crossover ,
        "story_title" : ffn_story_title,
        "author" : ffn_story_author_name,
        "author_id" : ffn_story_author_id,
        "description" : ffn_story_description,
        "rating" : ffn_story_rating,
        "language" : language,
        "genre" : ffn_story_genre,
        "characters" : ffn_characters,
        "amount of chapters" : ffn_story_chapter_count,
        "word count" : ffn_story_num_words,
        "review count" : ffn_story_num_rvws,
        "fav count" : ffn_story_num_favs,
        "follow count" : ffn_story_num_follows,
        "last update:" : ffn_story_last_update_date,
        "publish date" : ffn_story_publish_date,
        "status" : ffn_story_status
        })

        return metadata

    def story_chapter_titles(self, story_id):
        chapter_titles = []

        html_url = scraper.get(base_url + "s/" + story_id).text
        ffn_soup = BeautifulSoup(html_url, "lxml")

        soup_chapter_titles = ffn_soup.find("select").find_all("option")
        for x in soup_chapter_titles:
            chapter_titles.append(x.text)

        return chapter_titles