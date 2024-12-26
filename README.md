## About SoundSensei

In the realm of music recommender systems, advanced technology and data analytics have spurred a transformative shift. This research delves into SoundSensei, a data-driven music recommendation system, aiming to uncover its profound implications and intricate technical foundations.

Driven by data analysis, music recommender systems play a pivotal role, serving over 35 billion hours of music globally on platforms like Spotify in 2020. SoundSensei operates within Spotify's dataset of 70 million tracks, using advanced machine learning and data analytics to craft recommendations that surpass personalization.

At its core, SoundSensei employs sophisticated data analysis techniques, from statistical modeling to precise methods, bridging the gap between chart-toppers and deeply personal musical choices. This project offers a comprehensive guide to the underlying algorithms and methodologies. Beyond personalization, SoundSensei excels in content safety, using NLP algorithms to curate kid-friendly music content, addressing digital-age challenges for parents.

## Description of packages
soundsensei <br>
|----> frontend <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|----> node_modules: Libraries and dependencies for the frontend. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|----> public: Public assets like HTML and image files. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|----> src: Source code for the frontend. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> css: Stylesheets for frontend styling. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> components: React components used in the frontend. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> pages: JavaScript files for different pages of the app. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> media: Media files like images used in the frontend. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> App.js: Defines the overall layout of the web application and is responsible for rendering the top-level component hierarchy. <br>
|&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;|----> index.js: Main entry points for the React app. <br>
| <br>
|----> api <br>
       |----> database<br>
       |&nbsp;&nbsp;&nbsp;&nbsp;|----> db.txt: Database related text file. <br>
       |----> static: Static files used by the API, like data visualizations. <br>
       |&nbsp;&nbsp;&nbsp;&nbsp;|----> (visualization images like viz2_audio_profile_box.png) <br>
       |----> service: Service scripts for data processing and analytics. <br>
       |&nbsp;&nbsp;&nbsp;&nbsp;|----> analytics_service.py: Includes functions for statistical analysis, data transformation, and generating recommendations.  <br>
       |&nbsp;&nbsp;&nbsp;&nbsp;|----> (other data files like train_data.csv) <br>
       |----> app.py: Main Python script for running the API. Consists of the initialization of the web application instance, and route definitions for API endpoints. This file acts as the dispatcher for incoming HTTP requests, directing them to the appropriate handling logic defined elsewhere in the application. <br>


## Installation and Execution Requirements
To install and set up this code, you need to have:

- Python 3.x
- Node.js and npm (for JavaScript frontend)
- Python libraries used in analytics_service.py (like pandas, numpy, tensorflow, etc.)

## Running the web app
- Step 1: Clone the repository or download the files to your local machine.
- Step 2: Run the backend by navigating to the  `api` directory and running:
```bash
python app.py
```
- Step 3: Run the frontend by navigating to the `frontend` directory and running:
```bash
npm install
npm start
```

### To see how to run and a demo of the web application, please see this video: https://youtu.be/sHr-8_At3Y4 


