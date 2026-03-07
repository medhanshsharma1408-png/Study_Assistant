from ui import prompt
from LLM import Wiki,Trivia ,Assistant_response

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
else:
    print("not possible")