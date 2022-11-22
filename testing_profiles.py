from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
from selenium.webdriver.chrome.service import Service

#save the results in a dictionary like this
#one for each wing, 2 in total
#here we group togheter general and biased, if we want to analyse separately we just use the fact that the first 5
#are always the general and the last five are always the biased
#user_id:dict{username: .. , password: .. , session_id: {query : [top 10 results ranked]}}
def create_results():
    #create the results dictionary
    usernames = ['ggjlbwviowbepibw@outlook.com'] #usernames list
    passwords = ['lea0p0begathe0'] #passwords list
    user_ids = list(range(1, 21)) #userids list

    results = {}
    for id in user_ids[:1]:
        id_dict = {'username': usernames[id - 1], 'password': passwords[id - 1]}
        results.update({id: id_dict})

    return results

def query_todict(file):
    q_dict={}
    with open(file) as f:
        for line in f:
            if line.startswith(">"):
                header=line.strip(">").strip("\n")
                q_dict[header]=[]
            else:
                q_dict[header].append(line.strip("\n"))
    return q_dict

def set_driver():
    ser = Service("C:\Drivers\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.implicitly_wait(0.5)
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
    driver.get("https://www.bing.com/news")
    time.sleep(4)
    return driver

def search_news(driver, query):
    q = driver.find_element(By.ID, "sb_form_q")
    q.clear()
    q.send_keys(query)
    time.sleep(2)
    q.send_keys(Keys.ENTER)
    time.sleep(5)

def save_results(driver, results, query, session_id, user_id):
    allurls = driver.find_elements(By.CLASS_NAME, 'title')
    for url in allurls[:10]:
        results[user_id][session_id][query].append(url.get_attribute('href'))
    time.sleep(2)
    driver.back()
    time.sleep(3)

def user_session(results, user_id, session_id, queries):
    driver = login(set_driver(), results, user_id)
    #at this point the driver is in the bing news page, logged
    results[user_id].update({session_id: {}})#add the session to the user in the results dictionary
    #for each query
    for category in queries.keys():#general, biased
        for query in queries[category][:1]:
            results[user_id][session_id].update({query: []})#add the query to the session in the results dicitonary
            search_news(driver, query)#search the query
            save_results(driver, results, query, session_id, user_id)#save the first 10 results
            time.sleep(3)

    driver.close()

def browsing_session(results_rightwing, results_leftwing, queries, session_id):
    for id in list(range(1,2)):
        # user of rigth wing
        user_session(results_rightwing, id, str(session_id), queries)
        time.sleep(60)#how much??
        # user of left wing
        user_session(results_leftwing, id, str(session_id), queries)

def main():
    #RESULTS, TO RUN JUST IN THE FIRST SESSION, to create the dictionary
    results_rightwing_env = create_results()
    results_leftwing_env = create_results()
    #we save the dicitionary in a json and we reuploaded it for the next sessions
    #with open('results_rightwing_env.json') as json_file:
        #results_rightwing_env = json.load(json_file)

    #ENVIROMENTAL QUERIES
    fileenv = "Qenv.txt"
    q_env = query_todict(fileenv)

    #BROWSING SESSION HAVE TO CHANGE JUST THE SESSION_ID, here should be just 2 sessions
    browsing_session(results_rightwing_env, results_leftwing_env, q_env, 1)

    #save the session results in the results dictionary
    with open("results_rw_env.json", "w") as outfile:
         json.dump(results_rightwing_env, outfile)
    with open("results_lw_env.json", "w") as outfile:
         json.dump(results_leftwing_env, outfile)

main()