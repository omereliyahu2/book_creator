class StoryGenerator:
    def __init__(self, user_input: str, num_pages: int, gpt_client):
        self.story_input = f"I want to write a children's book. The target audience is the reluctant readers genre aged 3-5. it needs to be short, {num_pages} pages with font size of 18. The theme of the book is: {user_input}. Make sure there is only one character and if it is a female character make sure to write it as a strong independent powerful person, not like a gentle princess. And also, and this is very important, in order to separate the pages only use the indicator 'Page-<page number>' and nothing else. I will use this word to parse the text. Here is an example for the Page-<page number>: 'Page-1 page text. Page-2 more page text Page-3 more text' I also don't want any intros or comments from your side, just deliver the story. Intro or comments in the end will mess up my parsing."
        self.gpt_client = gpt_client

    def generate_story(self):
        story = self.gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": "You are a children's book author. You are using humor in your stories. You are sensitive and write stories with moral. You will be given a prompt to write a story for a children's book. You will also be given a prompt to create illustrations for the book."},
                {"role": "user", "content": f"{self.story_input}"}
            ]
        )

        return story.choices[0].message.content