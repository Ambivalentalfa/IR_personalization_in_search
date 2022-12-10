from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

#######FILES_PART#########
#obtain users and passwords list from the files
def users_passwords(file):
    u_p = {}
    u_p.update({'usernames': []})
    u_p.update({'passwords': []})
    with open(file) as f:
        for line in f:
            line = line.replace(" ", "")
            words = line.split('-')
            u_p['usernames'].append(words[0])
            u_p['passwords'].append(words[1].replace('\n', ''))
    return u_p

#create results dictionary
def create_results(file):
    u_p = users_passwords(file)
    usernames = u_p['usernames']  # usernames list
    passwords = u_p['passwords']  # passwords list
    user_ids = list(range(1, 11)) #userids list

    results = {}
    for id in user_ids:
        id_dict = {'username': usernames[id - 1], 'password': passwords[id - 1]}
        results.update({id: id_dict})

    return results

def query_todict(file):
    q_dict={}
    with open(file, encoding='utf-8-sig') as f:
        for line in f:
            if line.startswith(">"):
                header=line.strip(">").strip("\n")
                q_dict[header]=[]
            else:
                q_dict[header].append(line.strip("\n"))
    return q_dict
################

#######SELENIUM_PART#########
def set_driver():
    ser = Service("C:\Drivers\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.implicitly_wait(5)
    return driver

def login(driver, results, user_id):
    driver.get('https://www.bing.com/?wlexpsignin=1')
    time.sleep(4)
    driver.find_element(By.ID, "id_l").click()
    time.sleep(4)
    driver.find_element(By.NAME, "loginfmt").send_keys(results[user_id]['username'])
    time.sleep(4)
    driver.find_element(By.ID, "idSIButton9").click()
    time.sleep(4)
    driver.find_element(By.NAME, "passwd").send_keys(results[user_id]['password'])
    time.sleep(4)
    driver.find_element(By.ID, "idSIButton9").click()
    time.sleep(4)
    try:
        driver.find_element(By.ID, "iShowSkip").click()
        time.sleep(4)
    except NoSuchElementException:
        print('')
    try:
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(4)
    except NoSuchElementException:
        print('')
    try:
        driver.find_element(By.ID, "iCancel").click()
        time.sleep(4)
    except NoSuchElementException:
        print('')
    if (driver.current_url != 'https://www.bing.com/?wlexpsignin=1&wlexpsignin=1'):
        print('login problem')
        exit(1)
    return driver

def search_news(driver, query):
    driver.get("https://www.bing.com/news")
    time.sleep(4)
    q = driver.find_element(By.ID, "sb_form_q")
    q.clear()
    q.send_keys(query)
    time.sleep(2)
    q.send_keys(Keys.ENTER)
    time.sleep(5)

#save the first 10 urls of the search page
def save_results(driver, results, query, session_id, user_id):
    allurls = driver.find_elements(By.CLASS_NAME, 'title')
    for url in allurls[:10]:
        results[user_id][session_id][query].append(url.get_attribute('href'))
    # time.sleep(2)
    # driver.execute_script("window.history.go(-1)")
    time.sleep(3)

def user_session(results, user_id, session_id, queries):
    driver = login(set_driver(), results, user_id)
    #at this point the driver is logged
    results[user_id].update({session_id: {}})#add the session to the user in the results dictionary
    #for each query
    for category in list(queries.keys()):#general, biased
        for query in queries[category]:
            results[user_id][session_id].update({query: []})#add the query to the session in the results dicitonary
            search_news(driver, query)#search the query
            driver.save_screenshot("image"+str(user_id)+str(query)+".png")
            save_results(driver, results, query, session_id, user_id)#save the first 10 results
            time.sleep(3)

    driver.close()

def browsing_session(results_rightwing, results_leftwing, queries, session_id):
    for id in list(range(1,11)):
        # user of rigth wing
        print("user number:", id, " right wing")
        user_session(results_rightwing, id, str(session_id), queries)
        time.sleep(60)
        # user of left wing
        print("user number:", id, " left wing")
        user_session(results_leftwing, id, str(session_id), queries)
################

def main():
    #RESULTS, TO RUN JUST IN THE FIRST SESSION, to create the dictionary
    results_rightwing_env = create_results('users_right.txt')
    results_leftwing_env = create_results('users_left.txt')
    #we save the dicitionary in a json and we reuploaded it for the next sessions
    #with open('results_rightwing_env.json') as json_file:
        #results_rightwing_env = json.load(json_file)

    #ENVIROMENTAL QUERIES
    fileenv = "Qenv.txt"
    q_env = query_todict(fileenv)

    #BROWSING SESSION HAVE TO CHANGE JUST THE SESSION_ID, here should be just 2 sessions
    browsing_session(results_rightwing_env, results_leftwing_env, q_env, 3)
    # for id in list(range(1,11)):
    #     driver = set_driver()
    #     #login(driver, results_rightwing_env, id)
    #     login(driver, results_leftwing_env, id)

    #save the session results in the results dictionary
    with open("results_rw_env_3.json", "a") as outfile:
         json.dump(results_rightwing_env, outfile)
    with open("results_lw_env_3.json", "a") as outfile:
         json.dump(results_leftwing_env, outfile)

main()
#f = open('results_lw_env.json')
#data = json.load(f)
#print(len(data['1']['1']['energias renovables posibilidades']))
