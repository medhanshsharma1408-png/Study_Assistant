from ui import prompt
from LLM import Wiki, Trivia, Dict, Assistant_response

if any(word in prompt for word in ["explain","describe","elaborate"]):
    w=Wiki()
    w.Topic_Extraction()
    w.WIKI_call()
    p=w.WIKI_Finish()
    Assistant_response(input=p)
elif any(word in prompt for word in ["quiz","mcq","multiple choice questions","test","exam"]):
    t=Trivia()
    t.Conditon_Extraction()
    t.Triv_call()
    p=t.Triv_Finish()
    Assistant_response(input=p)
elif any(word in prompt for word in ["define","clarify","state"]):
    d=Dict()
    d.Def_Extraction()
    d.Def()
    p=d.Dict_finish()
    Assistant_response(input=p)
else:
    Assistant_response(input=prompt)