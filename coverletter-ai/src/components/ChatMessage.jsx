import { downloadPDF } from "../api";

export default function ChatMessage({ role, content }) {
  const isError =
    content.startsWith("⚠") ||
    content.startsWith("Failed to generate");

  const isCoverLetter =
    role === "assistant" && !isError && !content.startsWith("👋");

  return (
    <div className={`msg ${role}`}>
      <div className={`bubble ${isError ? "error" : ""}`}>
        <pre>{content}</pre>

        {isCoverLetter && (
          <button
            className="download-btn"
            onClick={() => downloadPDF(content)}
          >
            ⬇ Download PDF
          </button>
        )}
      </div>
    </div>
  );
}
