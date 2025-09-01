import React from 'react';
import Home from './Components/Home';
import UploadVideo from './Components/UploadVideo';
import LiveCam from './Components/LiveCam';
import RecordVideo from './Components/RecordVideo'; // 
import Results from './Components/Results';

function App() {
  return (
    <div className="App">
      <Home />
      <UploadVideo />
      <LiveCam />
      <RecordVideo /> {/* Insert camera recording UI */}
      <Results />
    </div>
  );
}

export default App;
