import React from 'react';
import './Footer.css';
import logo from '../images/logo.png';

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section logo">
          <img src={logo} alt="Logo" className="footer-logo" />
          <div className="footer-logo-text">OncoAlert</div>
        </div>
        <div className="footer-section about">
          <h2>About Us</h2>
          <p>
            We are dedicated to providing innovative solutions for cancer detection. Our mission is to improve lives through advanced technology and cutting-edge research.
          </p>
        </div>
        <div className="footer-section links">
          <h2>Quick Links</h2>
          <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/info">Info</a></li>
            <li><a href="/test">Test</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; 2024 OncoAlert. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
