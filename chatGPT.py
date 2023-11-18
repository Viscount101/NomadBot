import json
import requests
import math

class chatGPT:
    def generate(self, prompt, size, APIkey):

        tokens = math.floor(1.3333 * size)

        body = {
            "model": "text-babbage-001",
            "prompt": prompt,
            "max_tokens": tokens,
            "temperature": 1,
            "n": 1
            }

        response = requests.post('https://api.openai.com/v1/completions',
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + str(APIkey)
        },
        data = json.dumps(body))
        data = response.json()


        if response.status_code == 401:
            #raise noValidAPI()
            return "ERROR CODE 1"
        elif response.status_code == 429:
            #raise rateLimited()
            return "ERROR CODE 2"
        elif response.status_code == 500:
            #raise siteUnavailable()
            return "ERROR CODE 3"
        elif "error" in data:
            if (data['error']['code'] == None):
                #raise TOSViolation()
                return "ERROR CODE 4"

        return (data['choices'][0]['text'])
