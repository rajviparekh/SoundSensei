import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import NavBar from "../components/navbar";
import { BgLeft } from "../components/svg";
import LoadingModal from '../components/loader'; // Ensure this path is correct
import '../css/home.css';

const PlaylistsView = ({ setAuthUrl }) => {
    const [playlists, setPlaylists] = useState([]);
    const [isLoading, setIsLoading] = useState(false); // State to track loading status
    const navigate = useNavigate();

    const getPlaylists = async () => {
        setIsLoading(true); // Set loading to true
        let response = await axios.get('http://localhost:3000/playlist');
        if(response && response.data && response.data.playlists){
            setPlaylists(response.data.playlists);
            setAuthUrl(null);
        } else {
            setAuthUrl(response.data.oauth_url);
        }
        setIsLoading(false); // Set loading to false
    };

    const handlePlaylistClick = (selectedPlaylist) => {
        navigate('/songs', { state: { selectedPlaylist } });
    };

    useEffect(() => {
        if (playlists.length === 0) {
            getPlaylists();
        }
    }, [playlists]);

    if (isLoading) {
        return <LoadingModal showModal={isLoading} />;
    } else {
        return (
            <div className={"flex flex-col"}>
                <NavBar />
                <div className={"flex flex-col items-center text-white my-gap page-body content"}>
                    <div className={"px-10 list-header my-gap"}>
                        Select a playlist to analyze:
                    </div>
                    <div className={"flex flex-col my-gap"} style={{width:"100%"}}>
                        {playlists.map((playlistItem, i) => (
                            <div key={i} className="song-item my-gap" onClick={() => handlePlaylistClick(playlistItem)} >
                                <div className={"list-num"}>
                                    {(i + 1).toString().padStart(2, '0')}
                                </div>
                                <div className={"list-name"}>
                                    {playlistItem.name}
                                </div>
                            </div>
                        ))}
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

export default PlaylistsView;
