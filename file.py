import os
import requests
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
import ollama


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

HEADERS = {"Content-Type": "application/json"}
MODEL = "llama3.2:latest"

class Website:
    def __init__(self, url, profession):
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.url = url
        try:
            print(f"Fetching URL: {self.url}")
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.title = soup.title.string if soup.title else "No Title Found In Website"
            print(f"Website Title: {self.title}")
            for irrelevantData in soup.body(['script', 'style', 'img', 'input']):
                irrelevantData.decompose()
            self.text = soup.body.get_text(separator='\n', strip=True)
            self.profession = profession
        except requests.RequestException as e:
            print(f"Error fetching the website: {e}")
            self.title = "Error Fetching Website"
            self.text = ""
            self.profession = profession

system_prompt = """You are a Gen Alpha assistant that extracts data from a website and analyzes it \
to determine how it can be useful for my profession. \
Focus on relevant insights and practical applications. Respond in markdown."""

def user_prompt(web):
    user_prompt = f"You are looking at a website with the title {web.title}\n"
    user_prompt += f"Please tell me the ways I can use the information in the website constructively in my profession which is {web.profession}\n"
    user_prompt += web.text
    return user_prompt

def message_(web):
    return [
        {"role": "user", "content": user_prompt(web)},
        {"role": "system", "content": system_prompt}
    ]

profession = input("What is Your Profession: ")
website = input("Enter Website: ")
websiteClass = Website(website, profession)

try:
    print("Sending data to Ollama...")
    response = ollama.chat(model=MODEL, messages=message_(websiteClass))
    print("Received response from Ollama.")
    print(response['message']['content'])
except Exception as e:
    print(f"Error generating response: {e}")