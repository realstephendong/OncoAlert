import React from 'react';
import { NavLink } from 'react-router-dom';
import './Header.css';
import logo from '../images/logo.png';

const Header = () => {
  return (
    <header className="header">
      <div className="logo">
        <img src={logo} alt="Logo" />
        <span className="logo-text">OncoAlert</span>
      </div>
      <nav className="nav">
        <NavLink to="/home" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Home
        </NavLink>
        <NavLink to="/info" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Info
        </NavLink>
        <NavLink to="/test" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          Test
        </NavLink>
        <NavLink to="/about" className={({ isActive }) => (isActive ? 'nav-link active' : 'nav-link')}>
          About
        </NavLink>
      </nav>
    </header>
  );
};

export default Header;
