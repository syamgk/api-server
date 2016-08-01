from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

#Create a engine for connecting to SQLite3.
#Assuming chinook.db is in your app root folder

e = create_engine('sqlite:///chinook.db')

app = Flask(__name__)
api = Api(app)

class Show_Artists(Resource):
	def get(self):
		#Connect to databse
		conn = e.connect()
		#Perform query and return JSON data
		query = conn.execute("select Name, ArtistId from artists")
		return {'artists names': dict( i for i in query.cursor) }

class Songs_Of_Artist(Resource):
    def get(self, artist_id):
    	conn = e.connect()
    	query = conn.execute("select * from albums where ArtistId='%i'"%int(artist_id) )
        #Query the result and get cursor.Dumping that data to a JSON is looked by extension
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return result
    #We can have PUT,DELETE,POST here. But in our API GET implementation is sufficient

class Playlists(Resource):
    def get(self):
        conn = e.connect()
        query = conn.execute("select distinct Name from playlists")
        return {'playlists': [i[0] for i in query.cursor.fetchall()]}  

api.add_resource(Songs_Of_Artist, '/artists/<string:artist_id>')
api.add_resource(Show_Artists, '/artists')
api.add_resource(Playlists,'/playlists')

if __name__ == '__main__':
    app.run( host='0.0.0.0', port=8080, debug=True)
