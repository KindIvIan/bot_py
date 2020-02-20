from flask import Flask
from flask_restful import Api, Resource, reqparse
import random, json

app = Flask(__name__)
api = Api(app)

with open('data.txt') as json_file:
    ai_quotes = json.load(json_file)

class Quote(Resource):
    def get(self, id=0):
        if id==0:
            return random.choice(ai_quotes), 200
            with open('data.txt', 'w') as outfile:
                json.dump(ai_quotes, outfile)
        for quote in ai_quotes:
            if (quote["id"]==id):
                return quote, 200
        return "URL not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("url")
        parser.add_argument("tags")
        params = parser.parse_args()
        for quote in ai_quotes:
            if (id==quote["id"]):
                return f"Quote with id {id} already exists", 400
        quote = {
            "id": int(id),
            "url": params["url"],
            "tags": params["tags"]
        }
        ai_quotes.append(quote)
        return quote, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("url")
        parser.add_argument("tags")
        params = parser.parse_args()
        for quote in ai_quotes:
            if (id==quote["id"]):
                quote["ulr"] = params["url"]
                quote["tags"] = params["tags"]
                return quote, 200

        quote = {
            "id": id,
            "url": params["url"],
            "tags": params["tags"]
        }

        ai_quotes.append(quote)
        return quote, 201

    def delete(self, id):
        global ai_quotes
        ai_quotes = [qoute for qoute in ai_quotes if qoute["id"]!=id]
        return f"URL with id {id} is deleted.", 200


api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
if __name__=='__main__':
    app.run(debug=True)
