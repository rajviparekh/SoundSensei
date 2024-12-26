
import '../css/analytics.css'; // Import the CSS for styling
import React, {useState} from 'react';
import { useLocation } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import NavBar from "../components/navbar";
import SliderColumn from '../components/slidercolumn';

const AnalyticsView = () => {
    const location = useLocation();
    const [images, setImages] = useState(location.state.images);
    const [audioFeatures, setAudioFeatures] = useState(location.state.audioFeatures)
    const [sliderChanged, setSliderChanged] = useState(false);

    const navigate = useNavigate();

    const [profanityFilter, setProfanityFilter] = useState(false);

    const handleProfanityToggle = () => {
        setProfanityFilter(!profanityFilter);
    };


    const handleSliderChange = (label) => (event) => {
        console.log(event);
        setSliderChanged(true);
        setAudioFeatures(prevFeatures => ({
            ...prevFeatures,
            [label]: event.target.value
        }));
    };
    const getRecommendations = async() => {
        let response = await axios.post(`http://localhost:3000/playlist/recommend`, {'audio_features': audioFeatures, 'profanity': profanityFilter, 'slider_changed': sliderChanged});
        console.log(response);
        navigate('/recommend', { state: { songs: response.data.recommendations} });
    }


    return (
        <div className={"flex flex-col"}>
            <NavBar/>
            <div className="plots-grid">
                <div className="plot">
                    <h1>Pizza Plot of Audio Features</h1>
                    <img src={images[0].url} alt="Plot 1" />
                </div>
                <div className="plot">
                    <h1>Box Plot of Audio features</h1>
                    <img src={images[1].url} alt="Plot 2" />
                </div>
                <div className="plot">
                    <h1>Top Genres</h1>
                    <img src={images[2].url} alt="Plot 3" />
                </div>
                <div className="plot">
                    <h1>Lyrics Wordcloud</h1>
                    <img src={images[3].url} alt="Plot 4" />
                </div>

                <div className="plot">
                    <h1>Emotion Audio Aura</h1>
                    <img src={images[4].url} alt="Plot 4" />
                </div>

                <div className="plot">
                    <h1>Proportion of vulgar songs above 25% threshold</h1>
                    <img src={images[5].url} alt="Plot 5" />
                </div>
                <h1 style={{'fontFamily': 'Lexend Peta', fontSize: '2rem', marginBottom: '-3%'}}>Control your recommendations!</h1>
                <SliderColumn audioFeatures = {audioFeatures} handleSliderChange = {handleSliderChange} profanityFilter = {profanityFilter} handleProfanityToggle = {handleProfanityToggle}/>
                <div className={"py-1.5 px-3 cursor-pointer bg-white text-black rounded-full"} id ={"recommend-songs-btn"} onClick={() => {getRecommendations()}}> 
                            Recommend Songs
                </div>
            </div>
        </div>

    );
};

export default AnalyticsView;