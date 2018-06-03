import requests
import json

def get_text_by_image(image_file):
    url = 'http://10.100.1.73:5005/image_to_text'
    response = requests.post(url, data=image_file)
    j = json.loads(response.content.decode('utf8'))
    
    return j['text']
