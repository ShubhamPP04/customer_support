import React from 'react';
import { ChatProvider } from './context/ChatContext';
import { ChatWindow } from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <ChatProvider>
      <div className="App">
        <ChatWindow />
      </div>
    </ChatProvider>
  );
}

export default App;
