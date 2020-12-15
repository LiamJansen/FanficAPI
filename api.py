from flask import Flask
from flask_restful import Resource, Api
from scraper import Scraper
from flask import request
# from fanfiction import Scraper

app = Flask(__name__)
api = Api(app)

scraper = Scraper()

class Test(Resource):
    def get(self):
        # return {"fandoms" : scraper.get_fandoms_of_category('misc')}
        if 'category' in request.args and not 'fandom' in request.args:
            return {"fandoms" : scraper.get_fandoms_of_category(request.args['category'])}
        elif 'category' in request.args and 'fandom' in request.args:
            return {"story ids" : scraper.get_stories_of_fandom(request.args['category'], request.args['fandom'])}
        elif 'story_id' in request.args:
            return {"metadata" : scraper.scrape_story_metadata(request.args['story_id'])}
        else:
            return 'Your request failed'
            

# class Test2(Resource):
#     def get(self):
#         if 'category'  in request.args and 'fandom' in request.args:
#             return {"story ids" : scraper.get_stories_of_fandom(request.args['category'], request.args['fandom'])}
#         else:
#             return 'Your request failed'            

# class Test3(Resource):
#     def get(self):
#         if 'story_id' in request.args:
#             return {"metadata" : scraper.scrape_story_metadata(request.args['story_id'])}
#         else:
#             return 'Your request failed'

# class Test4(Resource):
#     def get(self):
#         if 'name' in request.args:
#             return 'Hello ' + request.args['name']
#         else:
#             return 'Hello John Doe'


api.add_resource(Test, '/')
# api.add_resource(Test2, '/2')
# api.add_resource(Test3, '/3')
# api.add_resource(Test4, '/4')

if __name__ == '__main__':
    app.run(debug=True)

# from fanfiction import Scraper

# app = Flask(__name__)
# api = Api(app)

# scraper = Scraper()

# class Test(Resource):
    # def get(self):
        # return {"fandoms" : scraper.get_genres('Family') }
        # return {"fandoms" : scraper.story_ids_by_fandom("Books", "Harry Potter", "test.txt") }
        # return {"fandoms" : scraper.scrape_story_metadata('8099181') }
        # return {"fandoms" : scraper.scrape_story(story_id, keep_html=False) }
        # return {"fandoms" : scraper.scrape_chapter(story_id, chapter_id, keep_html=False) }
        # return {"fandoms" : scraper.scrape_reviews_for_chapter(story_id, chapter_id) }

# api.add_resource(Test, '/')

# if __name__ == '__main__':
    # app.run(debug=True)