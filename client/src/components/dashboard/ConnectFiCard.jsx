import React, { useState, useEffect, useRef } from 'react';

// Mock logs that will be displayed in the terminal
const mockLogs = [
  { text: '> Initializing secure connection to Fi...', delay: 800 },
  { text: '> Establishing encrypted channel...', delay: 1200 },
  { text: '> Verifying API endpoints...', delay: 1000 },
  { text: '> Loading user financial profiles...', delay: 1500 },
  { text: '> Fetching account data...', delay: 1800 },
  { text: '> Decrypting transaction history...', delay: 1600 },
  { text: '> Analyzing spending patterns...', delay: 2000 },
  { text: '> Preparing financial insights...', delay: 1400 },
  { text: '> Connection to Fi established successfully!', delay: 1000, success: true }
];

const ConnectFiCard = () => {
  const [connecting, setConnecting] = useState(false);
  const [logs, setLogs] = useState([]);
  const [currentLogIndex, setCurrentLogIndex] = useState(0);
  const [typingText, setTypingText] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const [connected, setConnected] = useState(false);
  const terminalRef = useRef(null);

  // Blinking cursor effect
  useEffect(() => {
    const cursorInterval = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 500);
    
    return () => clearInterval(cursorInterval);
  }, []);

  // Scroll terminal to bottom when new logs come in
  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs, typingText]);

  // Start connection process
  const handleConnect = async () => {
    setConnecting(true);
    setLogs([]);
    setCurrentLogIndex(0);
    setTypingText('');
    
    try {
      // Call the run-initial-pipeline API
      const response = await fetch('http://localhost:8000/ai/run-initial-pipeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`API call failed with status: ${response.status}`);
      }
      
      // Get the response data
      const data = await response.json();
      console.log('Pipeline initialization successful:', data);
      
      // Continue with the mock log simulation
      simulateNextLog();
      
    } catch (error) {
      console.error('Error connecting to Fi:', error);
      // Add error log to the terminal
      setLogs(prevLogs => [...prevLogs, { 
        text: `> Error: ${error.message || 'Failed to connect to Fi services'}`, 
        delay: 0, 
        error: true 
      }]);
      // Wait a moment then reset the connection state
      setTimeout(() => {
        setConnecting(false);
      }, 2000);
    }
  };

  // Handle typing effect and log simulation
  const simulateNextLog = () => {
    if (currentLogIndex >= mockLogs.length) {
      setConnected(true);
      setConnecting(false);
      return;
    }
    
    const currentLog = mockLogs[currentLogIndex];
    let charIndex = 0;
    
    // Typing effect
    const typingInterval = setInterval(() => {
      if (charIndex <= currentLog.text.length) {
        setTypingText(currentLog.text.substring(0, charIndex));
        charIndex++;
      } else {
        clearInterval(typingInterval);
        setLogs(prevLogs => [...prevLogs, currentLog]);
        setTypingText('');
        setCurrentLogIndex(prevIndex => prevIndex + 1);
        
        // Schedule next log
        setTimeout(simulateNextLog, currentLog.delay);
      }
    }, 30); // typing speed
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className='text-2xl font-bold' style={{ color: 'var(--color-white)' }}>Connect to Fi</h2>
        {!connecting && !connected && (
          <button 
            onClick={handleConnect}
            className="px-4 py-2 rounded-md transition-all"
            style={{
              backgroundColor: 'var(--color-accent)',
              color: 'var(--color-white)'
            }}
            onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--color-accent-light)'}
            onMouseLeave={(e) => e.target.style.backgroundColor = 'var(--color-accent)'}
          >
            Connect
          </button>
        )}
        {connected && (
          <div className="flex items-center">
            <div className="h-3 w-3 rounded-full mr-2 animate-pulse" style={{ backgroundColor: 'var(--color-accent)' }}></div>
            <span className="font-medium" style={{ color: 'var(--color-accent)' }}>Connected</span>
          </div>
        )}
      </div>
      
      {(connecting || connected) && (
        <div 
          ref={terminalRef}
          className="rounded-lg p-4 font-mono text-sm h-64 overflow-y-auto backdrop-blur-sm"
          style={{
            backgroundColor: 'var(--color-bg-tertiary)',
            border: '1px solid var(--color-grey-dark)'
          }}
          style={{ 
            boxShadow: 'inset 0 0 10px rgba(0,0,0,0.4)',
            textShadow: '0 0 5px rgba(163, 230, 53, 0.3)'
          }}
        >
          {logs.map((log, index) => (
            <div 
              key={index} 
              className="mb-2"
              style={{
                color: log.success ? 'var(--color-accent)' : log.error ? '#f87171' : 'var(--color-grey-light)'
              }}
            >
              {log.text}
            </div>
          ))}
          {connecting && (
            <div style={{ color: 'var(--color-grey-light)' }}>
              {typingText}
              <span className={`${showCursor ? 'opacity-100' : 'opacity-0'} ml-0.5 font-bold`} style={{ color: 'var(--color-accent)' }}>▋</span>
            </div>
          )}
          {connected && (
            <div className="mt-4">
              <div className="mb-1" style={{ color: 'var(--color-accent)' }}>$ Fi services ready</div>
              <div className="flex items-center">
                <span className="mr-2" style={{ color: 'var(--color-grey-medium)' }}>$</span>
                <div className="h-4 w-2 animate-pulse" style={{ backgroundColor: 'var(--color-accent)' }}></div>
              </div>
            </div>
          )}
        </div>
      )}
      
      {connected && (
        <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg backdrop-blur-sm" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
            <h3 className="text-lg font-medium mb-2" style={{ color: 'var(--color-accent)' }}>Account Summary</h3>
            <div className="text-sm" style={{ color: 'var(--color-grey-light)' }}>
              <div className="flex justify-between mb-1">
                <span>Checking</span>
                <span>$4,285.63</span>
              </div>
              <div className="flex justify-between mb-1">
                <span>Savings</span>
                <span>$12,547.89</span>
              </div>
              <div className="flex justify-between">
                <span>Investment</span>
                <span>$38,652.14</span>
              </div>
            </div>
          </div>
          
          <div className="p-4 rounded-lg backdrop-blur-sm" style={{ backgroundColor: 'var(--color-bg-secondary)', border: '1px solid var(--color-grey-dark)' }}>
            <h3 className="text-lg font-medium mb-2" style={{ color: 'var(--color-accent)' }}>Recent Activity</h3>
            <div className="text-sm space-y-2" style={{ color: 'var(--color-grey-light)' }}>
              <div className="flex justify-between">
                <span>Amazon</span>
                <span style={{ color: '#f87171' }}>-$67.95</span>
              </div>
              <div className="flex justify-between">
                <span>Payroll</span>
                <span style={{ color: '#4ade80' }}>+$2,750.00</span>
              </div>
              <div className="flex justify-between">
                <span>Starbucks</span>
                <span style={{ color: '#f87171' }}>-$5.45</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConnectFiCard;