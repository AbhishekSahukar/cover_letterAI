import { useEffect, useState, useRef } from "react";
import { generateLetter, getHistory } from "./api";
import ChatMessage from "./components/ChatMessage";
import InputBar from "./components/InputBar";
import "./styles.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const endRef = useRef(null);

  useEffect(() => {
    getHistory().then(setMessages);
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text, files = {}) => {
    const formData = new FormData();
    formData.append("message", text);
    if (files.cv) formData.append("cv", files.cv);

    if (text) {
      setMessages((m) => [...m, { role: "user", content: text }]);
    }

    const res = await generateLetter(formData);

    setMessages((m) => [...m, { role: "assistant", content: res.letter }]);
  };

  return (
    <div className="app">
      <h1 className="title">CoverLetter.AI</h1>

      <div className="chat">
        {messages.length === 0 && (
          <ChatMessage
            role="assistant"
            content="👋 Welcome! Upload your CV or paste a Job Description to generate a professional cover letter."
          />
        )}

        {messages.map((m, i) => (
          <ChatMessage key={i} {...m} />
        ))}

        <div ref={endRef} />
      </div>

      <InputBar onSend={sendMessage} />
    </div>
  );
}
