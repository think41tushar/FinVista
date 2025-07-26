import { useState } from 'react';
import useTransactionStore from '../../store/transactionStore';

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
  
  const { getSelectedArray, clearSelection } = useTransactionStore();
  const selectedTransactions = getSelectedArray();

  const handleSendMessage = () => {
    if (inputMessage.trim() || selectedTransactions.length > 0) {
      let messageText = inputMessage;
      
      // Add selected transactions context to the message
      if (selectedTransactions.length > 0) {
        const transactionContext = `[Selected transactions: ${selectedTransactions.join(', ')}] `;
        messageText = transactionContext + messageText;
      }
      
      const newMessage = {
        id: messages.length + 1,
        text: messageText,
        sender: 'user'
      };
      setMessages([...messages, newMessage]);
      setInputMessage('');
      clearSelection(); // Clear selection after sending
      
      setTimeout(() => {
        const botResponse = {
          id: messages.length + 2,
          text: selectedTransactions.length > 0 
            ? `I can see you've selected ${selectedTransactions.length} transaction(s). Let me analyze those specific transactions for you.`
            : 'Thanks for your message! I\'m here to help you understand your financial patterns and insights.',
          sender: 'bot'
        };
        setMessages(prev => [...prev, botResponse]);
      }, 1000);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
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
            style={{ background: 'linear-gradient(135deg, var(--color-orange), var(--color-orange-light))' }}
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
      
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div
              className={`pinterest-card max-w-[85%] p-4 rounded-2xl ${
                message.sender === 'user'
                  ? 'chat-message-user ml-4'
                  : 'chat-message-bot mr-4'
              }`}
            >
              <p className="text-sm leading-relaxed">
                {message.text}
              </p>
            </div>
          </div>
        ))}
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
            {selectedTransactions.map((srNo) => (
              <span key={srNo} className="selected-chip">
                #{srNo}
              </span>
            ))}
            <input
              type="text"
              className="flex-1 bg-transparent border-none outline-none min-w-[200px]"
              placeholder={selectedTransactions.length > 0 ? "Continue your message..." : "Ask me about your finances..."}
              style={{ color: 'var(--color-white)' }}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
            />
          </div>
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() && selectedTransactions.length === 0}
            className={`px-4 py-3 rounded-xl transition-all ${
              (inputMessage.trim() || selectedTransactions.length > 0)
                ? 'chat-button'
                : 'chat-button'
            }`}
          >
            <SendIcon />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;