# Standard Library Imports
import os
import io
import re
import html
import requests
from io import BytesIO

# Third-Party Imports
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from google.cloud import vision_v1
from google.cloud import vision
from flask_cors import cross_origin
from pdf2image import convert_from_path


# Initialize Flask app
app = Flask(__name__)

# Constants
SERVICE_ACCOUNT_PATH = 'ServiceAccountToken.json'

# Helper Functions
def get_vision_client():
    return vision_v1.ImageAnnotatorClient.from_service_account_file(SERVICE_ACCOUNT_PATH)

def fetch_image_data(url):
    response = requests.get(url)
    return response.content

# Core Functions
# Converts the given image URL to text
def image_url_to_text(image_urls):
    """Converts the given image URLs to text."""
    texts = []
    client = get_vision_client()
    
    for url in image_urls:
        image_data = fetch_image_data(url)
        image = vision_v1.Image(content=image_data)
        response = client.text_detection(image=image)
        texts.append(response.text_annotations[0].description)
    
    return texts


#Sort and parse for image links
def image_parser(main_content):
    background_images = main_content.find_all(style=re.compile(r'background-image:\s*url\([^)]+\)'))
    image_pattern = r'https://[^"]+'
    result_images = []
    #Parse images
    for image in background_images:
        url = re.findall(image_pattern, image['style'])
        url = [html.unescape(u) for u in url]
        result_images.extend(url)
    return result_images


# Function to parse problem numbers
def problem_number_parser(soup, max_problem_length=6):
    result_problems = []
    problem_outline = soup.find_all('div', class_='selectPagesQuestionOutline--title')
    problem_pattern = r'</strong>(.*?)</div>'
    for problem in problem_outline:
        num = re.search(problem_pattern, str(problem))
        num_parsed = num.group(1).strip()
        if len(num_parsed) <= max_problem_length:
            result_problems.append(num_parsed)
    return result_problems


'''
Takes in a list of strings (image texts) and another list of strings (problem numbers) and returns a hashmap with the key being a problem number and the value being an array of integers corresponding to the problem number's associated pages
IN ORDER FOR BEST RESULTS, PROBLEM NUMBER WILL ALWAYS FOLLOW THE FOLLOWING FORMAT:
- BEGINNING OF LINE + NUMBER + PART OF PROBLEM + '.'
- example: '1a.' or '2c.' or '42e.' or '1)' or '5)'
- Since we are getting the problem numbers from the website, please follow the exact format used in gradescope.
- It is assumed that each problem number will always be on the left-most side of the line, to allow for easy parsing of textual information
- All numbering should be in the same vertical column across all pages of the assignment 
'''
def page_assigner(list_of_strings, problem_queue):
    page_num = 0
    curr_problem = problem_queue.pop(0)
    next_problem = problem_queue.pop(0)
    problem_pages_map = {}
    # iterate through each page
    for i in range(len(list_of_strings)):
        text_on_page = list_of_strings[i].splitlines()
    
        # iterate through each line in the page
        for line in text_on_page:
            # if line starts with next problem, set curr_problem to be next_problem, and set next_problem to be the next problem in the queue
            if line.startswith(next_problem):
                curr_problem = next_problem
                if problem_queue:
                    next_problem = problem_queue.pop(0)
                else: 
                    next_problem = None

            # add each new problem to the hashmap. Store the current page numbr as the first page associated with the problem
            if curr_problem not in problem_pages_map:
                    problem_pages_map[curr_problem] = []
                    problem_pages_map[curr_problem].append(page_num)

            # if answer to a question is continued on the next page, add the next page to the list that contains the number of pages for the current problem
            if curr_problem in problem_pages_map and page_num not in problem_pages_map[curr_problem]:                
                problem_pages_map[curr_problem].append(page_num)
                        
            # if there are no more problems in the queue, then just process the last question, then we're done
            if not next_problem:
                return problem_pages_map
        
        page_num += 1
    return problem_pages_map


# Function to select the question and pages
# Interacts with the DOM elements using Selenium
def question_selector(driver, question, page_nums):
    question_list = driver.find_elements("class name", "selectPagesQuestionOutline--item")
    images_list = driver.find_elements("class name", "pageThumbnail--selector")
    for index, question_element in enumerate(question_list):
        index -= 1
        # Selecting the right div element
        if question in question_element.text:
            # Selecting the question. Performs Click Action
            driver.execute_script("arguments[0].click();", question_element)
            # Select the pages. Performs Click Action
            # The website's JS should detect the click and perform the tagging process to save the selection
            for page_num in page_nums[index]:
                driver.execute_script("arguments[0].click();", images_list[page_num])


# Main route to get data
@app.route('/get-data', methods=['POST'])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_data():
    # Get the email and password from the request
    received_data = request.json
    email = received_data.get('email')
    password = received_data.get('password')

    # Setup selenium driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    # Automate sign-in process
    driver.get("https://www.gradescope.com/login")
    driver.find_element_by_id("session_email").send_keys(email)
    driver.find_element_by_id("session_password").send_keys(password)
    driver.find_element_by_name("commit").click()

    # Wait until the page loads
    WebDriverWait(driver, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))

    # Access and parse content
    driver.get("https://www.gradescope.com/courses/567436/assignments/3290069/submissions/193818048/select_pages")
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    main_content = soup.find("main")

    # Use the parsing functions
    image_links = image_parser(main_content)
    problem_numbers = problem_number_parser(soup)
    question_to_page_map = page_assigner(image_url_to_text(image_links), problem_numbers)
    page_num = list(question_to_page_map.values())

    # Performs the changes on the website
    for question in problem_numbers:
        question_selector(driver, question, page_num)


# Entry point
if __name__ == '__main__':
    app.run(port=5000)
