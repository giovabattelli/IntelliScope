# Import necessary libraries
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify, request
from selenium import webdriver
from bs4 import BeautifulSoup
import html
import re

#Use email and password data from popup.js to login to Gradescope
app = Flask(__name__)

@app.route('/get-data', methods=['POST'])
def get_data():
    global received_email, received_password
    received_data = request.json
    received_email = received_data.get('email')
    received_password = received_data.get('password')
    return jsonify({"email": received_email, "password": received_password})

if __name__ == '__main__':
    app.run(port=5000)

email, password = get_data()

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