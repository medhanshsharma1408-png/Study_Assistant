from groq import Groq
from config import Model,API_key,Temperature
import json
import requests
import logging

logging.basicConfig(
    filename="assistant.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def Assistant_response(input):
    logging.info(f"User prompt: {input}")
    for attempt in range(3):
        try:
            client = Groq(
                api_key=API_key
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
                model=Model,
                temperature=Temperature,
                max_tokens=500
            )
            response = chat_completion.choices[0].message.content
            tokens = chat_completion.usage.total_tokens
            logging.info(f"Tokens used: {tokens}")
            logging.info(f"LLM response: {response}")
            return response

        except Exception:
            logging.warning("LLM request failed, retrying...")
            logging.error("LLM request failed after 3 attempts")
            return "Sorry, I'm having trouble processing your request right now. Please try again later."

class Wiki:
    def __init__(self,prompt:str):
        self.prom_wiki=prompt

    def Topic_Extraction(self):
        client = Groq(
            api_key=API_key
        )
        extraction="you are an extraction tool that is used to extract key topics from a given prompt. Extact the main topic from the given prompt and display it."\
                     "Respond with only the extracted element, nothing else except the main topic should be displayed in the response."
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":extraction
                },
                {
                    "role":"user",
                    "content":self.prom_wiki
                }
            ],
            model=Model,
            temperature=Temperature
        )
        self.extracted_output=(chat_completion.choices[0].message.content)

    def WIKI_call(self):
        topic = self.extracted_output.strip()
        search_url = f"https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json",
            "srlimit": 1
        }
        headers = {
            "User-Agent": "StudyAssistant/1.0 (test@example.com)"
        }
        logging.info(f"Calling Wikipedia API for topic:{topic}")
        search_resp = requests.get(search_url, params=search_params, headers=headers)
        if search_resp.status_code == 200:
            results = search_resp.json().get("query", {}).get("search", [])
            if results:
                logging.info(f"Wikipedia search successful, found article: {results[0]['title']}")  
                exact_title = results[0]["title"].replace(" ", "_")
            else:
                logging.info("Wikipedia search successful but no articles found")
                self.add_info = "No Wikipedia article found."
                return
        else:
            logging.error("Wikipedia search failed.")
            self.add_info = "Wikipedia search failed."
            return

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{exact_title}"
        response = requests.get(summary_url, headers=headers)
        if response.status_code == 200:
            logging.info("Wikipedia summary fetch successful") 
            data = response.json()
            self.add_info = data.get("extract", "No summary available.")[:500]
        else:
            logging.error("Could not fetch Wikipedia summary.")
            self.add_info = "Could not fetch Wikipedia summary."
        
    def WIKI_Finish(self):
            self.info=self.add_info
            final_prompt=self.prom_wiki + str(self.info)
            return final_prompt
            
class Trivia:
    def __init__(self, prompt: str):
        self.prom_triv = prompt

    def Conditon_Extraction(self):
        triv=self.prom_triv + '''"{id":9,"name":"General Knowledge"},{"id":10,"name":"Entertainment: Books"},{"id":11,"name":"Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"},{"id":27,"name":"Animals"},{"id":28,"name":"Vehicles"},{"id":29,"name":"Entertainment: Comics"},{"id":30,"name":"Science: Gadgets"},{"id":31,"name":"Entertainment: Japanese Anime & Manga"},{"id":32,"name":"Entertainment: Cartoon & Animations"}'''
        client = Groq(
            api_key=API_key
        )
        extraction="you are a tool that is used to enter the number of question, difficulty of the question, and the category those questions belong to for a quiz or test.\n" \
                   "extract the number of questions, their category and their difficulty from the given prompt.\n" \
                   "use the given data to identify the id of the given category and respond using the specific id as answer.\n" \
                   "the difficuly can be easy, medium or hard.\n" \
                   "if no number of questions is provided, chose a random no between 1 and 49 and chose the medium difficulty with general knowledge category id." \
                   "Whatever difficulty the user ask, you have to convert them into one of the three given difficulties,i.e., easy, medium, hard" \
                   "you have to evaluate the given prompt deeply and assess the correct categorey, the catergories in the prompts can even be abbreviations" \
                   "response should be in the form of a python dictionary, where the keys should be number, difficulty, category_id" \
                   "Nothing else should be provided in response" \
                   "the response should strictly restrict to the JSON format" \
                   "Do not show how to do it and just respond with the JSON as response"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":extraction
                },
                {
                    "role":"user",
                    "content":triv
                }
            ],
            model=Model,
            temperature=Temperature
        )
        extracted_output=(chat_completion.choices[0].message.content)
        try:
            data=json.loads(extracted_output)
        except Exception as e:
            logging.error(f"Invalid JSON returned by LLM: {e}")
            return
        self.no=data["number"]
        self.diff=data["difficulty"]
        self.cat_id=data["category_id"]
        
    def Triv_call(self):
        logging.info(f"Calling Trivia API for topic: {self.prom_triv}")
        address=f"https://opentdb.com/api.php?amount={self.no}&category={self.cat_id}&difficulty={self.diff}"
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data["results"]
        else:
            logging.error("Trivia API request failed")
            self.add_info=["No additional information available"]

    def Triv_Finish(self):
        final_prompt=f"User Prompt:{self.prom_triv}\n Additional Information:{str(self.add_info)}"
        return final_prompt
    
class Dict:
    def __init__(self, prompt: str):
        self.prom_def = prompt

    def Def_Extraction(self):
        client = Groq(
            api_key=API_key
        )
        extraction="you are an extraction tool that is used to extract key topics from a given prompt. \
                     Extact the main topic from the given prompt and display it. \
                    Respond with only the extracted element, nothing else except the main topic should be displayed in the response."
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":extraction
                },
                {
                    "role":"user",
                    "content":self.prom_def
                }
            ],
            model=Model,
            temperature=Temperature
        )
        self.extracted_output=(chat_completion.choices[0].message.content)

    def Def(self):
        topic=self.extracted_output.replace(" ","_")
        logging.info(f"Calling Dictionary API for topic: {topic}")
        address=f"https://api.dictionaryapi.dev/api/v2/entries/en/{topic}"
        
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data[0]["meanings"]
        else:
            logging.error("Dictionary API request failed")
            self.add_info=["No additional information available"]

    def Dict_finish(self):
        self.info=self.add_info
        final_prompt=self.prom_def + str(self.info)
        return final_prompt