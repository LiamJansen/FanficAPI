from flask import Flask
# from flask_restful import Resource, Api
from scraper import Scraper
from flask import request, jsonify

app = Flask(__name__)

scraper = Scraper()

@app.route('/categories/')
# Gets the different categories of fandoms that ffnet offers
def get_categories():
    return {"categories": scraper.get_categories()}

@app.route('/<category>/fandoms')
# Gets all of the fandoms of a category
def get_fandoms_of_category(category):
    return {"fandoms": scraper.get_fandoms_of_category(category)}

@app.route('/<category>/<fandom>/stories/<page_number>')
# Get a page of stories for provided fandom
def get_stories_of_fandom(category, fandom, page_number):
    return {"story_data": scraper.get_stories_of_fandom(category, fandom, page_number)}

@app.route('/story/<story_id>/chapter/<chapter_number>')
# Get the contents of the chapter
def scrape_chapter_content(story_id, chapter_number):
    return {"chapter_content" : scraper.scrape_chapter_content(story_id, chapter_number)}

@app.route('/story/<story_id>/metadata')
# Gets the metadata of the story (need the story id) 
def story_metadata(story_id):
    return {"metadata" : scraper.story_metadata(story_id)}

@app.route('/story/<story_id>/chapter_titles')
# Gets the chapter titles of the story 
def story_chapter_titles(story_id):
    return {"chapter_titles" : scraper.story_chapter_titles(story_id)}

if __name__ == '__main__':
    app.run(debug=True)