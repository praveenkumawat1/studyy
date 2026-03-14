import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hi! Ask me anything about coding, DSA, or frontend tech.' }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: 'user', text: input }]);
    setLoading(true);
    try {
      const res = await fetch('/api/chatbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      setMessages([...messages, { sender: 'user', text: input }, { sender: 'bot', text: data.reply }]);
    } catch (e) {
      setMessages([...messages, { sender: 'user', text: input }, { sender: 'bot', text: 'Sorry, error occurred.' }]);
    }
    setInput('');
    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.sender === 'bot' ? 'bot-msg' : 'user-msg'}>{msg.text}</div>
        ))}
      </div>
      <div className="chatbot-input">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your question..."
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
