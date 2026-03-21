import requests
from groq import Groq   
import logging
from ..config import settings

logger = logging.getLogger(__name__)
class Dict:
    def __init__(self, prompt: str):
        self.prom_def = prompt

    def Def_Extraction(self):
        client = Groq(
            api_key=settings.groq_api_key
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
            model=settings.model,
            temperature=settings.temperature
        )
        self.extracted_output=(chat_completion.choices[0].message.content)

    def Def(self):
        topic=self.extracted_output.replace(" ","_")
        logger.info(f"Calling Dictionary API for topic: {topic}")
        address=f"https://api.dictionaryapi.dev/api/v2/entries/en/{topic}"
        
        response=requests.get(url=address)
        if response.status_code == 200:
            data=response.json()
            self.add_info=data[0]["meanings"]
        else:
            logger.error("Dictionary API request failed")
            self.add_info=["No additional information available"]

    def Dict_finish(self):
        self.info=self.add_info
        final_prompt=self.prom_def + str(self.info)
        return final_prompt