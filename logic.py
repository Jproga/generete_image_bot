import json
import time
import requests
from PIL import Image
from io import BytesIO
import base64  # Добавлен импорт

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images'][0]

            attempts -= 1
            time.sleep(delay)

    def text_to_image(self, prompt, model, filename, width=1024, height=1024):
        uuid = self.generate(prompt, model, width=width, height=height)
        image_data = self.check_generation(uuid)

        # Декодирование изображения
        image = Image.open(BytesIO(base64.b64decode(image_data)))
        image.save(filename)

if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'Api_token', 'secret_token')
    model_id = api.get_model()

    # Преобразование текста в изображение
    api.text_to_image("солнце в малиновом закате", model_id, "landscape.png")
