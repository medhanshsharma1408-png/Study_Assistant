from .services.LLM import Assistant_response
from .services.Wiki import Wiki
from .services.Trivia import Trivia
from .services.Dict import Dict

def run(prompt: str) -> tuple[str, str]:
    if any(word in prompt for word in ["explain","describe","elaborate","information","details"]):
        w=Wiki(prompt)
        w.Topic_Extraction()
        w.WIKI_call()
        return Assistant_response(input=w.WIKI_Finish()), "wiki"
    
    elif any(word in prompt for word in ["quiz","mcq","multiple choice questions","test","exam","question"]):
        t=Trivia(prompt)
        t.Conditon_Extraction()
        t.Triv_call()
        return Assistant_response(input=t.Triv_Finish()), "trivia"
    
    elif any(word in prompt for word in ["define","clarify","state","meaning","definition"]):
        d=Dict(prompt)
        d.Def_Extraction()
        d.Def()
        return Assistant_response(input=d.Dict_finish()), "dict"
    
    else:
        return Assistant_response(input=prompt),"general"
    