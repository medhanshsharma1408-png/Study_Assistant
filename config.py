import os

API_key=os.getenv("GROQ_API_KEY")
if API_key is None:
    raise ValueError("API_key not found.")
Model="llama-3.1-8b-instant"
Temperature=0 