import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from "./pages/home";
import About from "./pages/about";
import PlaylistsView from "./pages/playlitsView";
import SongsView from "./pages/songsView";
import AnalyticsView from './pages/analyticsView';
import RecommenderView from './pages/recommenderView';
import ScrollToTop from './pages/scrollToTop'; 
import ContactUs from './pages/contactUs';

function App() {
    const [authUrl, setAuthUrl] = useState(null);
    
    useEffect(() => {
        if(authUrl != null){
            window.location.href = authUrl;
        }
    }, [authUrl]);

    return (
        <div className="bg-black min-h-screen text-white">
                <ScrollToTop />
                <Routes>
                    <Route path="/" element={<Home/>} />
                    <Route path="/about" element={<About />} />
                    <Route path="/contact" element={<ContactUs />} />
                    <Route path="/playlists" element={<PlaylistsView setAuthUrl = {setAuthUrl}/>} />
                    <Route path="/songs" element={<SongsView/>} />
                    <Route path="/analytics" element={<AnalyticsView/>} />
                    <Route path="/recommend" element={<RecommenderView/>} />
                </Routes>
        </div>
    );
}

export default App;
