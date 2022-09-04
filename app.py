from flask import Flask, jsonify, render_template
import requests
import base64

# To get your client ID and secret you need to make an app at the Spotify Developers page
# https://developer.spotify.com/ #


# To get your refresh token visit this website
# https://getyourspotifyrefreshtoken.herokuapp.com/ #

CLIENT_ID = 'CLIENT ID HERE'
CLIENT_SECRET = 'CLIENT SECRET HERE'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REFRESH_TOKEN = 'YOUR REFRESH TOKEN HERE'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return("Use /spotify to get the data")

@app.route('/spotify', methods=['GET'])
def spotify():
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': f'{REFRESH_TOKEN}'
    }
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii')).decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    access_token = response.json()['access_token']


    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get('https://api.spotify.com/v1/me/player/currently-playing', headers=headers).json()
    track = response['item']['name']
    album = response['item']['album']['name']
    cover = response['item']['album']['images'][0]['url']
    artists = ', '.join([artist['name'] for artist in response['item']['artists']])

    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get('https://api.spotify.com/v1/me/player/devices', headers=headers).json()
    device = response['devices'][0]['name']

    return jsonify(track, album, cover, artists, device)

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=80,
        debug=True
)
