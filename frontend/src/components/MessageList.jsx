import { useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";

export default function MessageList({ messages }) {
  // A ref is like a pointer to a real DOM node — doesn't cause re-renders
  const bottomRef = useRef(null);

  // Every time messages changes, scroll the bottom sentinel into view
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto px-4 py-4">

      {messages.length === 0 && (
        <div className="flex items-center justify-center h-full text-gray-400 text-sm">
          Ask anything to start studying...
        </div>
      )}

      {messages.map((msg, idx) => (
        <MessageBubble
          key={idx}
          role={msg.role}
          content={msg.content}
          intent={msg.intent}
        />
      ))}

      {/* Invisible element at the bottom — we scroll here on new messages */}
      <div ref={bottomRef} />
    </div>
  );
}