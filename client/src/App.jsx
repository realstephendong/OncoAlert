import React from 'react';
import { Route, Routes, useLocation, Navigate } from 'react-router-dom'; // Ensure Navigate is imported
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import Header from './headerlayout/Header';
import Home from './pages/Home';
import Info from './pages/Info';
import Test from './pages/Test';
import Footer from './footerlayout/Footer';
import About from './pages/About';
import './Transitions.css';
import './App.css';

function App() {
  const location = useLocation(); // Get the current location for transitions

  return (
    <>
      <Header />
      <div className="app-container">
        <TransitionGroup>
          <CSSTransition
            key={location.pathname}
            timeout={300}
            classNames="fade"
          >
            <Routes location={location}>
              <Route path="/" element={<Navigate to="/home" />} /> {/* Redirect root to /home */}
              <Route path="/home" element={<Home />} />
              <Route path="/info" element={<Info />} />
              <Route path="/test" element={<Test />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </CSSTransition>
        </TransitionGroup>
      </div>
      <Footer />
    </>
  );
}

export default App;
