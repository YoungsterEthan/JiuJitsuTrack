import React from 'react';
import './App.css';
import VideoPlayer from './VideoPlayer';

function App() {
  return (
      <div className="App">
          <header className="App-header">
              <h1>Upload and Play Video</h1>
          </header>
          <div style={{ clear: 'both' }}>
              <VideoPlayer />
          </div>
      </div>
  );
}

export default App;

