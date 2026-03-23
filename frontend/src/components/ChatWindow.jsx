import { useState, useEffect } from "react";
import MessageList from "./MessageList";
import InputBar from "./InputBar";
import { sendMessage, fetchHistory } from "../api";

export default function ChatWindow({ sessionId, onSessionCreated }) {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  // When sessionId changes (user clicked a past session), load its history
  useEffect(() => {
    if (!sessionId) {
      setMessages([]);
      return;
    }
    fetchHistory(sessionId)
      .then((history) => {
        // Backend returns [{ role, content, intent, created_at }, ...]
        setMessages(history);
      })
      .catch(console.error);
  }, [sessionId]);
 
  async function handleSend(prompt) {
    // Optimistically add the user message immediately
    const userMsg = { role: "user", content: prompt, intent: null };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);
    
    try {
        const data = await sendMessage(prompt, sessionId);
        // data = { response, intent, session_id }
  
        // If this was a new chat, tell App.jsx the new session_id
        if (!sessionId) {
          onSessionCreated(data.session_id);
        }
  
        const assistantMsg = {
          role: "assistant",
          content: data.response,
          intent: data.intent,
        };
        setMessages((prev) => [...prev, assistantMsg]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: "⚠️ Error connecting to backend.", intent: null },
        ]);
      } finally {
        setIsLoading(false);
      }
    }
    
    return (
      <div className="flex flex-col flex-1 h-full bg-gray-50">
        <MessageList messages={messages} />
        <InputBar onSend={handleSend} disabled={isLoading} />
      </div>
    );
  }