import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      <h1>Welcome to the Traffic Violation Detection System</h1>
      <nav>
        <ul>
          <li><Link to="/upload">Upload Video</Link></li>
          <li><Link to="/live">Use Camera</Link></li>
        </ul>
      </nav>
    </div>
  );
}

export default Home;
