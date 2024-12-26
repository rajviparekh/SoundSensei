import React, { useState } from 'react';
import Slider from './slider';
import '../css/slider.css'



const SliderColumn = ({audioFeatures, handleSliderChange, profanityFilter, handleProfanityToggle}) => {

  return (
    <div className="slider-column">
      {Object.keys(audioFeatures).map((label, index) => (
        <Slider key={index} label = {label} value={audioFeatures[label]} onChange={handleSliderChange(label)} />
      ))}
      <div className="switch">
        <div className="slider-label-container">
          <label htmlFor="profanityToggle">Profanity Filter</label>
        </div>
        
        <div style={{
            width: '40px',
            height: '20px',
            backgroundColor: profanityFilter ? '#64D364' : '#ccc',
            borderRadius: '20px',
            position: 'relative',
            cursor: 'pointer',
            marginLeft: '-14%',
        }}
        onClick={handleProfanityToggle}>
            <input
                type="checkbox"
                id="profanityToggle"
                checked={profanityFilter}
                onChange={handleProfanityToggle}
                style={{
                    opacity: 0,
                    width: '40px',
                    height: '20px',
                    margin: 0,
                }}
            />
            <span style={{
                display: 'block',
                width: '18px',
                height: '18px',
                borderRadius: '50%',
                position: 'absolute',
                top: '1px',
                left: profanityFilter ? '20px' : '1px',
                backgroundColor: 'white',
                transition: 'left 0.2s',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
            }}></span>
        </div>
      </div>
    </div>
    
  );
};

export default SliderColumn;