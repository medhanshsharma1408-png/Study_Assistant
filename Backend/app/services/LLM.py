from groq import Groq   
import logging
from ..config import settings

logger = logging.getLogger(__name__)
def Assistant_response(input):
    logger.info(f"User prompt: {input}")
    for attempt in range(3):
        try:
            client = Groq(
                api_key=settings.groq_api_key
            )
            system_prompt="You are an advanced study assistant that tutors and helps the user with different topics and tasks through assessing the given prompt and the additional information provided in the prompt.\n" \
                        "read the prompt and given information carefully and follow the given tasks faithfully according to the given prompts.\n" \
                        "if there is no information, then search the web and fulfill the given task.\n" \
                        "Your response should be catered towards providing a positive response for the user as a caring and smart teacher or assistant.\n" \
                        "respond in a soft yet firm manner befiting the role of a teacher or advisor/assistant."\
                        "Your response should be concise and to the point, while also being informative and helpful.\n" \
                        "Make sure to address the user's query or task directly and provide clear and actionable advice or information.\n" \
                        "Use a friendly and approachable tone, while also maintaining a sense of authority and expertise in your response.\n" \
                        "Remember, your goal is to assist and guide the user in a positive and constructive way while also providing accurate and relevant information based on the given prompt and any additional information provided."\
                        "MAKE SURE TO RESTRICT YOUR RESPONSE UNDER 500 WORDS OR 500 TOKENS, IF THE RESPONSE EXCEEDS THIS LIMIT, THEN PRIORITIZE THE MOST IMPORTANT INFORMATION AND CONCISELY SUMMARIZE THE REST TO FIT WITHIN THE LIMIT."\
                        "ALWAYS MAKE SURE TO ADHERE TO THE TOKEN LIMIT AND PROVIDE A RESPONSE THAT IS BOTH HELPFUL AND CONCISE, WHILE ALSO MAINTAINING A FRIENDLY AND APPROACHABLE TONE IN YOUR RESPONSE WHILE ENDING WITH A POSITIVE NOTE TO ENCOURAGE THE USER AND PROVINING A SUBTLE CONLUSION TO YOUR RESPONSE TO MAKE IT MORE ENGAGING AND THOUGHT PROVOKING FOR THE USER."\
                        "YOU DONT HAVE TO INFORM THE USER THAT YOU HAVE BEEN PROVIDED WITH ADDITIONAL INFORMATION, JUST USE THE INFORMATION TO PROVIDE A BETTER RESPONSE TO THE USER WITHOUT DISCLOSING THAT YOU HAVE BEEN PROVIDED WITH ADDITIONAL INFORMATION, JUST SEAMLESSLY INCORPORATE THE INFORMATION INTO YOUR RESPONSE TO PROVIDE A MORE INFORMATIVE AND HELPFUL ANSWER TO THE USER'S QUERY OR TASK."
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content":system_prompt
                    },
                    {
                        "role":"user",
                        "content":input
                    }
                ],
                model=settings.model,
                temperature=settings.temperature,
                max_tokens=500
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