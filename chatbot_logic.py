from ui import get_prompt
from LLM import Wiki, Trivia, Dict, Assistant_response

def run(prompt: str) -> str:
    if any(word in prompt for word in ["explain","describe","elaborate","information","details"]):
        w=Wiki(prompt)
        w.Topic_Extraction()
        w.WIKI_call()
        return Assistant_response(input=w.WIKI_Finish())
    
    elif any(word in prompt for word in ["quiz","mcq","multiple choice questions","test","exam","question"]):
        t=Trivia(prompt)
        t.Conditon_Extraction()
        t.Triv_call()
        return Assistant_response(input=t.Triv_Finish())
    
    elif any(word in prompt for word in ["define","clarify","state","meaning","definition"]):
        d=Dict(prompt)
        d.Def_Extraction()
        d.Def()
        return Assistant_response(input=d.Dict_finish())
    
    else:
        return Assistant_response(input=prompt)
    
if __name__ == "__main__":
    prompt = get_prompt()
    print(run(prompt))