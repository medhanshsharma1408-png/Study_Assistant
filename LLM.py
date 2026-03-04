from groq import Groq
from config import Model,API_key,Temperature
from ui import prompt
import requests

def Assistant_response():
    client = Groq(
        api_key=API_key
    )
    system_prompt=("You are an advanced study assistant that tutors and helps the user with different topics and tasks through assessing the given prompt and the additional information provided in the prompt.\n"
                   "read the prompt and given information carefully and follow the given tasks faithfully according to the given prompts.\n"
                   " if there is no information, then search the web and fulfill the given task.")

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":system_prompt
            },
            {
                "role":"user",
                "content":prompt
            }
        ],
        model=Model,
        temperature=Temperature
    )
    print(chat_completion.choices[0].message.content)

class Wiki:
    def Topic_Extraction(self):
        self.prom=prompt
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

    def Summary(self):
        topic=self.extracted_output.replace(" ","_")
        address=f"https://en.wikipedia.org/api/rest_v1/page/summary{topic}"
        
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data["extract"][:500]
        else:
            self.add_info=["No additional information available"]
    
    def finishing_touches(self):
        final_prompt=self.prom + self.add_info

class Trivia:
    def



