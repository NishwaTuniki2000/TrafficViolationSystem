import React from 'react';

const Results = ({ violations = [], clipPath }) => {
  return (
    <div>
      <h2>Detection Results</h2>
      <p>Violations detected: {violations.length}</p>

      {/* Display violation frames info */}
      <ul>
        {violations.map((v, i) => (
          <li key={i}>
            Frame {v.frame}: {v.detections.length} detections
          </li>
        ))}
      </ul>

      {/* Display violation video clip if available */}
      {clipPath && (
        <div>
          <h3>Violation Video Clip</h3>
          <video controls width="600">
            <source src={`${process.env.REACT_APP_API_URL}/${clipPath}`} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
      )}
    </div>
  );
};

export default Results;
