from flask import Flask,request
import foursquare
import json
import pandas as pd, numpy as np
from sklearn.cluster import DBSCAN
from geopy.distance import great_circle
from shapely.geometry import MultiPoint
import nvector as nv
import itertools
from flask_cors import CORS, cross_origin



CLIENT_ID = "your four square client id"
CLIENT_SECRET = "your four squre client key"
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


@app.route('/bussiness')
def getBusinessScreennerResult():
    client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    categoryId = request.args.get('categoryId', None)
    location  = request.args.get('location', None)
    venuelist = client.venues.search(params={'near': location, 'categoryId': categoryId})
    venuedict = {venue['location']['lat']:venue['location']['lng'] for venue in venuelist['venues']}

    df = pd.DataFrame()
    df['lat'] = venuedict.keys()
    df['lng'] = venuedict.values()
    coords =df.as_matrix(columns=['lat', 'lng'])

    kms_per_radian = 6371.0088
    epsilon = 5 / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(np.radians(coords))
    cluster_labels = db.labels_
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([coords[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))

    centermost_points = clusters.map(get_centermost_point)

    listpoints = [x[1] for x in centermost_points.iteritems()]

    locationpeers = list(itertools.combinations(listpoints, 2))


    returnPeers =[]
    for eachPair in locationpeers:
       latitude = []
       longitude = []
       for eachpt in eachPair:
           latitude.append(eachpt[0])
           longitude.append(eachpt[1])
       points = nv.GeoPoint(latitude,longitude, degrees = True)
       nvectors = points.to_nvector()
       n_EM_E = nvectors.mean_horizontal_position()
       g_EM_E = n_EM_E.to_geo_point()
       lat, lon = g_EM_E.latitude_deg, g_EM_E.longitude_deg
       returnPeers.append((lat[0],lon[0]))

    return str(returnPeers)

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: great_circle(point, centroid).m)
    return tuple(centermost_point)


if __name__ == '__main__':
    app.run()
