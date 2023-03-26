import openai
import re

openai.api_key = "YOUR API KEY HERE"


def identify_url_types(url_list):
    '''Try and identify pages that are contact, policy, about or other pages related to the policies and standards of
    the site'''
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=f"Extract links from this list that appear to be contact, policy, about or other pages related to the "
               f"policies and standards of the website: {url_list}",
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text



def extract_scores(sentence):
    pattern = r"^(True|False), with a probability score of (\d+(\.\d+)?).*"

    match = re.match(pattern, sentence)
    result = {
    "outcome": match.group(1),
    "probability": float(match.group(2))
    }
    #print(result)
    return result


def quality_contact_page(page_text):
    '''To assess the quality score of a contact page.GPT4 provides better results but the API is limited at time of
    writing and is too expensive but if this changes during development I recommend switching from gpt3-turbo to gpt4
    Similar prompts can be used for other pages such as about, privacy, terms and conditions etc. as well as for detecting
    advertising, sponsored content markers on home pages'''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant assessing the quality of a webpage:"},
            {'role': 'user', 'content': f"Assess the text of this page to see if it is a quality contact page where a "
                                        f"quality contact page contains a physical address, a range of telephone "
                                        f"numbers and a range of email addresses. Provide the result only as True or "
                                        f"False and with a probability score as a float between 0 and 1:{page_text}"},
        ],
        temperature=0.7,
        max_tokens=15,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )
    print (response.choices[0]['message']['content'])
    answer = extract_scores(response.choices[0]['message']['content'])

    return answer


def categorise_page(home_page_text):
    '''To assess the quality score of a contact page.GPT4 provides better results but the API is limited at time of
    writing and is too expensive but if this changes during development I recommend switching from gpt3-turbo to gpt4'''

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant categorising a webpage:"},
            {'role': 'user', 'content': f"Categorise the text of this page. Return the category as a single word:{home_page_text}"},
        ],
        temperature=0.7,
        max_tokens=4,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0

    )
    print (response.choices[0]['message']['content'])
    answer = response.choices[0]['message']['content']

    return answer



if __name__ == '__main__':
    '''Try and identify pages that are contact, policy, about or other pages related to the policies and standards of 
    the site'''
    # Take as input the output of URL extraction function such as extract_links.py
    # The results tend to belong so will have to be chunked to meet the 4000 token input limit

    url_list = ['/login/?action=reset_pass', '/subscribe-to-mg/', 'https://www.facebook.com/MailGuardian/',
                ]

    # print(identify_url_types(url_list[0:int(len(url_list) / 2)]))  # first half of list because of token input limits
    # print(identify_url_types(url_list[int(len(url_list) / 2):int(len(url_list))]))  # second half of list

    '''To assess the quality score of a contact page'''
    """Extract text of a contact page using extract_text_from_page.py"""

    page_text = """blah bah"""
    #assess_page = quality_contact_page(page_text)
    #print(assess_page)

    '''To categorise a URL pass in the extracted text of the home page'''

    home_page_text = """blah blah"""


    categorise_page = categorise_page(home_page_text[0:3000]) # Take first 3000 characters because of token input limits