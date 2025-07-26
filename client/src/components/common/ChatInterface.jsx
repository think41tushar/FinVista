import { useState, useEffect, useRef } from 'react';
import useTransactionStore from '../../store/transactionStore';
import useAuthStore from '../../store/authStore';

const SendIcon = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
  </svg>
);

const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! How can I help you analyze your financial data today?', sender: 'bot' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef(null);
  
  const { user } = useAuthStore();
  const { 
    getSelectedArray, 
    getSelectedTransactions,
    clearSelection, 
    deselectTransaction,
    queryAI, 
    fetchUserData,
    loading 
  } = useTransactionStore();
  
  const selectedTransactionIds = getSelectedArray();
  const selectedTransactions = getSelectedTransactions();

  // Auto scroll to bottom when messages change
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isProcessing]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() && selectedTransactions.length === 0) return;
    
    setIsProcessing(true);
    
    // Prepare user message text
    let displayMessageText = inputMessage;
    if (selectedTransactions.length > 0) {
      const transactionSummary = selectedTransactions.map(t => 
        `#${t.id.slice(-8)} - ${t.narration.slice(0, 50)}...`
      ).join(', ');
      displayMessageText = `[${selectedTransactions.length} selected: ${transactionSummary}] ${inputMessage}`;
    }
    
    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: displayMessageText,
      sender: 'user'
    };
    setMessages(prev => [...prev, userMessage]);
    
    // Store the current selected transaction IDs for API call
    const currentSelectedIds = [...selectedTransactionIds];
    const currentInputMessage = inputMessage;
    
    // Clear input and selection
    setInputMessage('');
    clearSelection();
    
    try {
      // Call AI API with context
      const result = await queryAI(currentInputMessage, currentSelectedIds, user?.id);
      
      if (result.success) {
        // Ensure response is a string
        let responseText = result.response;
        if (typeof responseText !== 'string') {
          responseText = JSON.stringify(responseText, null, 2);
        }
        
        // Add AI response to chat
        const botMessage = {
          id: Date.now() + 1,
          text: responseText,
          sender: 'bot'
        };
        setMessages(prev => [...prev, botMessage]);
        
        // Always refresh data after successful AI query to ensure UI is up-to-date
        try {
          if (user?.id) {
            await fetchUserData(user.id);
          }
        } catch (refreshError) {
          console.error('Error refreshing data after AI response:', refreshError);
          // Don't show error to user, just log it
        }
      } else {
        // Handle error
        console.error('AI query failed:', result.error);
        const errorMessage = {
          id: Date.now() + 1,
          text: `Sorry, I encountered an error: ${result.error}`,
          sender: 'bot'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Unexpected error in chat interface:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an unexpected error. Please try again.',
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="h-full flex flex-col chat-container rounded-2xl">
      <div 
        className="p-4 border-b"
        style={{ 
          borderColor: 'var(--color-grey-dark)',
          backgroundColor: 'var(--color-bg-tertiary)'
        }}
      >
        <div className="flex items-center space-x-3">
          <div 
            className="w-10 h-10 rounded-full flex items-center justify-center"
            style={{ background: 'linear-gradient(135deg, var(--color-accent), var(--color-accent-light))' }}
          >
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-white">AI Assistant</h3>
            <p className="text-sm" style={{ color: 'var(--color-cream)' }}>Financial Advisor</p>
          </div>
        </div>
      </div>
      
      <div className="flex-1 overflow-auto p-4 space-y-4 min-h-0">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`pinterest-card max-w-[85%] p-4 rounded-2xl ${
                message.sender === 'user'
                  ? 'chat-message-user ml-4'
                  : 'chat-message-bot mr-4'
              }`}
            >
              <p className="text-sm leading-relaxed whitespace-pre-wrap">
                {message.text}
              </p>
            </div>
          </div>
        ))}
        
        {/* Loading indicator when processing */}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="pinterest-card max-w-[85%] p-4 rounded-2xl chat-message-bot mr-4">
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2" style={{ borderColor: 'var(--color-accent)' }}></div>
                <p className="text-sm">AI is thinking...</p>
              </div>
            </div>
          </div>
        )}
        
        {/* Auto scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
      
      <div 
        className="p-4 border-t"
        style={{ 
          borderColor: 'var(--color-grey-dark)',
          backgroundColor: 'var(--color-bg-tertiary)'
        }}
      >
        
        <div className="flex space-x-3">
          <div className="chat-input flex-1 rounded-xl px-4 py-3 transition-all min-h-[48px] flex items-center flex-wrap gap-2">
            {/* Selected transaction chips */}
            {selectedTransactions.map((transaction) => (
              <span key={transaction.id} className="selected-chip" style={{ paddingRight: '28px' }}>
                #{transaction.id.slice(-8)}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    deselectTransaction(transaction.id);
                  }}
                  className="absolute right-1 top-1/2 transform -translate-y-1/2 text-xs hover:text-red-400 transition-colors"
                  style={{ color: 'var(--color-grey-light)' }}
                >
                  ×
                </button>
              </span>
            ))}
            <input
              type="text"
              className="flex-1 bg-transparent border-none outline-none min-w-[200px]"
              placeholder={selectedTransactions.length > 0 ? "Ask about selected transactions..." : "Ask me about your finances..."}
              style={{ color: 'var(--color-white)' }}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyDown={handleKeyPress}
              disabled={isProcessing}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={(!inputMessage.trim() && selectedTransactions.length === 0) || isProcessing}
            className={`px-4 py-3 rounded-xl transition-all ${
              (inputMessage.trim() || selectedTransactions.length > 0) && !isProcessing
                ? 'chat-button opacity-100'
                : 'chat-button opacity-50 cursor-not-allowed'
            }`}
          >
            {isProcessing ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            ) : (
              <SendIcon />
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;