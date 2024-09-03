import re


class ImagePromptsGenerator:
    def __init__(self, story_input: str, gpt_client):
        self.story_input = story_input
        self.gpt_client = gpt_client
        self.image_input_prompt = f"Now I need illustrations for the book. create prompts for each page image. make sure to keep a consistent description to be used in an ai image generator, every prompt should start the same, with the description of the main charachter and then a description of the scene. The prompts should be simillar to eachother regarding the character. If the character is a female, make sure that she is presented as a stron and powerful female and not a princess. And also, and this is very important, in order to separate the pages only use the indicator 'Image-<page number>' and nothing else. I will use this word to parse the text. Here is an example: 'Image-1 prompt. Image-2 prompt Image-3 prompt' I also don't want any intros or comments from your side, just deliver the prompts. Intro or comments in the end will mess up my parsing."

    def generate_image_prompts(self):
        images_prompts = self.gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a children's book illustrator. You are using humor in your illustrations. Your drawings are cute and funny. You will be given a prompt to create illustrations for a book."},
                {"role": "user", "content": f"{self.image_input_prompt}"},
                {"role": "assistant", "content": self.story_input},
            ]
        )

        images = re.split(r'Image-\d+', images_prompts.choices[0].message.content)
        images = [image.strip() for image in images if image.strip()]

        return images

