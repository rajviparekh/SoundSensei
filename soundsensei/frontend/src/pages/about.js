import React, { useState } from 'react';
import NavBar from "../components/navbar";
import { BgLeft } from "../components/svg";
import '../css/home.css';
import img1 from '../media/aboutdata_1.png';
import img2 from '../media/aboutdata_2.png';
import img3 from '../media/aboutdata_3.png';
import img4 from '../media/aboutdata_4.png';
import img5 from '../media/aboutdata_5.png';
import img6 from '../media/aboutdata_6.png';
import img7 from '../media/aboutdata_7.png';
import img8 from '../media/aboutdata_8.png';

const About = () => {
    // States to manage foldable sections
    const [showAudioFeatures, setShowAudioFeatures] = useState(false);
    const [showArtists, setShowArtists] = useState(false);
    const [showGenres, setShowGenres] = useState(false);

    // Function to render the arrow based on section visibility
    const renderArrow = (isVisible) => (
        <span style={{ display: 'inline-block', transform: isVisible ? 'rotate(0deg)' : 'rotate(-90deg)', transition: 'transform 0.3s ease' }}>
            ▼
        </span>
    );

    // Function to toggle visibility of sections
    const toggleSection = (section) => {
        if (section === "audioFeatures") setShowAudioFeatures(!showAudioFeatures);
        else if (section === "artists") setShowArtists(!showArtists);
        else if (section === "genres") setShowGenres(!showGenres);
    };

    return (
        <div className={"flex flex-col"}>
            <NavBar />
            <div className={"flex flex-col text-white my-gap page-body content"} style={{fontFamily: 'Lexend Peta'}}>
                {/* Existing About Text */}
                <div className={"px-10 my-gap"}>
                    <h2 className={"text-3xl font-bold mb-4"}>About SoundSensei</h2>
                        <p>In the realm of music recommender systems, advanced technology and data analytics have spurred a transformative shift. This research delves into SoundSensei, a data-driven music recommendation system, aiming to uncover its profound implications and intricate technical foundations.</p>
                        <br></br>
                        <p>Driven by data analysis, music recommender systems play a pivotal role, serving over 35 billion hours of music globally on platforms like Spotify in 2020. SoundSensei operates within Spotify's dataset of 70 million tracks, using advanced machine learning and data analytics to craft recommendations that surpass personalization.</p>
                        <br></br>
                        <p>At its core, SoundSensei employs sophisticated data analysis techniques, from statistical modeling to precise methods, bridging the gap between chart-toppers and deeply personal musical choices. This project offers a comprehensive guide to the underlying algorithms and methodologies. Beyond personalization, SoundSensei excels in content safety, using NLP algorithms to curate kid-friendly music content, addressing digital-age challenges for parents.</p>
                    <h1 className={"text-2xl font-bold mt-6 mb-4"}>About Our Dataset</h1>
                    <p>The SoundSensei dataset is a compilation of music tracks from the Billboard Top 100 charts across 6 decades, featuring a diverse array of audio features, artist information, and genre classifications. It encompasses a wide spectrum of data points, providing a deep insight into the musical preferences and trends across different demographics.</p>
                </div>
                <div className={"px-10 my-gap"}>
                    <h4 className={"text-2xl font-bold mt-6 mb-2 cursor-pointer"} onClick={() => toggleSection("audioFeatures")}>
                    {renderArrow(showAudioFeatures)} Understanding Audio Features
                    </h4>
                    {showAudioFeatures && (
                        <div>
                            <h1 className="text-center">Distribution of the Audio Features</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img1} height={300} width={700} alt="Audio Feature 1" />
                            </div>
                            <h1 className="text-center">Trends of Audio Features with respect to Time</h1>
                            <div style={{ display: 'flex', justifyContent: 'center' }}>
                                <img src={img2}  height={300} width={700} alt="Audio Feature 2" />
                            </div>
                        </div>
                    )}


                    <h4 className={"text-2xl font-bold mt-6 cursor-pointer"} onClick={() => toggleSection("artists")}>
                    {renderArrow(showArtists)} Understanding Artists
                    </h4>
                    {showArtists && (
                        <div>
                            <h1 className="text-center">Top 15 Artists from 1960-2021</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img3} height={300} width={700} alt="Artist 1" />
                            </div>

                            <h1 className="text-center">Trends in Hit Quality of Top 6 Artists with respect to Time</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img4} height={300} width={700} alt="Artist 2" />
                            </div>

                            <h1 className="text-center">Audio Profile of Top 6 Artists</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img5} height={300} width={700} alt="Artist 3" />
                            </div>

                            <h1 className="text-center">Top 5 Artists of the Top 6 Genres</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img6} height={300} width={700} alt="Artist 4" />
                            </div>

                        </div>
                    )}

                    <h4 className={"text-2xl font-bold mt-6 cursor-pointer"} onClick={() => toggleSection("genres")}>
                        {renderArrow(showGenres)} Understanding Genres
                    </h4>
                    {showGenres && (
                        <div>
                            
                            <h1 className="text-center">Top 15 Artist Genres from 1960-2021</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img7} height={300} width={700} alt="Genre 1" />
                            </div>

                            <h1 className="text-center">Trends in Hit Quality of Top 6 Artist Genres with respect to Time</h1>
                            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '5%'}}>
                                <img src={img8} height={300} width={700} alt="Genre 2" />
                            </div>

                        </div>
                    )}
                </div>
            </div>

            <div id={"home-animation-top"}>
                <BgLeft />
            </div>
            <div id={"home-animation-bottom"}>
                <BgLeft />
            </div>
        </div>
    );
}

export default About;

