const INTENT_META = {
    wiki:    { label: "Wikipedia", color: "bg-blue-100 text-blue-700" },
    trivia:  { label: "Trivia",    color: "bg-yellow-100 text-yellow-700" },
    dict:    { label: "Dictionary",color: "bg-green-100 text-green-700" },
    general: { label: "General",   color: "bg-gray-100 text-gray-600" },
  };
  
  export default function MessageBubble({ role, content, intent }) {
    const isUser = role === "user";
  
    return (
      <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
        <div className={`max-w-[75%] ${isUser ? "items-end" : "items-start"} flex flex-col gap-1`}>
  
          {!isUser && intent && INTENT_META[intent] && (
            <span className={`text-xs font-semibold px-2 py-0.5 rounded-full w-fit ${INTENT_META[intent].color}`}>
              {INTENT_META[intent].label}
            </span>
          )}

        <div className={`px-4 py-2 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap
          ${isUser
            ? "bg-indigo-600 text-white rounded-br-sm"
            : "bg-white text-gray-800 border border-gray-200 rounded-bl-sm shadow-sm"
          }`}>
          {content}
        </div>

      </div>
    </div>
  );
}