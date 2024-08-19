import React from 'react';
import Slider from 'react-slick';
import './Slider.css'; 
import { useNavigate } from 'react-router-dom';
import './ButtonStyles.scss'; // Import the button styles 

// Import images
import oralImage from '../../images/oral_cancer.jpg';
import kidneyImage from '../../images/kidney_cancer.jpg';
import breastImage from '../../images/breastcancerphoto.jpg';
import brainImage from '../../images/braincancerphoto.jpg';

// Image data
const images = [
  { src: oralImage, header: 'Oral Cancer', description: 'Description for oral cancer' },
  { src: kidneyImage, header: 'Kidney Cancer', description: 'Description for kidney cancer' },
  { src: breastImage, header: 'Breast Cancer', description: 'Description for breast cancer' },
  { src: brainImage, header: 'Brain Cancer', description: 'Description for brain cancer' },
];

function ImageSlider() {
  const navigate = useNavigate();

  const settings = {
    dots: true,
    infinite: true,
    speed: 1000,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 2500,
  };

  return (
    <div className="slider-container">
      <Slider {...settings}>
        {images.map((image, index) => (
          <div key={index} className="slide">
            <img src={image.src} alt={`Slide ${index + 1}`} className="slider-image" />
            <div className="slide-content">
              <h2 className="slide-header">{image.header}</h2>
              <p className="slide-description">{image.description}</p>
              <button className="button" onClick={() => navigate('/test')}>
                Test Image
              </button>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
}

export default ImageSlider;
