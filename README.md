# Chat-bot---using-OpenAi-api-key-and-python-libraries

the Python libraries required to create the GP Bot are:
- tkinter
- requests
- BeautifulSoup
- re
- ssl
- openai
- pandas
- tqdm

- the GP Bot analyzes website content by:
1. Extracting all URLs from a given website, excluding social media, YouTube, and policy-related domains.
2. Sending a GET request to fetch the HTML content of each extracted URL.
3. Parsing the HTML content using BeautifulSoup and extracting the text content.
4. Filtering the text content to only include paragraphs that contain relevant keywords.
5. Using OpenAI's GPT-3 model to generate responses to user questions based on the relevant text content.
