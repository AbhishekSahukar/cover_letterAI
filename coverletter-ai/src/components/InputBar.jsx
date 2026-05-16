import { useRef, useState } from "react";

export default function InputBar({ onSend }) {
  const [text, setText] = useState("");
  const [cvFile, setCvFile] = useState(null);
  const [jdFile, setJdFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const cvRef = useRef();
  const jdRef = useRef();

  const handleSend = async () => {
    if (!text.trim() && !cvFile && !jdFile) return;
    setLoading(true);
    try {
      await onSend(text, { cv: cvFile, jd: jdFile });
    } finally {
      setText("");
      setCvFile(null);
      setJdFile(null);
      if (cvRef.current) cvRef.current.value = "";
      if (jdRef.current) jdRef.current.value = "";
      setLoading(false);
    }
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="composer-wrapper">
      {(cvFile || jdFile) && (
        <div className="file-previews">
          {cvFile && (
            <div className="file-preview">
              📄 <strong>CV:</strong> {cvFile.name}
              <span
                role="button"
                aria-label="Remove CV"
                onClick={() => {
                  setCvFile(null);
                  if (cvRef.current) cvRef.current.value = "";
                }}
              >
                ✕
              </span>
            </div>
          )}
          {jdFile && (
            <div className="file-preview">
              📋 <strong>JD:</strong> {jdFile.name}
              <span
                role="button"
                aria-label="Remove job description"
                onClick={() => {
                  setJdFile(null);
                  if (jdRef.current) jdRef.current.value = "";
                }}
              >
                ✕
              </span>
            </div>
          )}
        </div>
      )}

      <div className="composer">
        <div className="upload-buttons">
          <label className="composer-icon" title="Upload CV (PDF, DOCX, TXT)">
            CV
            <input
              ref={cvRef}
              type="file"
              hidden
              accept=".pdf,.docx,.txt"
              onChange={(e) => setCvFile(e.target.files[0] || null)}
            />
          </label>

          <label className="composer-icon" title="Upload Job Description">
            JD
            <input
              ref={jdRef}
              type="file"
              hidden
              accept=".pdf,.docx,.txt"
              onChange={(e) => setJdFile(e.target.files[0] || null)}
            />
          </label>
        </div>

        <textarea
          rows="1"
          placeholder="Paste a job description or just ask…"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKey}
          disabled={loading}
        />

        <button className="send-btn" onClick={handleSend} disabled={loading}>
          {loading ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}