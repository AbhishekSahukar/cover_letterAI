import { useEffect, useRef, useState } from "react";
import { generateLetter, getHistory } from "./api";
import ChatMessage from "./components/ChatMessage";
import InputBar from "./components/InputBar";
import "./styles.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const endRef = useRef(null);

  useEffect(() => {
    getHistory().then((history) => {
      if (Array.isArray(history) && history.length > 0) {
        setMessages(history);
      }
    });
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async (text, files = {}) => {
    const formData = new FormData();
    formData.append("message", text);
    if (files.cv) formData.append("cv", files.cv);
    if (files.jd) formData.append("jd", files.jd);

    if (text.trim()) {
      setMessages((prev) => [...prev, { role: "user", content: text }]);
    }

    try {
      const res = await generateLetter(formData);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.letter },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "⚠ Something went wrong. Please try again.",
        },
      ]);
    }
  };

  return (
    <div className="app">
      <h1 className="title">CoverLetter.AI</h1>

      <div className="chat">
        {messages.length === 0 && (
          <ChatMessage
            role="assistant"
            content={
              "👋 Welcome! Upload your CV and a Job Description to generate a tailored cover letter.\n\n" +
              "You can upload PDF, DOCX, or TXT files — or just paste the job description as text."
            }
          />
        )}

        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}

        <div ref={endRef} />
      </div>

      <InputBar onSend={sendMessage} />
    </div>
  );
}