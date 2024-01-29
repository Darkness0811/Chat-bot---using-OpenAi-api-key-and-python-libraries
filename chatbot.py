from tkinter import *
import requests
from bs4 import BeautifulSoup
import re
import requests
import ssl
import openai
import pandas as pd
from tqdm import tqdm

# GUI
root = Tk()
root.title("GP Bot")

api_key = " " # use your openai api key here
openai.api_key = api_key

# Set the size of the root window to 1080x1920
root.geometry("800x600")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "system", "content": prompt}]

    response = openai.ChatCompletion.create(

    model=model,

    messages=messages,

    temperature=0,

    )

    return response.choices[0].message["content"]



# Send function
def send():
    
    ssl._create_default_https_context = ssl._create_unverified_context

    website_content = {}
    
    input = e.get()
    web_key_ques = input.split(",")

    website_str = ""
    if len(web_key_ques[0]) > 1:
        top_url = web_key_ques[0].split(";")
        for i in top_url:
            website_str += i + "\n"
    else:
        top_url = web_key_ques[0]
        website_str += top_url + "\n"

        
    txt.insert(END, "\nWEBSITES TO BE LOOKED INTO:\n" + website_str)

    txt.insert(END, "\n\nAnalysing Sub URLs.....")
    inside_urls = []

    failed_fetch = 0

    # Send a GET request to the URL
    for url_ in top_url:
        response = requests.get(url_)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all anchor tags (<a>) that contain an 'href' attribute
            all_links = soup.find_all('a', href=True)

            # Regular expression pattern for social media, YouTube, and policy-related domains or patterns to exclude
            excluded_domains = r'(facebook\.com|twitter\.com|instagram\.com|linkedin\.com|youtube\.com|\.gov|\.org|policy|terms)'

            # Extract and print URLs excluding social media, YouTube, and policy-related domains
            for link in all_links:
                href = link['href']
                if re.match(r'https?://', href) and not re.search(excluded_domains, href):
                    inside_urls.append(href)
        else:
            failed_fetch += 0
    txt.insert(END, "\n\n" + f"{failed_fetch} URLS Failed to be fetch the content from the {len(inside_urls)} sub URL")

    # Prints all URLS withing Top URL
    website_sub_str = "\n".join(inside_urls)
    text_file = open("Metadata 1", "w")
    text_file.write(website_sub_str)

    root.after(2000, lambda:txt.insert(END,"\n" + f"{len(inside_urls)} sub URLs has been saved in 'Metadata 1.txt'"))

    root.after(2000, lambda:txt.insert(END,f"\n\nPlease wait as {len(inside_urls)} sub URLs are getting scrapped"))


    for url_index in tqdm(range(len(inside_urls))):
        website  = inside_urls[url_index]

        # Send a GET request to fetch the HTML content of the webpage
        response = requests.get(website)

        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract text content
            text = soup.get_text()

        else:
            # txt.insert(END, "\nFailed to fetch the content from the URL")
            pass

        lines = text.splitlines()
        non_empty_lines = [line for line in lines if line.strip()]

        # Joining the non-empty lines back together
        result = '\n'.join(non_empty_lines)
        website_content[website] = result

    # Takes in keywords
    print("\n\n\n")
    
    keywords = web_key_ques[1].split(";")
    

    keywords_str = "\n".join(keywords)
    txt.insert(END,"\n\n" + f"KEYWORDS:\n{keywords_str}")

    website_content_relevant = {}

    

    for url, text in website_content.items():
        
        paragraphs = text.split('\n')

        # Filtering paragraphs that contain any of the keywords
        keyword_paragraphs = [paragraph for paragraph in paragraphs if any(keyword in paragraph.lower() for keyword in keywords)]

        # Printing paragraphs containing the keywords
        for paragraph in keyword_paragraphs:
            if len(paragraph) >= 60:
                website_content_relevant[url] = paragraph.strip()



    keys_str = "\n".join(website_content_relevant.keys())
    text_file = open("Metadata 2", "w")
    text_file.write(keys_str)
    root.after(2000, lambda:txt.insert(END,"\n\n" + "Relavent URLS has been saved in 'Metadata 2.txt'"))



    ## CHATGPT API promting starts from here
    # Promt to generate only text
    print("\n\n")
    question = web_key_ques[2]
    

    txt.insert(END , f"\n\nQuestion\Topic : {question}\n")

    root.after(2000, lambda:txt.insert(END , "\n\nGenerating Response.......\n"))

# DO NOT TAKE INFORMATION FROM OUTSIDE, IF CANT FIND RELAVENT INFORMATION say "Relavent information not found"\n\n\n
    
    prompt = f""" 
    Data is in the form of dictionary : {website_content_relevant} \n\n\n 
    Question : {question} \n\n\n
    Method of reply : 100 - 200 word sentences, clear reply,

    """

    response = get_completion(prompt)
    root.after(2000, lambda:txt.insert(END,"\n\nRenpose : " + response))

    # Promt to generate only relavent URL links
    prompt = f"""Data : {website_content_relevant} \n\n\n 
    Question : Only mention URLS from data for {question} \n\n\n
    Method of reply : 2-5 URLs, seperate each point with 2 line gap, format it properly
    """
    response1 = get_completion(prompt)
    root.after(2000, lambda:txt.insert(END,"\n\nFor more information : \n\n" + response1))

    text_file = open("Result", "w")
    text_file.write(response + "\n\n\n\n" + response1)



txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=80, height=20)
txt.grid(row=1, column=0, columnspan=2)

scrollbar = Scrollbar(txt)
scrollbar.place(relheight=1, relx=0.974)

e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=70)
e.grid(row=2, column=0)

send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send)
send_button.grid(row=2, column=1)

root.mainloop()
