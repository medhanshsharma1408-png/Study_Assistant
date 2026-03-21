import requests
import json 
from groq import Groq
import logging
from ..config import settings

logger = logging.getLogger(__name__)
class Trivia:
    def __init__(self, prompt: str):
        self.prom_triv = prompt

    def Conditon_Extraction(self):
        triv=self.prom_triv + '''"{id":9,"name":"General Knowledge"},{"id":10,"name":"Entertainment: Books"},{"id":11,"name":"Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"},{"id":27,"name":"Animals"},{"id":28,"name":"Vehicles"},{"id":29,"name":"Entertainment: Comics"},{"id":30,"name":"Science: Gadgets"},{"id":31,"name":"Entertainment: Japanese Anime & Manga"},{"id":32,"name":"Entertainment: Cartoon & Animations"}'''
        client = Groq(
            api_key=settings.groq_api_key
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
            model=settings.model,
            temperature=settings.temperature
        )
        extracted_output=(chat_completion.choices[0].message.content)
        try:
            data=json.loads(extracted_output)
        except Exception as e:
            logger.error(f"Invalid JSON returned by LLM: {e}")
            return
        self.no=data["number"]
        self.diff=data["difficulty"]
        self.cat_id=data["category_id"]
        
    def Triv_call(self):
        logger.info(f"Calling Trivia API for topic: {self.prom_triv}")
        address=f"https://opentdb.com/api.php?amount={self.no}&category={self.cat_id}&difficulty={self.diff}"
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data["results"]
        else:
            logger.error("Trivia API request failed")
            self.add_info=["No additional information available"]

    def Triv_Finish(self):
        final_prompt=f"User Prompt:{self.prom_triv}\n Additional Information:{str(self.add_info)}"
        return final_prompt