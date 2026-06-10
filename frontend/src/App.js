import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      const res = await fetch("https://agentdesk-backend-jut7.onrender.com/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
          actions: data.actions,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Error connecting to backend." },
      ]);
    }

    setLoading(false);
  };

  const clearChat = async () => {
    await fetch("https://agentdesk-backend-jut7.onrender.com/clear", { method: "POST" });
    setMessages([]);
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="logo">AgentDesk</div>
        <div className="tagline">AI Agent Workspace</div>
        <div className="tools-list">
          <p>Available Tools</p>
          <span>🔍 Web Search</span>
          <span>📄 Read File</span>
          <span>💾 Write File</span>
          <span>📁 List Files</span>
        </div>
        <button className="clear-btn" onClick={clearChat}>Clear Chat</button>
      </div>

      <div className="main">
        <div className="messages">
          {messages.length === 0 && (
            <div className="empty-state">
              <h2>What can I help you get done?</h2>
              <p>I can search the web, read and write files, and complete multi-step tasks.</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="bubble">{msg.content}</div>
              {msg.actions && msg.actions.length > 0 && (
                <div className="actions">
                  {msg.actions.map((action, j) => (
                    <div key={j} className="action-chip">
                      ⚡ Used {action.tool}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
          {loading && (
            <div className="message assistant">
              <div className="bubble loading">Agent is thinking...</div>
            </div>
          )}
        </div>

        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask me anything or give me a task..."
          />
          <button onClick={sendMessage} disabled={loading}>
            {loading ? "..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;