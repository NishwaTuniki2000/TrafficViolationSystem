import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./Components/Home";
import UploadVideo from "./Components/UploadVideo";
import LiveCam from "./Components/LiveCam";
import RecordVideo from "./Components/RecordVideo";
import Results from "./Components/Results";

function App() {
  return (
    <Router>
      <div className="App">
        {/* Global navigation */}
        <nav style={{ marginBottom: "20px" }}>
          <Link to="/" style={{ marginRight: "10px" }}>Home</Link>
          <Link to="/upload" style={{ marginRight: "10px" }}>Upload Video</Link>
          <Link to="/live" style={{ marginRight: "10px" }}>Live Camera</Link>
          <Link to="/record" style={{ marginRight: "10px" }}>Record Video</Link>
          <Link to="/results">Results</Link>
        </nav>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<UploadVideo />} />
          <Route path="/live" element={<LiveCam />} />
          <Route path="/record" element={<RecordVideo />} />
          <Route path="/results" element={<Results />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
