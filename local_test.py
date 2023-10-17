from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup
import html
import re

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(options=chrome_options)


def login_to_gradescope(driver, email, password):
    driver.get("https://www.gradescope.com/login")
    driver.find_element("id", "session_email").send_keys(email)
    driver.find_element("id", "session_password").send_keys(password)
    driver.find_element("name", "commit").click()
    
    WebDriverWait(driver, timeout=10).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )


def navigate_to_problem_selection(driver, url):
    driver.get(url)
    html_content = driver.page_source
    return BeautifulSoup(html_content, "html.parser")


def get_image_links(soup):
    main_content = soup.find("main")
    background_images = main_content.find_all(style=re.compile((r'background-image:\s*url\([^)]+\)')))
    image_pattern = r'https://[^"]+'
    result_images = []
    for image in background_images:
        url = re.findall(image_pattern, image['style'])
        html.unescape(url)
        result_images.extend(url)

    return result_images


def get_problem_numbers(soup):
    result_problems = []
    problem_outline = soup.find_all('div', class_='selectPagesQuestionOutline--title')
    problem_pattern = r'</strong>(.*?)</div>'
    for problem in problem_outline:
        num = re.search(problem_pattern, str(problem))
        num_parsed = num.group(1).strip()
        if len(num_parsed) <= 3:
            result_problems.append(num_parsed)
    
    return result_problems


def question_selector(driver, question):
    # Take the nums from the map from the other code
    page_nums = [[0], [0], [1], [1, 2], [2]]
    question_list = driver.find_elements("class name", 
    "selectPagesQuestionOutline--item")
    images_list = driver.find_elements("class name", "pageThumbnail--selector")

    #TEST 
    # print(len(question_list))
    # print(len(images_list))

    for index, question_element in enumerate(question_list):
        index -= 1
        if question in question_element.text:
            #TESTING PRE CHANGE HTML
            # print("OLD")
            # div_html_pre = driver.execute_script("return arguments[0].outerHTML;", question_element)
            # print(div_html_pre)

            #Select the question
            driver.execute_script("arguments[0].click();", question_element)

            #Select the pages
            #The website's js should detect the click and perform the tagging process to save the selection
            for page_num in page_nums[index]:
                driver.execute_script("arguments[0].click();", images_list[page_num])

            #TESTING CHANGES
            # print("NEW")
            # div_html = driver.execute_script("return arguments[0].outerHTML;", question_element)
            # print(div_html)
            # div_html_image = driver.execute_script("return arguments[0].outerHTML;", images_list[page_nums[index][0]])
            # print(div_html_image)
            # print("")
    

if __name__ == "__main__":
    #email and password removed during publishing
    email = ""
    password = ""

    driver = setup_driver()
    login_to_gradescope(driver, email, password)
    
    soup = navigate_to_problem_selection(driver, "https://www.gradescope.com/courses/567436/assignments/3461579/submissions/203094601/select_pages")
    
    image_links = get_image_links(soup)
    problem_numbers = get_problem_numbers(soup)

    question_selector(driver, "1a")
    question_selector(driver, "1b")

    # for question in problem_numbers:
    #     question_selector(driver, question)
    
    driver.quit()



