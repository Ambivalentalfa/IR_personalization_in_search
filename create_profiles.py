from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
from selenium.webdriver.chrome.service import Service

#this method takes in input a file and returns a dictionary with the following structure
#q_dict={category1: [list of queries for category1], ... }

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

#may need to check how to disable some extra questions during login, probably possible in account setups
#but I think it's needed just the first time
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

def url_navigation(driver, results, query, session_id, user_id):
    links_number = random.randint(2,3)
    for i in range(links_number):#explore 2 or 3 of the results
        # get all the titles, have to do it inside the for otherwise doesn't work
        allurls = driver.find_elements(By.CLASS_NAME, 'title')

        #click on random one and save it in the dictionary
        url = allurls[random.randint(1, len(allurls) - 1)].get_attribute('href')
        driver.get(url)
        time_for_link = random.randint(10, 15)
        time.sleep(time_for_link)#stay from 10 to 15 seconds on the url
        results[user_id][session_id][query].append(url)

        driver.back()
        time.sleep(3)

def user_session(results, user_id, session_id, queries):
    driver = login(set_driver(), results, user_id)
    #at this point the driver is in the bing news page, logged
    results[user_id].update({session_id: {}})#add the session to the user in the results dictionary
    #for each category
    for category in queries.keys():
        #randomly select one query
        query = queries[category][random.randint(0, len(queries[category]) - 1)]
        results[user_id][session_id].update({query: []})#add the query to the session in the results dicitonary
        search_news(driver, query)#search the query
        url_navigation(driver, results, query, session_id, user_id)#explore the results and save the vistited urls
        time.sleep(3)

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

def browsing_session(results_rightwing, results_leftwing, q_rw, q_lw, session_id):
    for id in list(range(1,2)):
        #user_rw = results_rightwing[id]['username']
        #user_lw = results_leftwing[id]['username']
        # user of rigth wing
        user_session(results_rightwing, id, str(session_id), q_rw)
        time.sleep(60)#how much??
        # user of left wing
        user_session(results_leftwing, id, str(session_id), q_lw)

def main():
    #RESULTS, TO RUN JUST IN THE FIRST SESSION, to create the dictionary
    results_rightwing = create_results()
    results_leftwing = create_results()
    #we save the dicitionary in a json and we reuploaded it for the next sessions
    #with open('results_rw.json') as json_file:
        #results_rightwing = json.load(json_file)

    #QUERIES
    filelw = "Qleft.txt"
    q_lw = query_todict(filelw)
    filerw = "Qright.txt"
    q_rw = query_todict(filerw)

    #BROWSING SESSION HAVE TO CHANGE JUST THE SESSION_ID
    browsing_session(results_rightwing, results_leftwing, q_rw, q_lw, 1)

    #save the session results in the results dictionary
    with open("results_rw.json", "a") as outfile:
         json.dump(results_rightwing, outfile)
    with open("results_lw.json", "a") as outfile:
         json.dump(results_leftwing, outfile)

main()
