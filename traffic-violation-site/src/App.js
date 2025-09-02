import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './Components/Home';
import UploadVideo from './Components/UploadVideo';
import LiveCam from './Components/LiveCam';
import RecordVideo from './Components/RecordVideo';
import Results from './Components/Results';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<UploadVideo />} />
        <Route path="/live" element={<LiveCam />} />
        <Route path="/record" element={<RecordVideo />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </div>
  );
}

export default App;
