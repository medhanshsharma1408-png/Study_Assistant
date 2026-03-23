import { useState, useEffect } from "react";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import { fetchSessions } from "./api";

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);

  // Load all sessions on first render
  useEffect(() => {
    loadSessions();
  }, []);

  async function loadSessions() {
    try {
      const data = await fetchSessions();
      setSessions(data);
    } catch (err) {
      console.error("Failed to load sessions:", err);
    }
  }

  function handleSelectSession(sessionId) {
    setActiveSessionId(sessionId);
  }

  function handleNewChat() {
    setActiveSessionId(null); // null = no session yet, backend will create one on first send
  }

  function handleSessionCreated(newSessionId) {
    setActiveSessionId(newSessionId);
    loadSessions(); // refresh the sidebar to show the new session
  }

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">
      <Sidebar
        sessions={sessions}
        activeSessionId={activeSessionId}
        onSelect={handleSelectSession}
        onNewChat={handleNewChat}
      />
      <ChatWindow
        sessionId={activeSessionId}
        onSessionCreated={handleSessionCreated}
      />
    </div>
  );
}