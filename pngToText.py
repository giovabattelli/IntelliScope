import os, io
import requests
from io import BytesIO
from google.cloud import vision_v1
from pdf2image import convert_from_path
from google.cloud import vision

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

# WILL TAKE INPUT FROM GRADESCOPE.PY
test_pdf_path = 'resources/testPDF.pdf'
image_url = 'https://production-gradescope-uploads.s3-us-west-2.amazonaws.com/uploads/page/file/855388146/page_3.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAV45MPIOW2IZ34NWW%2F20230917%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230917T062613Z&X-Amz-Expires=10800&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJ7%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIFnUiXsqXt2fUguI3BmEfEwdBZkt7b%2F%2BW1FN7FXyjH3qAiEA0jpZ83D9818K%2FJM0ClI7rR%2FRf8AKpH31cQALi2j2Sr4qxAUIh%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw0MDU2OTkyNDkwNjkiDIHs35YuN7GDVZLRGiqYBa1uM0UlcbiqAptKnIDvI8qV8BONNnvRms1gKDYg2MJo1PmPc7sPgZ9UsmKFJmDLshfF5nKmZz1AsJtr1irtlyxqCJyAOmpTnYSmykkA%2BsfEzgcv5qaBdmsDdlK8lGKcEE%2BUH69XY2cW%2FRTm7sMFUul8uRNCRaFX%2FZ0uIIYz6nhBfBBHM1gCX4IFwxzIHDwQj45Vzqt6B1lcjA80t2qvKNyaGGFO62DdTdOp36hHLsKWS%2B3bzKMDjAHzIFXRThUVFlyOSL8vA6RQydik5m8SGoZST7YaNVnoQ7c8IGpX118ZE2EUJQ6PCsPCNpmdk9QjwD4EKNjIX%2BpnYuRueZPU63IGo3iUlVKF4a4MAG9KZU9L7Bgjs4UyEB%2BajY2rV6GUdEiNkF21IfQBEezBz98ki569h6Xb7L0Odef8cRJrqvqHTvmYRUoW9HWWxNOjBkTdD%2BUSadN%2FEXyvG%2BsFR5NY1YYi%2BTHeI0%2BrN0cFd98i1%2Bo01DynSM2rVkk5C4MHpBYYZ7smdZTNw4jkx1hsK9PNtt7WL7nt%2FXsFkU0pAJrgSZ3vHcniFim3YjhITJuOaOsOPMbmu9dURRsmh016rw2a%2FYwc1avqcpVihwlzrMNiHXEQ9ffmZLFYyLyy%2FCSuk7%2Bmo1%2FuD6UhwjISDXMbbdxww69inzIxersSNxMYk4ekeRHS%2Fyu%2B6Ph0myNT%2F0jPIvuH9X3%2B88zXfAwAfyuBX13uvjZTmMXPUGKk8hE83VnMGRCfe%2B9MP2MpxWPdwRYtnSdfW9MKDwbWL%2BytDQO9oTmj8nKp%2F0AP8pKGg7FFmCXHSBH8UTpiFxzHA%2F%2FRSWn65Z9XT7lP9LGwNmmlgIhEq4y611sTAM%2F2f3nh7g89qLIydMThjmHfFZhwIpYwzq6aqAY6sQGwDCfxj2%2FsC2DbbmIJTtWrP0NDIEt3lMQoyTNonI4MsjpT24YZAgPZeDQt8BHDjlLCwPar4KXeom9pPE2bCqC6Q2DaSAWU9tWwVzbt%2FBZJBMwJtyfOdX1aa2t3cGd7zQPQ%2BoQbfh6IZ5tyER1e8jZi3nttBoookndo8dDvTsEMkoP37y%2FF5SsaTrDAGi0qmjS6vdwn4ScuJulzRC978oOH8Iaf4Y%2Ffs9KTnROUI0ljR9o%3D&X-Amz-SignedHeaders=host&X-Amz-Signature=5c6202c8e541980afed5bbf3c79a10c2a917633f29f2a4987dbbcda52a24d476'
arr_of_img_urls = ['resources/page0.png', 'resources/page1.png', 'resources/page2.png']
example_list_of_problems = ['1.', '2.', '3a.', '3b.', '3c.', '3d.', '3e.', '3f.', '3g.', '4.', '5.']

# test list of problems and page contents for testing problem_and_pages:
test1 = ["1a. blah blah balh\nblah blah bklah\nblah blah\n1b. hello everyone!!!!!\n", "1c. blah blah balh\nblah blah bklah\nblah blah\n2. hello ebveryone!!!!!\n", "2nd question continued over here\n3. Debugging this is nutssss.\n help me\n"]
test2 = ['1a', '1b', '1c', '2', '3']

# converts the given image URL to text
# the output's page numbers correspond to the index in the array + 1
def image_url_to_text(image_urls):

    strings = []

    client = vision_v1.ImageAnnotatorClient.from_service_account_file('ServiceAccountToken.json')
    
    for url in image_urls:
        response = requests.get(url)
        image_data = response.content
        url = vision_v1.Image(content=image_data)
        response = client.text_detection(image=url)
        texts = response.text_annotations
        strings.append(texts[0].description)
    return strings

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# takes in a list of strings (image texts) and another list of strings (problem numbers) and returns a hashmap 
# with the key being a problem number and the value being an array of integers corresponding to the problem number's
# associated pages
# IN ORDER FOR BEST RESULTS, PROBLEM NUMBER WILL ALWAYS FOLLOW THE FOLLOWING FORMAT:
# - BEGINNING OF LINE + NUMBER + PART OF PROBLEM + '.'
# - example: '1a.' or '2c.' or '42e.' or '1)' or '5)'
# - Since we are getting the problem numbers from the website, please follow the exact format used in gradescope.
# - It is assumed that each problem number will always be on the left-most side of the line, to allow for easy
#   parsing of textual information
# - All numbering should be in the same vertical column across all pages of the assignment 

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

print(page_assigner(test1, test2))
# print(page_assigner(image_url_to_text(arr_of_img_urls), example_list_of_problems))
