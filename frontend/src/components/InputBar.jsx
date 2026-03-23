import { useState } from "react";

export default function InputBar({ onSend, disabled }) {
  const [input, setInput] = useState("");

  function handleSend() {
    const trimmed = input.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);   // lift the value up to the parent
    setInput("");      // clear the box
  }

  function handleKeyDown(e) {
    // Send on Enter, but allow Shift+Enter for newlines (future use)
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }
  return (
    <div className="border-t border-gray-200 bg-white px-4 py-3 flex gap-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask a question..."
        disabled={disabled}
        className="flex-1 rounded-xl border border-gray-300 px-4 py-2 text-sm
                   focus:outline-none focus:ring-2 focus:ring-indigo-400
                   disabled:opacity-50 disabled:cursor-not-allowed"
      />
      <button
      onClick={handleSend}
        disabled={disabled || !input.trim()}
        className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium
                   px-4 py-2 rounded-xl transition-colors
                   disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {disabled ? "..." : "Send"}
      </button>
    </div>
  );
}