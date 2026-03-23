export default function Sidebar({ sessions, activeSessionId, onSelect, onNewChat }) {

    function formatDate(isoString) {
      const d = new Date(isoString);
      return d.toLocaleDateString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
    }
  
    return (
      <div className="w-64 shrink-0 bg-gray-900 text-white flex flex-col h-full">
  
        {/* Header */}
        <div className="px-4 py-4 border-b border-gray-700">
          <h1 className="text-lg font-bold tracking-tight">📚 Study Assistant</h1>
        </div>
  
        {/* New Chat button */}
        <div className="px-3 py-3">
          <button
            onClick={onNewChat}
            className="w-full text-sm bg-indigo-600 hover:bg-indigo-700 text-white
                       rounded-lg px-3 py-2 transition-colors font-medium"
          >
          + New Chat
        </button>
      </div>

      {/* Session list */}
      <div className="flex-1 overflow-y-auto px-2 pb-4">
        {sessions.length === 0 && (
          <p className="text-gray-500 text-xs text-center mt-4">No sessions yet</p>
        )}
        {sessions.map((s) => (
          <button
            key={s.session_id}
            onClick={() => onSelect(s.session_id)}
            className={`w-full text-left px-3 py-2 rounded-lg mb-1 text-sm transition-colors
              ${s.session_id === activeSessionId
                ? "bg-indigo-700 text-white"
                : "text-gray-300 hover:bg-gray-800"
              }`}
          > 
          <div className="font-medium truncate">Session</div>
          <div className="text-xs text-gray-400 mt-0.5">{formatDate(s.created_at)}</div>
        </button>
      ))}
    </div>

  </div>
);
}