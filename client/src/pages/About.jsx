import React from 'react';
import './About.css';

function About() {
  return (
    <section id="about" className="about-footer">
      <h2>About the App</h2>
      <p>
        This app was developed to help users easily detect potential cancer through image analysis.
        IgnitionDetect utilizes advanced machine-learning algorithms and high-quality datasets to provide accurate and reliable cancer detection.
      </p>
      
      <h3>Our Team</h3>
      <ul className="team-list">
        <li><a href='https://www.linkedin.com/in/matei-brisca-47214a226/' target='_blank' rel="noopener noreferrer">Matei Brisca</a></li>
        <li><a href='#' target='_blank' rel="noopener noreferrer">Kostia Novosydliuk</a></li>
        <li><a href='https://www.linkedin.com/in/stephen-dong/' target='_blank' rel="noopener noreferrer">Stephen Dong</a></li>
        <li><a href='#' target='_blank' rel="noopener noreferrer">Brian Cheung</a></li>
      </ul>
      
      <h3>Contact Us</h3>
      <p>
        If you have any questions or need further information, feel free to contact us on LinkedIn/GitHub!
      </p>
      
      <h3>Learn More</h3>
      <p>
        Explore our <a href="https://www.kaggle.com/datasets/obulisainaren/multi-cancer/" target="_blank" rel="noopener noreferrer" className="learn-more-link">dataset</a> for more details about the data used in our tool.
      </p>
      
      <p>&copy; 2024 OncoAlert. All Rights Reserved.</p>
    </section>
  );
}

export default About;
