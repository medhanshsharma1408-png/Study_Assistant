from .services.LLM import Assistant_response
from .services.Wiki import Wiki
from .services.Trivia import Trivia
from .services.Dict import Dict


def run(prompt: str, history: list[dict] = None) -> tuple[str, str]:
    """
    prompt  : the raw user message (lowercased by the validator in chat.py)
    history : up to 6 recent {"role", "content"} dicts from the DB, oldest first
    """
    if any(word in prompt for word in ["explain", "describe", "elaborate", "information", "details"]):
        w = Wiki(prompt)
        w.Topic_Extraction()
        w.WIKI_call()
        return Assistant_response(input=w.WIKI_Finish(), history=history), "wiki"

    elif any(word in prompt for word in ["quiz", "mcq", "multiple choice questions", "test", "exam", "question"]):
        t = Trivia(prompt)
        t.Condition_Extraction()
        t.Triv_call()
        return Assistant_response(input=t.Triv_Finish(), history=history), "trivia"

    elif any(word in prompt for word in ["define", "clarify", "state", "meaning", "definition"]):
        d = Dict(prompt)
        d.Def_Extraction()
        d.Def()
        return Assistant_response(input=d.Dict_finish(), history=history), "dict"

    else:
        return Assistant_response(input=prompt, history=history), "general"