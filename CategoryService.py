from flask import Flask,request
import foursquare
import json
from flask_cors import CORS, cross_origin
import os



CLIENT_ID = "Input your client ID"
CLIENT_SECRET = "Input your client secret"
VERSION = "20170519"


app = Flask(__name__)
CORS(app)

@app.route('/categories')
def getCategories():
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    venue_categories = client.venues.categories()
    venue_cat_id_name_dict = {vc['id']: vc['name'] for vc in venue_categories['categories']}
    venue_cat_id_name_dict.update({category['id']: category['name'] for vc in venue_categories['categories'] for category in vc['categories']})

    return str(json.dumps(sorted(venue_cat_id_name_dict.items(),key=lambda  t:t[1]),ensure_ascii=True))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 9098))
    app.run(host='0.0.0.0', port=port)
