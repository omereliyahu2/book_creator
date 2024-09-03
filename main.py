import argparse
import os

from openai import OpenAI

from weasyprint import HTML

from html_generator import HTMLGenerator
from image_generator import ImageGenerator
from image_prompts_generator import ImagePromptsGenerator
from story_generator import StoryGenerator

parser = argparse.ArgumentParser(description="Get the user's input")
parser.add_argument('story_input', type=str, help='The input parameter for the script')
parser.add_argument('num_pages', type=int, help='The number of pages for the story')
args = parser.parse_args()
story_input = args.story_input
num_pages = args.num_pages

gpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

story_generator = StoryGenerator(user_input=story_input, num_pages=num_pages, gpt_client=gpt_client)
story = story_generator.generate_story()

images_prompts_generator = ImagePromptsGenerator(story_input=story, gpt_client=gpt_client)
images_prompts = images_prompts_generator.generate_image_prompts()

image_generator = ImageGenerator(generator_url=os.getenv("GENERATOR_URL"), generator_payload=os.getenv("GENERATOR_PAYLOAD"), generator_headers=os.getenv("GENERATOR_HEADERS"), gpt_client=gpt_client)
images_urls = image_generator.generate_image(prompts=images_prompts)

html_content = HTMLGenerator.generate_html(story=story, images_urls=images_urls)

# Save the test HTML to a file
with open("your_book.html", "w") as file:
    file.write(html_content)
HTML("your_book.html").write_pdf("your_book.pdf")
print("PDF generated")
