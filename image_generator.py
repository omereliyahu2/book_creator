from time import sleep
import requests

class ImageGenerator:
    def __init__(self, generator_url, generator_payload, generator_headers, gpt_client):
        self.generator_url = generator_url
        self.generator_payload = generator_payload
        self.generator_headers = generator_headers
        self.gpt_client = gpt_client

    def generate_image(self, prompts: list) -> list:
        image_responses = []
        for prompt in prompts:
            self.generator_payload["prompt"] = prompt
            response = requests.post(self.generator_url, json=self.generator_payload, headers=self.generator_headers)
            image_responses.append(response.json()['sdGenerationJob']['generationId'])

        print("images generated")

        images_urls = []
        for image_response in image_responses:
            url = f"{self.generator_url}/{image_response}"
            response = requests.get(url, headers=self.generator_headers)
            while not response.json()['generations_by_pk']['generated_images']:
                print("waiting for image")
                sleep(3)
                response = requests.get(url, headers=self.generator_headers)
            images_urls.append(response.json()['generations_by_pk']['generated_images'][0]['url'])
            print("image get")

        return images_urls