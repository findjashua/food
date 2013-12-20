from flask import Flask
app = Flask(__name__)
from flask import render_template
import requests
import json
import pymongo
client = pymongo.MongoClient('mongodb://heroku_app20526236:n9tsd8c8ca53nuod7enkbo4ntv@ds061188.mongolab.com:61188/heroku_app20526236')
db = client['heroku_app20526236']

@app.route('/home')
def home():
	return render_template('home.html')

'''
@app.route('/init')
def init():
	r = requests.get('http://data.sfgov.org/resource/rqzj-sfat.json')
	trucks = r.json()
	for truck in trucks:
		if 'latitude' in truck and 'longitude' in truck:
			truck['loc'] = [float(truck['latitude']), float(truck['longitude'])]
	db.trucks.insert(trucks)
	return json.dumps(trucks)
'''

@app.route('/near/<lat>/<lng>')
def nearby(lat, lng):
	[lat, lng] = [float(loc) for loc in [lat, lng]]
	trucks = db.trucks.find({'loc': {'$near': [lat, lng]}}).limit(100)
	trucks = [delete_loc(truck) for truck in trucks]
	return json.dumps(trucks)

@app.route('/within/<swlat>/<swlng>/<nelat>/<nelng>')
def within(swlat, swlng, nelat, nelng):
	[swlat, swlng, nelat, nelng] = [float(loc) for loc in [swlat, swlng, nelat, nelng]]
	trucks = db.trucks.find({'loc': {'$within': {'$box': [[swlat, swlng], [nelat, nelng]]}}})
	trucks = [delete_loc(truck) for truck in trucks]
	return json.dumps(trucks)

def delete_loc(truck):
	del truck['_id']
	if truck.has_key('loc'):
		del truck['loc']
	return truck

if __name__ == '__main__':
	app.debug = True
	app.run()