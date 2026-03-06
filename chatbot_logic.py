from ui import prompt
from LLM import Wiki,Trivia ,Assistant_response

if any(word in prompt for word in ["explain","describe","elaborate"]):
    w=Wiki()
    w.Topic_Extraction()
    w.Summary()
    p=w.finishing_touches()
    Assistant_response(input=p)
elif any(word in prompt for word in ["quiz","mcq","multiple choice questions","test","exam"]):
    t=Trivia()
    t.Conditon_Extraction()
else:
    print("not possible")