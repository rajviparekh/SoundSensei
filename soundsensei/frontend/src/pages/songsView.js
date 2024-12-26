import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import axios from 'axios';
import Logo from '../components/logo';
import NavBar from "../components/navbar";
import { BgLeft } from "../components/svg";
import LoadingModal from '../components/loader'; // Ensure this path is correct
import '../css/songview.css';
import '../css/home.css';

const SongsView = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const [songs, setSongs] = useState([]);
    const [playlist, setPlaylist] = useState(location.state.selectedPlaylist || null);
    const [analyzingPlaylist, setAnalyzingPlaylist] = useState(false);
    const [isLoading, setIsLoading] = useState(false); // State to track loading status

    const getSongs = async (playlist) => {
        setIsLoading(true); // Set loading to true
        let playlistUri = playlist["uri"];
        let encodedUri = encodeURIComponent(playlistUri);
        let response = await axios.get(`http://localhost:3000/songs?playlist_uri=${encodedUri}&limit=50&offset=0`);
        console.log(response);
        if(response && response.data && response.data.songs){
            setSongs(response.data.songs);
        }
        setIsLoading(false); // Set loading to false
    };

    const analyzePlaylist = async () => {
        setAnalyzingPlaylist(true);
        let playlistUri = playlist["uri"];
        let encodedUri = encodeURIComponent(playlistUri);
        let response = await axios.get(`http://localhost:3000/playlist/analyze?playlist_uri=${encodedUri}`);
        console.log(response);
        setAnalyzingPlaylist(false);
        navigate('/analytics', { state: { images: response.data.analysis_images, audioFeatures: response.data.audio_feature_means } });
    };

    useEffect(() => {
        console.log(location);
        if (playlist) {
            getSongs(playlist);
        }
    }, [playlist]);

    if (isLoading) {
        return <LoadingModal showModal={isLoading} />;
    } else {
        return (
            <div className={"flex flex-col wrapper"}>
                <LoadingModal showModal={analyzingPlaylist} />
                <NavBar />
                <div className={"flex flex-col items-center text-white my-gap page-body content"}>
                    <div className={"px-10 list-header my-gap"}>
                        Your current songs:
                    </div>
                    <div className={"flex flex-col"} style={{width:"100%"}}>
                        {songs.map((song, i) => (
                            <div key={song.track.id} className="song-item my-gap" >
                                <div className={"list-num"} >
                                    {(i + 1).toString().padStart(2,'0')}
                                </div>
                                <div className={"list-name"} >
                                    {song.track.name}
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className={"py-1.5 px-3 cursor-pointer bg-white text-black rounded-full"} id={"analyze-playlist-btn"} onClick={analyzePlaylist}>
                        Analyze My Playlist
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
};

export default SongsView;
