import requests
from groq import Groq
import logging
from ..config import settings

logger = logging.getLogger(__name__)
class Wiki:
    def __init__(self,prompt:str):
        self.prom_wiki=prompt

    def Topic_Extraction(self):
        client = Groq(
            api_key=settings.groq_api_key
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
            model=settings.model,
            temperature=settings.temperature
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
        logger.info(f"Calling Wikipedia API for topic:{topic}")
        search_resp = requests.get(search_url, params=search_params, headers=headers)
        if search_resp.status_code == 200:
            results = search_resp.json().get("query", {}).get("search", [])
            if results:
                logger.info(f"Wikipedia search successful, found article: {results[0]['title']}")  
                exact_title = results[0]["title"].replace(" ", "_")
            else:
                logger.info("Wikipedia search successful but no articles found")
                self.add_info = "No Wikipedia article found."
                return
        else:
            logger.error("Wikipedia search failed.")
            self.add_info = "Wikipedia search failed."
            return

        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{exact_title}"
        response = requests.get(summary_url, headers=headers)
        if response.status_code == 200:
            logger.info("Wikipedia summary fetch successful") 
            data = response.json()
            self.add_info = data.get("extract", "No summary available.")[:500]
        else:
            logger.error("Could not fetch Wikipedia summary.")
            self.add_info = "Could not fetch Wikipedia summary."
        
    def WIKI_Finish(self):
            self.info=self.add_info
            final_prompt=self.prom_wiki + str(self.info)
            return final_prompt