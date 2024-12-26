import Logo from '../components/logo'
import React, {useState, useEffect} from 'react';
import { useLocation } from 'react-router-dom';
import LoadingModal from '../components/loader';
import '../css/songview.css';
import NavBar from "../components/navbar";
import axios from 'axios';
import {BgLeft} from "../components/svg";
import '../css/home.css';

const RecommenderView = () => {

    const location = useLocation();
    const [songs, setSongs] = useState(location.state.songs || null);

    
    if (songs.length === 0) {
        return <div>Loading songs...</div>;
    }
    else{
        return (
            <div className={"flex flex-col wrapper"}>
                {/* <LoadingModal showModal = {analyzingPlaylist}/> */}
                <NavBar/>
                <div className={"flex flex-col items-center text-white my-gap page-body content"}>
                    <div className={"px-10 list-header my-gap"}>
                        Your recommended songs:
                    </div>
                    <div className={"flex flex-col"} style={{width:"100%"}}>
                        {songs.map((song, i) => {
                            return (
                                <div key={i} className="song-item my-gap" >
                                    <div className={"list-num"} >
                                        {(i + 1).toString().padStart(2,'0')}
                                    </div>
                                    <div className={"list-name"} >
                                        {song}
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>
                <div id = {"home-animation-top"}>
                        <BgLeft />
                    </div>
                    <div id = {"home-animation-bottom"}>
                        <BgLeft />
                    </div>
            </div>
            
        )
    }
   
        
}

export default RecommenderView;