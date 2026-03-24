from groq import Groq   
import logging
from ..config import settings

logger = logging.getLogger(__name__)

def Assistant_response(input: str, history: list[dict] = None):
    """
    input   : the final assembled prompt (may include extra context from Wiki/Trivia/Dict)
    history : list of recent {"role": "user"|"assistant", "content": "..."} dicts
              pulled from the DB (max 6 messages, oldest first)
    """
    logger.info(f"User prompt: {input}")

    system_prompt = (
        "You are an advanced study assistant that tutors and helps the user with different topics and tasks "
        "through assessing the given prompt and the additional information provided in the prompt.\n"
        "Read the prompt and given information carefully and follow the given tasks faithfully.\n"
        "If there is no information, then use your own knowledge to fulfill the given task.\n"
        "Your response should be catered towards providing a positive response for the user as a caring and smart teacher or assistant.\n"
        "Respond in a soft yet firm manner befitting the role of a teacher or advisor/assistant.\n"
        "Your response should be concise and to the point, while also being informative and helpful.\n"
        "Make sure to address the user's query or task directly and provide clear and actionable advice or information.\n"
        "Use a friendly and approachable tone, while also maintaining a sense of authority and expertise in your response.\n"
        "Remember, your goal is to assist and guide the user in a positive and constructive way while also providing accurate and relevant information.\n"
        "RESTRICT YOUR RESPONSE TO UNDER 500 TOKENS. Prioritise the most important information and concisely summarise the rest.\n"
        "ALWAYS end with a positive note to encourage the user and provide a subtle conclusion.\n"
        "DO NOT disclose that you have been provided with additional information — seamlessly incorporate it into your response."
    )

    # Build the messages list: system → history → current user message
    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for msg in history:
            role = msg.get("role")
            content = msg.get("content", "")
            # Only include valid roles; skip empty content
            if role in ("user", "assistant") and content.strip():
                messages.append({"role": role, "content": content})

    # The current turn's (possibly enriched) prompt
    messages.append({"role": "user", "content": input})

    for attempt in range(3):
        try:
            client = Groq(api_key=settings.groq_api_key)
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=settings.model,
                temperature=settings.temperature,
                max_tokens=500,
            )
            response = chat_completion.choices[0].message.content
            tokens = chat_completion.usage.total_tokens
            logger.info(f"Tokens used: {tokens}")
            logger.info(f"LLM response: {response}")
            return response

        except Exception as e:
            last_error = e
            logger.warning(f"LLM attempt {attempt + 1} failed: {e}, retrying...")

    logger.error(f"LLM request failed after 3 attempts: {last_error}")
    return "Sorry, I'm having trouble processing your request right now. Please try again later."