import React from 'react';
import logo from '../media/logo-transparent.png';
import {BgLeft} from "../components/svg";
import { useNavigate } from 'react-router-dom';
import '../css/home.css';

const Home = () => {
    const navigate = useNavigate();
    return (
        
        <div className={"container-fluid"} id={"home-container"}>
            <div className={"flex flex-col gap-20 justify-center items-center my-auto h-full"}>
                <div className={"flex flex-col justify-center items-center"}>
                    <div id={"home-logo-wrapper"}>
                    <img src={logo} height={300} width={300} alt=""/>              
            
                    <div className={"py-1.5 px-3 cursor-pointer bg-white text-black rounded-full"} id = {"home-upload-button"} onClick={() => {navigate("/playlists")}} style={{fontFamily: 'Lexend Peta'}}>
                            Upload your Spotify Playlist
                    </div>
                </div>
                </div>
                    <div id = {"home-animation-top"}>
                        <BgLeft />
                    </div>
                    <div id = {"home-animation-bottom"}>
                        <BgLeft />
                    </div>
            </div>
        </div>
   
    )
}

export default Home;