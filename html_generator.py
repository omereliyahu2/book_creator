import re

import requests


class HTMLGenerator:
    @staticmethod
    def generate_html(images_urls: list, story: str):
        pages = re.split(r'Page-\d+', story)
        pages = [page.strip() for page in pages if page.strip()]

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

        return html_content