from groq import Groq
from config import Model,API_key,Temperature
from ui import prompt
import json
import requests

def Assistant_response(input):
    print("yes4")
    client = Groq(
        api_key=API_key
    )
    system_prompt="You are an advanced study assistant that tutors and helps the user with different topics and tasks through assessing the given prompt and the additional information provided in the prompt.\n" \
                   "read the prompt and given information carefully and follow the given tasks faithfully according to the given prompts.\n" \
                   "if there is no information, then search the web and fulfill the given task.\n" \
                   "Your response should be catered towards providing a positive response for the user as a caring and smart teacher or assistant.\n" \
                   "respond in a soft yet firm manner befiting the role of a teacher or advisor/assistant."
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
    print(chat_completion.choices[0].message.content)

class Wiki:
    def Topic_Extraction(self):
        self.prom_wiki=prompt
        print("yesW1")
        client = Groq(
            api_key=API_key
        )
        extraction="you are an extraction tool that is used to extract key topics from a given prompt. Extact the main topic from the given prompt and display it."
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content":extraction
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            model=Model,
            temperature=Temperature
        )
        self.extracted_output=(chat_completion.choices[0].message.content)

    def WIKI_call(self):
        print("yesW2")
        topic=self.extracted_output.replace(" ","_")
        address=f"https://en.wikipedia.org/api/rest_v1/page/summary{topic}"
        
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data["extract"][:500]
        else:
            self.add_info=["No additional information available"]
    
    def WIKI_Finish(self):
        print("yesW3")
        self.info=self.add_info[0]
        final_prompt=self.prom_wiki + str(self.info)
        return final_prompt
    
class Trivia:
    def Conditon_Extraction(self):
        self.prom_triv=prompt
        triv=self.prom_triv + '''"{id":9,"name":"General Knowledge"},{"id":10,"name":"Entertainment: Books"},{"id":11,"name":"Entertainment: Film"},{"id":12,"name":"Entertainment: Music"},{"id":13,"name":"Entertainment: Musicals & Theatres"},{"id":14,"name":"Entertainment: Television"},{"id":15,"name":"Entertainment: Video Games"},{"id":16,"name":"Entertainment: Board Games"},{"id":17,"name":"Science & Nature"},{"id":18,"name":"Science: Computers"},{"id":19,"name":"Science: Mathematics"},{"id":20,"name":"Mythology"},{"id":21,"name":"Sports"},{"id":22,"name":"Geography"},{"id":23,"name":"History"},{"id":24,"name":"Politics"},{"id":25,"name":"Art"},{"id":26,"name":"Celebrities"},{"id":27,"name":"Animals"},{"id":28,"name":"Vehicles"},{"id":29,"name":"Entertainment: Comics"},{"id":30,"name":"Science: Gadgets"},{"id":31,"name":"Entertainment: Japanese Anime & Manga"},{"id":32,"name":"Entertainment: Cartoon & Animations"}'''
        print("yesT1")
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
        data=json.loads(extracted_output)
        self.no=data["number"]
        self.diff=data["difficulty"]
        self.cat_id=data["category_id"]
        print(self.no,self.diff,self.cat_id)
        
    def Triv_call(self):
        print("yesT2")
        address=f"https://opentdb.com/api.php?amount={self.no}&category={self.cat_id}&difficulty={self.diff}"
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data["results"]
        else:
            self.add_info=["No additional information available"]

    def Triv_Finish(self):
        print("yesT3")
        final_prompt=self.prom_triv + str(self.add_info)
        return final_prompt