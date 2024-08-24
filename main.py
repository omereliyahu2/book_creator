import re
from time import sleep

from openai import OpenAI

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.units import inch
import requests

from weasyprint import HTML

leo_url = "https://cloud.leonardo.ai/api/rest/v1/generations"
gpt_client = OpenAI(api_key="testtttttt")
leo_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    'authorization': 'Bearer testtttttttt'
}

leo_payload = {
    "alchemy": True,
    "height": 768,
    "modelId": "d69c8273-6b17-4a30-a13e-d6637ae1c644",
    "num_images": 1,
    "presetStyle": "DYNAMIC",
    "prompt": "",
    "width": 1024
}

user_input = "A story about a girl who is brave that goes on an adventure. Make sure the story is funny and has a moral. Also the girl should be a strong independent character, not a princess."
num_pages = 3

story_input_prompt = f"I want to write a children's book. The target audience is the reluctant readers genre aged 3-5. it needs to be short, {num_pages} pages with font size of 18. The theme of the book is: {user_input}. Make sure there is only one character and if it is a female character make sure to write it as a strong independent powerful person, not like a gentle princess. And also, and this is very important, in order to separate the pages only use the indicator 'Page-<page number>' and nothing else. I will use this word to parse the text. Here is an example for the Page-<page number>: 'Page-1 page text. Page-2 more page text Page-3 more text' I also don't want any intros or comments from your side, just deliver the story. Intro or comments in the end will mess up my parsing."
illus_input_prompt = f"Now I need illustrations for the book. create prompts for each page image. make sure to keep a consistent description to be used in an ai image generator, every prompt should start the same, with the description of the main charachter and then a description of the scene. The prompts should be simillar to eachother regarding the character. If the character is a female, make sure that she is presented as a stron and powerful female and not a princess. And also, and this is very important, in order to separate the pages only use the indicator 'Image-<page number>' and nothing else. I will use this word to parse the text. Here is an example: 'Image-1 prompt. Image-2 prompt Image-3 prompt' I also don't want any intros or comments from your side, just deliver the prompts. Intro or comments in the end will mess up my parsing."

completion_story = gpt_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a children's book author. You are using humor in your stories. You are sensitive and write stories with moral. You will be given a prompt to write a story for a children's book. You will also be given a prompt to create illustrations for the book."},
    {"role": "user", "content": f"{story_input_prompt}"}
  ]
)
print("story completion")
completion_image = gpt_client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a children's book illustrator. You are using humor in your illustrations. Your drawings are cute and funny. You will be given a prompt to create illustrations for a book."},
    {"role": "user", "content": f"{illus_input_prompt}"},
    {"role": "assistant", "content": completion_story.choices[0].message.content},
  ]
)
print("image completion")
pages = re.split(r'Page-\d+', completion_story.choices[0].message.content)
pages = [page.strip() for page in pages if page.strip()]

images = re.split(r'Image-\d+', completion_image.choices[0].message.content)
images = [image.strip() for image in images if image.strip()]


image_responses = []
for image in images:
    leo_payload["prompt"] = image
    response = requests.post(leo_url, json=leo_payload, headers=leo_headers)
    image_responses.append(response.json()['sdGenerationJob']['generationId'])

print("images generated")


images_urls = []
for image_response in image_responses:
    url = f"{leo_url}/{image_response}"
    response = requests.get(url, headers=leo_headers)
    while not response.json()['generations_by_pk']['generated_images']:
        print("waiting for image")
        sleep(3)
        response = requests.get(url, headers=leo_headers)
    images_urls.append(response.json()['generations_by_pk']['generated_images'][0]['url'])
    print("image get")



html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            padding: 2cm;
            background-color: #f5f5f5;
            color: #333;
        }
        h1 {
            text-align: center;
            color: #1e90ff;
            font-size: 2.5em;
        }
        p {
            text-align: justify;
            font-size: 1.2em;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .page {
            page-break-after: always;
        }
        img {
            display: block;
            margin: 20px auto;
            max-width: 80%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    <title>Children's Book</title>
</head>
<body>
"""

for idx, page in enumerate(zip(pages, images_urls)):
    response = requests.get(page[1])
    image_name = page[1].split("/")[-1]
    with open(image_name, "wb") as img_file:
        img_file.write(response.content)


    html_content += f"""
    <div class="page">
        <h1>Page: {idx}</h1>
        <p>{page[0]}</p>
        <img src="{image_name}" alt="Image for page {idx}">
    </div>
    """

html_content += """
</body>
</html>
"""
# Save the test HTML to a file
with open("test.html", "w") as file:
    file.write(html_content)
HTML("test.html").write_pdf("children_book.pdf")