import pandas as pd
from IPython.display import HTML
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras import regularizers
import seaborn as sns
import time
import requests
import os
import wikipedia 
import spotipy 
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
from ast import literal_eval
import re
import math
import scipy
from copy import deepcopy
from fuzzywuzzy import fuzz 
from sklearn.preprocessing import MinMaxScaler, MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.ndimage import gaussian_filter
from matplotlib.ticker import PercentFormatter 

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mplsoccer import PyPizza, FontManager 
from highlight_text import fig_text, ax_text 
import matplotlib.patheffects as path_effects
from matplotlib.ticker import MaxNLocator
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap

from spotipy.oauth2 import SpotifyClientCredentials 
from spotipy.oauth2 import SpotifyOAuth
from lyricsgenius import Genius

from wordcloud import WordCloud 

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
from perspective import PerspectiveAPI
from flask import jsonify
from urllib.error import HTTPError

class AnalyticsService:

    def __init__(self,sp):
        # Things to make stuff pretty
        self.spotifyGreen = '#1dda63' 
        self.sp = sp
        authenticator = IAMAuthenticator('gGRtc-KuTDdhBnmqVU2WaEiZsJk2DU4dcHhXjzGwbpaK')
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(version='2023-04-01',authenticator=authenticator)
        # Set the service URL
        self.natural_language_understanding.set_service_url('https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/bdcc8e4f-f930-4845-b8d1-2255f06fc7f4')

    def analyze_playlist(self,playlist_uri):
        df = pd.read_csv('service/billboardOHE_lyrics.csv')
        print("Getting songs...")
        features_df, mean_dict = self.create_playlist_dataframe(playlist_uri,df)
        print("Getting lyrics...")
        features_df = self.get_lyrics(features_df) ## Calls Genius API
        print("Getting emotion/sentiment...")
        features_df['analysis'] = features_df['song_lyrics'].dropna().apply(self.analyze_text_emotion_and_sentiment)
        features_df[['sentiment', 'dominant_emotion']] = features_df['analysis'].apply(lambda x: pd.Series(self.extract_sentiment_and_emotion(x)))
        features_df = features_df[features_df['dominant_emotion'].notna()]
        emotion_columns = features_df['analysis'].apply(self.extract_emotions)
        features_df = pd.concat([features_df, emotion_columns], axis=1)
        
        features_df = self.get_toxic(features_df)
        print(features_df.columns)

        # Save user's dataframe
        features_df.to_csv('service/Playlistfeatures.csv')
        # Load in bigger dataset
        

        ############ VISUALIZATION 1
        print("Creating viz 1...")
        self.create_viz1(features_df, df)

        ############ VISUALIZATION 2
        print("Creating viz 2...")
        self.create_viz2(features_df)


        ############ VISUALIZATION 3
        print("Creating viz 3...")
        self.create_viz3(features_df)

        ############ VISUALIZATION 4
        print("Creating viz 4...")
        self.create_viz4(features_df)

        ############ VISUALIZATION 5
        print("Creating viz 5...")
        emotion_means = self.create_viz5(features_df)

        ############ VISUALIZATION 6
        print("Creating viz 6...")
        self.create_viz6(features_df[['Toxicity','Obscene','Identity_Attack','Insult','Threat','Sexual_Explicit']])

        # # Dominant emotion information
        emotion_means_dict = dict(emotion_means)
        # Calculate the total sum of the emotion values
        total = sum(emotion_means_dict.values())

        # Convert to percentages
        emotion_percentages = {emotion: value / total * 100 for emotion, value in emotion_means_dict.items()}
        print("Emotion percentages: ", emotion_percentages)

        return jsonify({
            "analysis_images": [
                {"url": "http://localhost:3000/analytics/audio-profile/plot"},
                {"url": "http://localhost:3000/analytics/audio-profile-box/plot"},
                {"url": "http://localhost:3000/analytics/genres/plot"},
                {"url": "http://localhost:3000/analytics/wordcloud/plot"},
                {"url": "http://localhost:3000/analytics/audioaura/plot"},
                {"url": "http://localhost:3000/analytics/vulgarity/plot"}
            ],
            "audio_feature_means": mean_dict
        })

    def generate_recommendation(self, use_custom_features=False, target_features=None, profanity_filter=0):
        # Load data
        print('Target Features:', target_features)
        df = pd.read_csv('service/train_data.csv', index_col=0)
        df = df.dropna()
        userdf = pd.read_csv('service/Playlistfeatures.csv', index_col=0)

        # Prepare user data
        userdf = userdf.drop(columns=['analysis', 'dominant_emotion', 'song_lyrics', 'Song','Artist Names', 'Artist(s) Genres'])
        # Initialize new one-hot encoded columns to 0
        userdf['sentiment_neutral'] = 0
        userdf['sentiment_positive'] = 0
        userdf['sentiment_negative'] = 0

        # One-hot encode the sentiment
        for index, row in userdf.iterrows():
            if row['sentiment'] == 'neutral':
                userdf.at[index, 'sentiment_neutral'] = 1
            elif row['sentiment'] == 'positive':
                userdf.at[index, 'sentiment_positive'] = 1
            elif row['sentiment'] == 'negative':
                userdf.at[index, 'sentiment_negative'] = 1

        # Optionally, drop the original 'sentiment' column if it's no longer needed
        userdf.drop('sentiment', axis=1, inplace=True)
        userdf = userdf.dropna()
        userdf.to_csv('service/train_user_data.csv')

        # Compute user profile
        traindf = df.drop(columns=['Song', 'Artist Names', 'Artist(s) Genres'])
        traindf = traindf.reindex(sorted(traindf.columns), axis=1)
        userdf = userdf.reindex(sorted(userdf.columns), axis=1)

        if use_custom_features:
            # Add feature distance to each song in df
            for feature in target_features:
                traindf[feature + '_distance'] = abs(traindf[feature] - float(target_features[feature]))

            # Calculate combined feature distance
            
            traindf['combined_feature_distance'] = traindf[[f'{feature}_distance' for feature in target_features]].sum(axis=1)
            
            # Apply profanity filter if enabled
            if profanity_filter:
                profanity_columns = ['Toxicity', 'Obscene', 'Identity_Attack', 'Insult', 'Threat', 'Sexual_Explicit']
                traindf = traindf[~traindf[profanity_columns].ge(0.5).any(axis=1)]
            # Calculate similarity
            traindf_filter = traindf.drop(columns=['Danceability_distance','Energy_distance', 'Instrumentalness_distance','Liveness_distance','Loudness_distance','Popularity_distance','Speechiness_distance','Tempo_distance','Valence_distance','combined_feature_distance', 'Acousticness_distance'])
            traindf_filter = traindf_filter.reindex(sorted(traindf_filter.columns), axis=1)
            X_train = traindf_filter.values.astype(np.float32) 
            
        else:
            X_train = traindf.values.astype(np.float32)

        X_user = userdf.values.astype(np.float32)

        
        # Define the encoder architecture 
        encoding_dim = 64  # The size of our encoded representations
        input_song = Input(shape=(X_train.shape[1],))  # Adjust the shape based on your input features
        encoded = Dense(encoding_dim, activation='relu', activity_regularizer=regularizers.l1(10e-5))(input_song)

        # Re-create the encoder model
        encoder = Model(input_song, encoded)

        # Load the saved weights
        encoder.load_weights('service/encoder_weights.h5')
        
        # Generate embeddings for train_data and train_user_data
        train_data_embeddings = encoder.predict(X_train)
        user_data_embeddings = encoder.predict(X_user)

        # Average the embeddings for the user's playlist
        user_playlist_embedding = np.mean(user_data_embeddings, axis=0).reshape(1, -1)

        # Compute similarity between the averaged user playlist embedding and all song embeddings in train_data
        similarity_scores = cosine_similarity(user_playlist_embedding, train_data_embeddings)
        
        if use_custom_features:
            traindf['combined_score'] = traindf['combined_feature_distance'] * -1 + similarity_scores.flatten()  # Adjust weights as necessary
            # Get top 10 recommendations based on combined score
            top_10_indices = traindf.sort_values(by='combined_score', ascending=False).head(10).index
        else:
            # Find the indices of the top 10 most similar songs
            top_10_indices = similarity_scores.argsort()[0][-10:]
        
        # Extract the recommended song names
        # recommended_songs = df.iloc[top_10_indices][['Song', 'Artist Names', 'Artist(s) Genres']]
        # recommended_songs['Artist'] = df['Artist Names'].apply(lambda x: x.strip("[,],'") if x else None)

        recommendations = df.iloc[top_10_indices]
        recommendations_for_user = recommendations["Song"].tolist()[0:10]
  
        return jsonify({
            "recommendations": recommendations_for_user
        })

    def path_effect_stroke(self,**kwargs):
        return [path_effects.Stroke(**kwargs), path_effects.Normal()]

    def get_audio_info(self,uris, batch_size=50):
        output = pd.DataFrame()

        # batches uris so fewer requests are sent
        for lower in tqdm(range(0, len(uris), batch_size)):
            audio_features_list = self.sp.audio_features(uris[lower:lower + batch_size])
            audio_features_list = [d for d in audio_features_list if d is not None]
            if isinstance(audio_features_list, list) and all(isinstance(item, dict) for item in audio_features_list):
                audio_features = audio_features_list
            else:
                audio_features = [audio_features_list]
            audio_df = pd.DataFrame.from_dict(audio_features)
            output = pd.concat([output, audio_df], ignore_index=True)

        return output

    def get_album_info(self,uris, batch_size=50):
        output = pd.DataFrame()

        #batches uris so fewer requests are sent
        for lower in tqdm(range(0, len(uris), batch_size)):
            albums = self.sp.albums(uris[lower:lower + batch_size])["albums"]
            albums = [d for d in albums if d is not None]
            album_df = pd.DataFrame.from_dict(albums)
            output = pd.concat([output, album_df], ignore_index=True)
        return output

    def get_track_info(self,uris, country, batch_size=50):
        output = pd.DataFrame()
        for lower in tqdm(range(0, len(uris), batch_size)):
            tracks = self.sp.tracks(uris[lower:lower + batch_size], market=country)["tracks"]
            tracks = [d for d in tracks if d is not None]
            track_df = pd.DataFrame.from_dict(tracks)
            output = pd.concat([output, track_df], ignore_index=True)
        return output

    def get_artist_info(self,uris, batch_size=50):
        output = pd.DataFrame()

        for lower in tqdm(range(0, len(uris), batch_size)):
            artist = self.sp.artists(uris[lower:lower + batch_size])['artists']
            artist_df = pd.DataFrame.from_dict(artist)
            output = pd.concat([output, artist_df], ignore_index=True)

        return output

    def count_occurances(self,d, l):
        for item in l:
            if item in d:
                d[item] += 1
            else:
                d[item] = 1   

    def print_playlist_names(self,playlists):
        for _, i in enumerate(playlists['items']): # list of dictionaries
            print(_, i['name'])
        
    def create_playlist_dataframe(self,example_playlist_uri,df):
        playlist = self.sp.playlist(example_playlist_uri)
        items = []

        for i in range(0,  playlist["tracks"]["total"], 100):
            items += self.sp.playlist_tracks(example_playlist_uri, limit=100, offset=i)["items"]

        track_ids = []
        album_ids = []
        artist_ids = []
        add_dates = []

        for item in items:
            track_ids.append(item["track"]["id"])
            album_ids.append(item["track"]["album"]["id"])
            add_dates.append(item["added_at"])
            #TODO consider all artists instead of just the first
            artist_ids.append(item["track"]["artists"][0]["id"])

        audio_df = self.get_audio_info(track_ids)
        track_df = self.get_track_info(track_ids, "US")
        add_df = pd.Series(add_dates).to_frame("added_on")

        features_df = pd.concat([track_df[["name", "popularity", "preview_url"]], audio_df], axis="columns").reset_index(drop=True)
        features_df = pd.concat([features_df, add_df], axis="columns").reset_index(drop=True)

        #album_df = get_album_info(album_ids)                          #dont think theres anything super useful in here
        artist_df = self.get_artist_info(artist_ids).reset_index(drop=True)
        artist_df.rename(columns={'name': 'artist'}, inplace=True)

        features_df = pd.concat([artist_df[["artist", "genres"]], features_df], axis="columns")
        features_df = features_df[['artist','genres','name','popularity','danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms']]

        # Mapping of old column names to new column names
        column_mapping = {
            'artist': 'Artist Names',
            'genres': 'Artist(s) Genres',
            'name': 'Song',
            'popularity': 'Popularity',
            'danceability': 'Danceability',
            'energy': 'Energy',
            'loudness': 'Loudness',
            'speechiness': 'Speechiness',
            'acousticness': 'Acousticness',
            'instrumentalness': 'Instrumentalness',
            'liveness': 'Liveness',
            'valence': 'Valence',
            'tempo': 'Tempo',
            'duration_ms': 'Duration'  
        }

        # Renaming the columns
        features_df.rename(columns=column_mapping, inplace=True)

        # Extract unique artist names from the existing one-hot encoded DataFrame
        unique_artists = [col.replace('Artist: ', '') for col in df.columns if col.startswith('Artist: ')]

        # Initialize the columns in the new DataFrame
        for artist in unique_artists:
            features_df[f'Artist: {artist}'] = 0

        # Set the appropriate column to 1 for each row in the new DataFrame
        for index, row in features_df.iterrows():
            artist_col = f'Artist: {row["Artist Names"]}'
            if artist_col in features_df.columns:
                features_df.at[index, artist_col] = 1

        # Extract unique genres from the existing DataFrame
        unique_genres = [col.replace('Genre: ', '') for col in df.columns if col.startswith('Genre: ')]

        # Initialize the genre columns in the new DataFrame
        for genre in unique_genres:
            features_df[f'Genre: {genre}'] = 0

        # Set the appropriate genre columns to 1 for each row in the new DataFrame
        for index, row in features_df.iterrows():
            if isinstance(row['Artist(s) Genres'], list):
                for genre in row['Artist(s) Genres']:
                    genre_col = f'Genre: {genre}'
                    if genre_col in features_df.columns:
                        features_df.at[index, genre_col] = 1
        
        # Normalize as they are on a different scale
        mean_df = features_df
        scaler = MinMaxScaler()
        numerical_features = ['Popularity', 'Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Loudness', 'Speechiness', 'Tempo', 'Valence']
        mean_df[numerical_features] = scaler.fit_transform(mean_df[numerical_features])
        mean_dict = mean_df[numerical_features].describe().loc['mean'].to_dict()
        
        return features_df, mean_dict
        
    def clean_lyrics(self, df_o, inplace=False):
        if not inplace:
            df = df_o.copy()
        else:
            df = df_o

        df_na = df.isna()
        for index, lyrics in enumerate(df['song_lyrics']):
            if df_na.iloc[index]['song_lyrics']:
                continue

            rc = re.compile("^.*Contributor.*Lyrics")
            s = rc.sub("", lyrics )
            rc = re.compile("\[.*\]")
            s = rc.sub("", s)
            rc = re.compile("You might.*Embed$")
            s = rc.sub( "", s)
            rc = re.compile(r"\d*Embed$")
            s = rc.sub("", s).split()

            s = "".join([i+ " " for i in s])

            df.at[index, "song_lyrics"] = s
        if not inplace:
            return df
    
    def get_lyrics(self,features_df):
        client_id = 'afaixXQGd2TNw0XgeCVvgfKfTFJMxVzWDLWui8u1COCTjeh7WM2LSWSYIYS7CZDN'
        client_secret = 'UN-cUCsqu5JJBV7v92jgE3_0s6Ru_5FxrlJygWRufgN_LezVdnNY4XlYFFfZTQ-yMMf2jQaDEuL6qYs1VxWrMw'
        client_access_token = 'bovKxxW-6PLBu5LgT_d-RXvIejYmnRNfCmfoDBFZgT6te-Ea8QtQ9K2ybxdd2Euq'
        # Making a song lyrics column
        features_df['song_lyrics'] = None
        # Querying all songs in the dataframe for lyrics
        for index, song_name in enumerate(features_df['Song']):
            try:
                genius = Genius(client_access_token) # Initialising the Genius API
                last_idx = index
                song = genius.search_song(features_df['Song'].iloc[index], features_df['Artist Names'].iloc[index])
                if song != None:
                    features_df.iloc[index, -1] = song.lyrics
            except:
                # If the API produces a connection timeout error, waiting for 2 mins and trying again
                print("CONNECTION TIMEOUT")
                connect_timeout_idx = index
                time.sleep(120)
                genius = Genius(client_access_token)
                last_idx = index
                song = genius.search_song(features_df['Song'].iloc[index], features_df['Artist Names'].iloc[index])
                if song != None:
                    features_df.iloc[index, -1] = song.lyrics

        # List of words to be removed from the lyrics, in lowercase
        remove_words = ['chorus', 'verse', 'pre-chorus', 'bridge', 'intro', 'outro', 'instrumental', 'hook', 'lyrics', 'contributors', 'Translations']
        for name, artist in zip(features_df['Song'], features_df['Artist Names']):
            remove_words.append(name)
            remove_words.append(artist)
        pattern = '|'.join(re.escape(word) for word in remove_words)
        pattern += r'|\b\d+\b|[^\w\s]'
        features_df['song_lyrics'] = features_df['song_lyrics'].str.replace(pattern, '', regex=True, case=False)
        
        features_df = self.clean_lyrics(features_df)
        
        return features_df

    def get_toxic(self, df_o, inplace=False, local=False):
        p = PerspectiveAPI('AIzaSyAyP-nQY3uWDVvaqfF3SIULohtAsFMMgKA')
        if not inplace:
            df = df_o.copy()
        else:
            df = df_o

        df['Toxicity'] = None #-7
        df['Severe_Toxicity'] = None #-6
        df['Obscene'] = None #-5
        df['Identity_Attack'] = None #-4
        df['Insult'] = None #-3
        df['Threat'] = None #-2
        df['Sexual_Explicit'] = None #-1

        df_na = df.isna()
        for index, lyrics in enumerate(df['song_lyrics']):
            try:
                if df_na.iloc[index]['song_lyrics']:
                    continue

                if local:
                    toxic_info = Detoxify('unbiased').predict(lyrics)
                else:
                    categories = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'THREAT','OBSCENE','SEXUALLY_EXPLICIT']
                    try:
                        toxic_info_upper = p.score(lyrics, categories)
                        time.sleep(1)
                    except Exception as e:
                        print('An exception occured: ', str(e))
                        if e.code != 429:
                            continue
                        print("sleeping for 15 seconds")
                        time.sleep(15)
                        toxic_info_upper = p.score(lyrics, categories)

                    print(index, " done")
                    toxic_info = {}
                    toxic_info.update([(key.lower(), val) for key, val in toxic_info_upper.items()])
                    toxic_info["sexual_explicit"] = toxic_info.pop("sexually_explicit")

                df.iloc[index, -1] = toxic_info['sexual_explicit']
                df.iloc[index, -2] = toxic_info['threat']
                df.iloc[index, -3] = toxic_info['insult']
                df.iloc[index, -4] = toxic_info['identity_attack']
                df.iloc[index, -5] = toxic_info['obscene']
                df.iloc[index, -6] = toxic_info['severe_toxicity']
                df.iloc[index, -7] = toxic_info['toxicity']
            except Exception as e:
                print('An exception occured: ', str(e))
                continue
        if not inplace:
            return df
    
    def analyze_text_emotion_and_sentiment(self,text):
        try:
            response = self.natural_language_understanding.analyze(
                text=text,
                features=Features(
                    emotion=EmotionOptions(),
                    sentiment=SentimentOptions()
                )).get_result()
            return response
        except Exception as e:
            return str(e)

    def extract_sentiment_and_emotion(self,analysis):
        try:
            analysis_dict = analysis
            sentiment = analysis_dict.get('sentiment', {}).get('document', {}).get('label', '')
            emotions = analysis_dict.get('emotion', {}).get('document', {}).get('emotion', {})
            dominant_emotion = max(emotions, key=emotions.get) if emotions else np.nan
            
            return sentiment, dominant_emotion
        except Exception as e:
            return np.nan, np.nan

    def extract_emotions(self,analysis_dict):
        try:
            # Extract emotions and their weights
            emotions = analysis_dict.get('emotion', {}).get('document', {}).get('emotion', {})
            return pd.Series(emotions)
        except json.JSONDecodeError:
            # Return NaN for each emotion if parsing fails
            return pd.Series({'sadness': None, 'joy': None, 'fear': None, 'disgust': None, 'anger': None})

    def create_viz1(self,features_df, df):
        # Audio Profiles
        # Setting the color and linewidth of the spines/borders
        mpl.rc('axes',edgecolor='white')
        mpl.rc('axes',linewidth='2')

        # Creating subplots as polar plots and adjusting them
        fig,ax = plt.subplots(figsize=(10,8),subplot_kw=dict(projection='polar'))
        plt.subplots_adjust(wspace=0.3,hspace=0.3)
        fig.set_facecolor('#181818')

        # List of features for the pizza chart
        featColumns = ['Popularity','Acousticness','Danceability','Energy','Instrumentalness','Loudness','Speechiness','Tempo','Valence']

        # Font colors and slice colors for Pizza chart
        slice_colors = [self.spotifyGreen]*9
        text_colors = ['k']*9

        # instantiating PyPizza class
        baker = PyPizza(
                            params=featColumns,
                            background_color="#181818",
                            straight_line_color="#979797",
                            straight_line_lw=3,
                            straight_line_ls='-',
                            last_circle_color="#979797",
                            last_circle_lw=7,
                            last_circle_ls='-',
                            other_circle_lw=2,
                            other_circle_color='#595959',
                            other_circle_ls='--',
                            inner_circle_size=20
                        )

        # Path effects object for getting the outline/stroke for text
        pe1 = self.path_effect_stroke(linewidth=2, foreground="w")


        # Getting data for each artist
        artistData = features_df[featColumns]
        
        # Setting artist as title
        # ax.set_title(top6Artists[idx].title(), pad=40,fontsize=24, color='w')
        # Calculating mean percentile ranks for each feature
        values = []
        try:
            for idx in range(len(artistData)):
                songFeats = list(artistData.loc[idx])
                valuesSong = []
                for x in range(len(featColumns)):
                    valuesSong.append(math.floor(scipy.stats.percentileofscore(df[featColumns[x]],songFeats[x])))
                values.append(valuesSong)
        except Exception as e:
            print("An exception in viz 1", str(e))
        if(len(values)>0):
            values = np.round(np.mean(values, axis=0)).astype(int)
        # Plotting the Pizza chart
        baker.make_pizza(
                            values,
                            figsize=(6, 8),
                            ax=ax,
                            color_blank_space=['#181818']*9,
                            slice_colors=slice_colors,
                            value_bck_colors=slice_colors,
                            param_location=110,
                            blank_alpha=1,
                            kwargs_slices=dict(edgecolor="w", zorder=2, linewidth=3,alpha=.9,linestyle='-'),
                            kwargs_params=dict(color="w", fontsize=16, fontweight='bold',
                                                va="center"),
                            kwargs_values=dict(color="k", fontsize=14,va='center',path_effects=pe1,
                                                zorder=3,
                                                bbox=dict(edgecolor="w",boxstyle="round,pad=0.2", lw=2.5))
                        )
        print('Saving viz 1...')
        plt.savefig('static/viz1_audio_profile.png',transparent=True,bbox_inches='tight')
        
    def create_viz2(self,features_df):
        features_to_plot = ['Tempo', 'Danceability', 'Valence', 'Energy', 'Acousticness', 'Liveness', 'Loudness', 'Speechiness']
        data_features = features_df[features_to_plot]

        plt.figure(figsize=(12, 7), facecolor='#181818')

        # Create a boxplot with the specified color settings and green outline for the boxes
        sns.boxplot(data=data_features, linewidth=2, fliersize=5, palette="muted",
                    boxprops=dict(edgecolor="green"), whiskerprops=dict(color="green"),
                    capprops=dict(color="green"), medianprops=dict(color="green"),
                    flierprops=dict(markerfacecolor='g', marker='o', markersize=5))

        # Setting the title and labels with the appropriate color
        # plt.title('Boxplot of Playlist Audio Features', color='white', fontsize=24, fontweight='bold', pad=20)
        plt.ylabel('Normalized Value', color='white', fontsize=15, fontweight='bold',labelpad=20)
        plt.xlabel('Audio Features', color='white', fontsize=15, fontweight='bold',labelpad=20)

        # Changing the color of the tick labels
        plt.xticks(color='white',fontsize=12)
        plt.yticks(color='white',fontsize=13)

        # Setting grid
        # plt.grid(color='#979797', linestyle='--', linewidth=0.5)

        # Changing figure and axis properties to match the dark theme
        ax = plt.gca()
        ax.set_facecolor('#181818')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')

        # Show the plot
        plt.savefig('static/viz2_audio_profile_box.png',transparent=True,bbox_inches='tight')

    def create_viz3(self,features_df):
        #finds counts of genres for a playlist
        genres = {}
        for row in features_df["Artist(s) Genres"]:
            self.count_occurances(genres, row)

        genres_df = pd.Series(genres).to_frame("count")

        genres_df = genres_df.sort_values(by=["count"], ascending=False)[:5]
        genres_df = genres_df.reset_index()
        
        def to_camel_case(text):
            words = text.split()
            return ' '.join(word.capitalize() for word in words)

        genres_df['index'] = [to_camel_case(idx) for idx in genres_df['index']]

        ## Setting the color and linewidth of the spines/borders
        mpl.rc('axes',edgecolor='white')
        mpl.rc('axes',linewidth='0')

        # Adding background color and gridlines
        fig,ax = plt.subplots(figsize=(10,8))
        fig.set_facecolor('#181818')
        ax.patch.set_facecolor('#181818')
        ax.set_axisbelow(True)
        ax.grid(color='#bdbdbd',which='major',linestyle='--',alpha=0.35)

        scaler = MinMaxScaler(feature_range=(0.25,1))
        # Using the normalized hit quality values as alpha values
        alphaList = scaler.fit_transform(genres_df['count'].values.reshape(-1,1)).flatten().tolist()

        # Inverting the y-axis to show the aritst with highest quality on the top
        ax.invert_yaxis()

        # Looping through each row and plotting a horizontal bar
        for index,row in genres_df.iterrows():
            ax.barh(genres_df['index'][index],genres_df['count'][index],height=0.65,color=self.spotifyGreen,alpha=alphaList[index])
        # Plotting the horizontal bars for each Artist as outline
        bars = ax.barh(genres_df['index'],genres_df['count'],height=0.65,
                    color='None',edgecolor='w',ls='-',linewidth=2.5)

        # Customizing the tick-labels for both the axes
        plt.yticks(fontsize=9,color='white')
        plt.xticks(fontsize=10,color='white')
        plt.xlabel('Count',labelpad=10,fontsize=14,color='white')

        plt.savefig('static/viz3_genres.png',transparent=True,bbox_inches='tight')

    def create_viz4(self,features_df):
        # Concatenate all the lyrics into one text string
        all_lyrics = ' '.join(features_df['song_lyrics'].dropna()).lower()  # Convert to lower case for case-insensitive removal

        # Generate the word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='black').generate(all_lyrics)

        # Display the generated word cloud
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')  # Remove the axis
        plt.savefig('static/viz4_wordcloud.png',transparent=True,bbox_inches='tight')

    def create_viz5(self,features_df):
        
        emotions = ['sadness', 'joy', 'fear', 'disgust', 'anger']

        emotion_means = features_df[emotions].mean()
        colors = ['#0d72ea', '#f72d93', '#d64000', '#088569', '#d64000']
        cmap = LinearSegmentedColormap.from_list("my_cmap", colors)

        # Coordinates for the focal points of the emotions
        coordinates = [(0.1, 0.3), (0.0, 0.9), (0.8, 0.2), (0.4, 0.9), (0.7, 0.7)]


        fig, ax = plt.subplots(figsize=(2, 2))

        for j, emotion in enumerate(emotions):
            score = emotion_means[emotion]
            x, y = coordinates[j]
            ax.scatter(x, y, s=score * 80000, alpha= 0.7, c=cmap(j / len(emotions)), edgecolors='none')
        ax.axis('off')
        plt.tight_layout()
        
        # Capture the figure as an image
        fig.canvas.draw()
        image_with_custom_legend = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image_with_custom_legend = image_with_custom_legend.reshape((200, 200, 3))

        # Apply Gaussian blur to the image
        blurred_image_with_custom_legend = gaussian_filter(image_with_custom_legend, sigma=(30, 30, 0))

        # Show the blurred image with custom legend
        plt.figure(figsize=(3, 3))
        plt.imshow(blurred_image_with_custom_legend)
        plt.axis('off')

        # plt.savefig('audioaura.png', transparent=True)
        # Create custom legend with small boxes for each emotion
        
        legend_elements = [Patch(facecolor=cmap(i / len(emotions)), edgecolor='none', label=emotion) for i, emotion in enumerate(emotions)]
        plt.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=len(emotions), frameon=False, labelcolor='white')
        plt.tight_layout()
        plt.savefig('static/viz5_audioaura.png',transparent=True, bbox_inches='tight')
        
        return emotion_means
    
    def create_viz6(self,features_df):
        features_df = features_df.dropna()
        print(features_df)
        features_df = features_df.applymap(lambda i: i >= 0.25)

        fig, ax = plt.subplots(figsize=(10, 4), facecolor='#181818')
        print(features_df.melt(var_name='Content Type', value_name='Key'))
        sns.histplot(data=features_df.melt(var_name='Content Type', value_name='Key'), y='Content Type', hue='Key',
                stat="percent", multiple='fill', discrete=True, shrink=0.8,
                palette=["grey", self.spotifyGreen], alpha=1, ax=ax, linewidth=0)

        sns.despine()
        sns.move_legend(ax, bbox_to_anchor=(1.01, 1.02), loc='upper left')
        ax.xaxis.set_major_formatter(PercentFormatter(1))

        for p in ax.patches:
            h, w, x, y = p.get_height(), p.get_width(), p.get_x(), p.get_y()
            if(w > .1):
                text = f'{w * 100:0.2f} %'
                ax.annotate(text=text, xy=(x + w / 2, y + h / 2), ha='center', va='center', color='black', size=10)

        plt.xlabel("Proportion", color="white", fontsize=20, fontweight='bold',labelpad=20)
        plt.ylabel("Features", color="white", fontsize=20, fontweight='bold',labelpad=20)
        # plt.title(f"Proportion of songs above {thresh * 100:0.2f}% threshold", color='white', fontsize=24, fontweight='bold', pad=20)
        plt.tight_layout()

        plt.xticks(color='white',fontsize=14)
        plt.yticks(color='white',fontsize=18)
        ax.set_facecolor('#181818')
        plt.savefig('static/viz6_vulgarity.png',transparent=True, bbox_inches='tight')
        