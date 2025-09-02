import React from "react";
import { ReactMediaRecorder } from "react-media-recorder";

const RecordVideo = () => {
  return (
    <div>
      <h2 className="text-xl font-bold mb-4">Live Video Recorder</h2>
      <ReactMediaRecorder
        video
        render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
          <div>
            <p>Status: {status}</p>
            <video src={mediaBlobUrl} controls autoPlay className="w-full" />
            <div className="space-x-2 mt-2">
              <button
                onClick={startRecording}
                className="bg-green-600 text-white px-4 py-2 rounded"
              >
                Start Recording
              </button>
              <button
                onClick={stopRecording}
                className="bg-red-600 text-white px-4 py-2 rounded"
              >
                Stop Recording
              </button>
            </div>
            {mediaBlobUrl && (
              <form
                onSubmit={async (e) => {
                  e.preventDefault();
                  const response = await fetch(mediaBlobUrl);
                  const blob = await response.blob();
                  const file = new File([blob], "recorded-video.mp4", {
                    type: "video/mp4",
                  });
                  const formData = new FormData();
                  formData.append("video", file);

                  try {
                    const res = await fetch("/api/detect-video", {
                      method: "POST",
                      body: formData,
                    });

                    const data = await res.json();
                    alert("Upload successful: " + data.filename);
                  } catch (error) {
                    console.error("Upload error:", error);
                    alert("Failed to upload");
                  }
                }}
              >
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-4 py-2 rounded mt-3"
                >
                  Upload Recording
                </button>
              </form>
            )}
          </div>
        )}
      />
    </div>
  );
};

export default RecordVideo;
