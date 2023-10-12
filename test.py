# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup

# # Token
# signed_token = "RVgyZmVUTmFhenNtTlBkUkNjY3ZkUDU1WjVaQ0c2YVI4M1ZrUTR6clhQST0tLUVwdjJ3YnJwKzdUdkoza0pSZ3VCU3c9PQ%3D%3D--780e3a109530a6cdbca2dd59844690aa96e732c1" 

# # Set up Chrome options for headless browsing
# chrome_options = Options()
# chrome_options.add_argument("--headless") # Run Chrome in headless mode (no GUI)

# # Create a WebDriver instance for Chrome
# driver = webdriver.Chrome(options=chrome_options)

# # Update Cookie
# driver.get('https://www.gradescope.com') # Visit the website to set cookies
# driver.add_cookie({'name': 'signed_token', 'value': signed_token})

# # Navigate to the desired URL
# url = 'https://www.gradescope.com/courses/567436/assignments/3290069/submissions/193710547/select_pages'
# driver.get(url)

# # Wait for the content to load (you may need to adjust the sleep duration)
# time.sleep(0.5) # Wait for 5 seconds (adjust as needed)

# # Get the fully loaded HTML content
# html_content = driver.page_source

# # Close the WebDriver when done
# driver.quit()

# # Parse the HTML with BeautifulSoup
# soup = BeautifulSoup(html_content, 'html.parser')

# main_content = soup.find('main')

# # Since the click event is on the <li> elements, we need to find them first
# ol_items = soup.find('ol').find_all('ol', class_='selectPagesQuestionOutline--list')
# # print(len(list_items)) = 3

# question_div_dict = {}
# questions_list = []
# for ol in ol_items:
#     questions = ol.find_all('div', class_='selectPagesQuestionOutline--title')
#     target_div = ol.find_all('div', class_='selectPagesQuestionOutline--item')
#     for question in range(len(questions)):
#         questions_list.append(questions[question].text) 
#         # question_div_dict[questions[question].text] = target_div[question]

# print(questions_list)




# Import necessary libraries
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import html
import re

# User credentials
email = "assad.g@northeastern.edu"
password = "Gfideliova03!@#$"

# Setup selenium driver
chrome_options = Options()
chrome_options.add_argument("--headless")
# chrome_options.add_extension()
driver = webdriver.Chrome(options=chrome_options)

# Navigate to gradescope.com
driver.get("https://www.gradescope.com/login")

# Automate sign-in process
driver.find_element("id", "session_email").send_keys(email)
driver.find_element("id", "session_password").send_keys(password)
driver.find_element("name", "commit").click()

# Wait until page loads
WebDriverWait(driver, timeout=10).until(lambda x: x.execute_script("return document.readyState === 'complete'"))

# Access problem-selection page
# URL NEEDS TO BE CHANGED DEPENDING ON WHAT USER WANTS TO ACCESS!
driver.get("https://www.gradescope.com/courses/567436/assignments/3290069/submissions/193818048/select_pages")

# Save content and parse
html_content = driver.page_source
driver.quit()
soup = BeautifulSoup(html_content, "html.parser")
main_content = soup.find("main")

# Sort and parse for image links
background_images = main_content.find_all(style=re.compile((r'background-image:\s*url\([^)]+\)')))
image_pattern = r'https://[^"]+'

# Parse image links
result_images = []
for image in background_images:
    url = re.findall(image_pattern, image['style'])
    html.unescape(url)
    result_images.extend(url)

# Parse problem numbers
result_problems = []
problem_outline = soup.find_all('div', class_='selectPagesQuestionOutline--title')
problem_pattern = r'</strong>(.*?)</div>'

# Finalize problem parsing
for problem in problem_outline:
    num = re.search(problem_pattern, str(problem))
    num_parsed = num.group(1).strip()
    if len(num_parsed) <= 3: # Depends how many problems
        result_problems.append(num_parsed)


print(result_images)
print(result_problems)