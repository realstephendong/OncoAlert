import React from 'react';
import ImageSlider from './sliderlayout/Slider';
import './Home.css';
import { useNavigate } from 'react-router-dom';
import './sliderlayout/ButtonStyles.scss'; // Import the button styles

function Home() {
  const navigate = useNavigate();

  return (
    <section id="home">
      <ImageSlider />
      <div className="info-section">
        <h1 className="info-header">OncoAlert</h1>
        <div className="info-description-container">
          <p className="info-description">
            Our innovative cancer detection system utilizes cutting-edge technology to provide accurate and timely diagnosis, improving treatment outcomes and saving lives.
          </p>
        </div>
        <button className="button" onClick={() => navigate('/about')}>
          Know More 
        </button> 
      </div>
    </section>
  );
}

export default Home;
