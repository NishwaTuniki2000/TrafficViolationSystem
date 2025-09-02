import React, { useState, useEffect, useRef } from "react";

const LiveCam = () => {
  const [socket, setSocket] = useState(null);
  const videoRef = useRef(null);

  useEffect(() => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices
        .getUserMedia({ video: true })
        .then((stream) => {
          if (videoRef.current) {
            videoRef.current.srcObject = stream;
          }
        })
        .catch((err) => {
          console.error("Error accessing camera:", err);
          alert("Could not access camera. Please check permissions.");
        });
    }

    return () => {
      if (socket) socket.close();
      if (videoRef.current && videoRef.current.srcObject) {
        videoRef.current.srcObject.getTracks().forEach((t) => t.stop());
      }
    };
  }, [socket]);

  const startWebSocket = () => {
    if (socket) {
      alert("WebSocket already connected");
      return;
    }

    const ws = new WebSocket(`wss://${window.location.host}/api/live-video`);

    ws.onopen = () => {
      console.log("WebSocket connection established");
      alert("Live detection started");
    };

    ws.onmessage = (event) => {
      alert("Violation detected: " + event.data);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      alert("WebSocket error occurred");
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      alert("Live detection stopped");
      setSocket(null);
    };

    setSocket(ws);
  };

  const captureFrame = () => {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      alert("WebSocket is not connected. Start live detection first.");
      return;
    }
    if (videoRef.current) {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");
      canvas.width = videoRef.current.videoWidth;
      canvas.height = videoRef.current.videoHeight;
      ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
      const frameData = canvas.toDataURL("image/jpeg");
      socket.send(frameData);
    }
  };

  return (
    <div>
      <h2>Live Camera - Traffic Violation Detection</h2>
      <video
        ref={videoRef}
        width="600"
        height="400"
        autoPlay
        muted
        playsInline
        style={{ border: "1px solid black" }}
      />
      <div style={{ marginTop: "10px" }}>
        <button onClick={startWebSocket} style={{ marginRight: "10px" }}>
          Start Live Detection
        </button>
        <button onClick={captureFrame}>Capture Frame</button>
      </div>
    </div>
  );
};

export default LiveCam;
