import json
import requests

class Dalle:
    def generate(self, prompt, APIkey):
        body = {
            "prompt": prompt,
            "n": 1,
            "size": "512x512"
        }
        response = requests.post('https://api.openai.com/v1/images/generations',
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + str(APIkey)
            },
            data=json.dumps(body))
        data = response.json()

        if response.status_code == 401:
            print("Server has no API Key")
            return "ERROR CODE 1"
        elif response.status_code == 429:
            print("Too many requests at a time or hard limit reached")
            return "ERROR CODE 2"
        elif response.status_code == 500:
            print("Dalle API is unavailable")
            return "ERROR CODE 3"
        elif "error" in data:
            if (data['error']['code'] == None):
                print("Violation of TOS for openAI")
                return "ERROR CODE 4"

        url = data['data'][0]['url']
        response = requests.get(url)
        with open("temp/dalle.png", 'wb+') as f:
            f.write(response.content)
        return url
