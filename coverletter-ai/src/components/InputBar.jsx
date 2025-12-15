import { useState } from "react";

export default function InputBar({ onSend }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const handleSend = () => {
    if (!text.trim() && !file) return;
    onSend(text, file ? { cv: file } : {});
    setText("");
  };

  return (
    <div className="composer-wrapper">
      <div className="composer">
        <label className="composer-icon" title="Upload CV or Job Description">
          +
          <input
            type="file"
            hidden
            onChange={(e) => setFile(e.target.files[0])}
          />
        </label>

        <textarea
          rows="1"
          placeholder="Ask anything"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        <button className="send-btn" onClick={handleSend}>
          Send
        </button>
      </div>

      {file && (
        <div className="file-preview">
          📎 {file.name}
          <span onClick={() => setFile(null)}>✕</span>
        </div>
      )}
    </div>
  );
}
