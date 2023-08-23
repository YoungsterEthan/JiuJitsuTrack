import React, { useState, useRef } from 'react';

function VideoPlayer() {
    const [videoSrc, setVideoSrc] = useState(null);
    const videoRef = useRef(null);
    const canvasRef = useRef(null);

    const handleVideoChange = (event) => {
        const file = event.target.files[0];
        const videoURL = URL.createObjectURL(file);
        setVideoSrc(videoURL);
    };

    const viewCanvasContent = () => {
        const canvas = canvasRef.current;
        const dataURL = canvas.toDataURL();
        const newWindow = window.open('about:blank');
        newWindow.document.write('<img src="' + dataURL + '" alt="Canvas Content"/>');
    };

    const handleVideoClick = async (event) => {
        const video = videoRef.current;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        // Pause the video
        video.pause();

        // Set the canvas dimensions to match the video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

// Draw the current frame onto canvas
ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        console.log('Canvas has been drawn with the current video frame.');


        const x = event.clientX - video.getBoundingClientRect().left;
        const y = event.clientY - video.getBoundingClientRect().top;

        canvas.toBlob(async (blob) => {
            const formData = new FormData();
            formData.append('image', blob);

            const response = await fetch('http://127.0.0.1:5000/detect', {
                method: 'POST',
                body: formData,
            });

            const boxes = await response.json();
            console.log("BOXES")
            console.log(boxes)
            boxes.forEach(box => {
                const width = box.x2 - box.x1;
                const height = box.y2 - box.y1;

                ctx.strokeStyle = 'red';
                ctx.lineWidth = 3;
                ctx.strokeRect(box.x1, box.y1, width, height);
            });
        });
    };



    return (
        <div>
            <input type="file" accept="video/*" onChange={handleVideoChange} />
            {videoSrc && (
                <div>
                    <div className="video-container">
                        <video ref={videoRef} onClick={handleVideoClick} controls>
                            <source src={videoSrc} type="video/mp4" />
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <div className="canvas-container">
                        <canvas ref={canvasRef} style={{position: 'absolute', top: '0', left: '0', pointerEvents: 'none', backgroundColor: 'rgba(255,255,255,0.5)'}}></canvas>
                        <button onClick={viewCanvasContent}>View Canvas Content</button> {/* Added button */}
                    </div>
                </div>
            )}
        </div>
    );

}

export default VideoPlayer;
