import React, { useState } from "react";

export default function UploadVideo() {
  const [videoFile, setVideoFile] = useState(null);
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setVideoFile(e.target.files[0]);
    setViolations([]);
    setError(null);
  };

  const handleUpload = async () => {
    if (!videoFile) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", videoFile);

    try {
      const response = await fetch("/api/detect-video", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to process video");
      }

      const data = await response.json();
      setViolations(data.violations || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Upload Video for Traffic Violation Detection</h2>
      <input type="file" accept="video/*" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={!videoFile || loading}>
        {loading ? "Processing..." : "Upload & Detect"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {violations.length > 0 && (
        <div>
          <h3>Violations Detected:</h3>
          {violations.map((v, i) => (
            <div key={i} style={{ marginBottom: "20px" }}>
              <p>Frame: {v.frame}</p>
              {v.image_url && (
                <img
                  src={`/api${v.image_url}`}
                  alt={`Violation frame ${v.frame}`}
                  style={{ width: "300px", border: "1px solid black" }}
                />
              )}
              <pre>{JSON.stringify(v.detections, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
