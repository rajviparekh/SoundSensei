from flask import Flask, send_from_directory 
from flask import jsonify
from flask_cors import CORS

import os

import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 
from spotipy.oauth2 import SpotifyOAuth
from service.analytics_service import AnalyticsService
# import keras
# from keras import layers
# from keras import regularizers
# import tensorflow as tf

import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, roc_curve, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay
from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sklearn.linear_model import RidgeClassifier

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

from flask import Flask, redirect, request
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

# Your Spotify credentials
clientID = '8d29cf8d347641dcab869168e52e62e1'
clientSecret = 'd5cc0f865d014b329ee7a362855d4ec9'
scope = "playlist-read-private"
auth_callback_uri = 'http://localhost:3000/callback'  # Make sure this is added to your Spotify app as a valid redirect URI
auth = SpotifyOAuth(client_id=clientID, client_secret=clientSecret, scope=scope, redirect_uri=auth_callback_uri)



@app.route('/playlist', methods=['GET'])
def get_playlists():
    response = {}
    if(os.path.isfile('database/db.txt')):
        f = open("database/db.txt", "r")
        code = f.read()
        token_info = auth.get_access_token(code)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        playlists = sp.current_user_playlists()
        response = {"playlists": playlists["items"]}
    else:
        # Redirect to Spotify auth page
        auth_url = auth.get_authorize_url()
        response = {"oauth_url": auth_url}

    return jsonify(response)

@app.route('/songs', methods=['GET'])
def get_songs():

    # Get the playlist URI from query parameters
    playlist_uri = unquote(request.args.get('playlist_uri'))
    if not playlist_uri:
        return "Playlist URI is required", 400

    limit = int(request.args.get('limit'))
    offset = int(request.args.get('offset'))
    try:
        # Fetch playlist details
        f = open("database/db.txt", "r")
        code = f.read()
        token_info = auth.get_access_token(code)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        tracks = sp.playlist_tracks(playlist_uri, limit=limit, offset=offset)
        return jsonify({'songs': tracks["items"]})
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/playlist/analyze', methods=['GET'])
def analyzePlaylist():
    playlist_uri = unquote(request.args.get('playlist_uri'))
    if not playlist_uri:
        return "Playlist URI is required", 400
    try:
        # Fetch playlist details
        f = open("database/db.txt", "r")
        code = f.read()
        token_info = auth.get_access_token(code)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        analytics_service = AnalyticsService(sp)
        analysis_plots = analytics_service.analyze_playlist(playlist_uri)
        return analysis_plots
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/playlist/recommend', methods=['POST'])
def generateRecommendation():
    try:
        # Fetch playlist details
        request_data = json.loads(request.data)
        audio_features = request_data['audio_features']
        profanity = request_data['profanity']
        slider_changed = request_data['slider_changed']
        print('Slider Changed: ',slider_changed)
        f = open("database/db.txt", "r")
        code = f.read()
        token_info = auth.get_access_token(code)
        sp = spotipy.Spotify(auth=token_info['access_token'])
        analytics_service = AnalyticsService(sp)
        recommendations = analytics_service.generate_recommendation(use_custom_features=slider_changed, target_features=audio_features, profanity_filter=profanity)
        return recommendations
    except Exception as e:
        print(e)
        return f"An error occurred: {str(e)}", 500

    

@app.route('/analytics/audio-profile/plot',methods=['GET'])
def serve_plot1():
    return send_from_directory('static', 'viz1_audio_profile.png')

@app.route('/analytics/audio-profile-box/plot',methods=['GET'])
def serve_plot2():
    return send_from_directory('static', 'viz2_audio_profile_box.png')

@app.route('/analytics/genres/plot',methods=['GET'])
def serve_plot3():
    return send_from_directory('static', 'viz3_genres.png')

@app.route('/analytics/wordcloud/plot',methods=['GET'])
def serve_plot4():
    return send_from_directory('static', 'viz4_wordcloud.png')

@app.route('/analytics/audioaura/plot',methods=['GET'])
def serve_plot5():
    return send_from_directory('static', 'viz5_audioaura.png')

@app.route('/analytics/vulgarity/plot',methods=['GET'])
def serve_plot6():
    return send_from_directory('static', 'viz6_vulgarity.png')

@app.route('/callback')
def spotify_callback():

    # Spotify redirects here after user authenticates
    code = request.args.get('code')
    f = open("database/db.txt", "w")
    f.write(code)
    f.close()

    return redirect('http://localhost:3001/playlists')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

