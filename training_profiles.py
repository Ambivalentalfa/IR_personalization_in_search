from selenium import webdriver
import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import time
import random
import json
from selenium.webdriver.chrome.service import Service
import threading

########FILES PART##########
#save time of the sessions
def report(file, string, id):
    f = open(file, "a")
    f.write(string + " " + str(id) + ": " + str(datetime.now()) + "\n")

#read queries from files
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

#create the results file
def create_results(file):
    #create the results dictionary
    u_p = users_passwords(file)
    usernames = u_p['usernames']#usernames list
    passwords = u_p['passwords'] #passwords list
    user_ids = list(range(1, 11)) #userids list

    results = {}
    for id in user_ids:
        id_dict = {'username': usernames[id - 1], 'password': passwords[id - 1]}
        results.update({str(id): id_dict})

    return results
###################

######SELENIUM_PART#########
#set the driver
def set_driver():
    ser = Service("C:\Drivers\chromedriver.exe")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.implicitly_wait(15)
    return driver

#login
def login(driver, results, user_id):
    driver.get('https://www.bing.com/?wlexpsignin=1')
    time.sleep(15)
    driver.find_element(By.ID, "id_l").click()
    time.sleep(5)
    driver.find_element(By.NAME, "loginfmt").send_keys(results[user_id]['username'])
    time.sleep(5)
    driver.find_element(By.ID, "idSIButton9").click()
    time.sleep(5)
    driver.find_element(By.NAME, "passwd").send_keys(results[user_id]['password'])
    time.sleep(5)
    driver.find_element(By.ID, "idSIButton9").click()
    time.sleep(5)
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
        sys.exit(1)
    return driver

#get the news page, search a query
def search_news(driver, query):
    driver.get("https://www.bing.com/news")
    time.sleep(4)
    q = driver.find_element(By.ID, "sb_form_q")
    q.clear()
    q.send_keys(query)
    time.sleep(2)
    q.send_keys(Keys.ENTER)
    time.sleep(5)

def url_navigation(driver, results, query, session_id, user_id):
    allurls = driver.find_elements(By.CLASS_NAME, 'title')
    if(len(allurls) >= 2):
        #just look at the best ranked
        url = allurls[random.randint(1, round(len(allurls)/2))].get_attribute('href')

        driver.get(url)

        time_for_link = random.randint(5, 10)
        time.sleep(time_for_link)
        # save it in results
        results[user_id][session_id][query].append(url)

def user_session(res_str, results, user_id, session_id, queries):
    driver = login(set_driver(), results, user_id)
    #at this point the driver is logged
    results[user_id].update({session_id: {}})#add the session to the user in the results dictionary
    for category in queries.keys():
        for i in range(2):
            #randomly select two queries
            if(len(queries[category]) >= 2):
                query = queries[category][random.randint(0, len(queries[category]) - 1)]
                if query not in list(results[user_id][session_id].keys()):
                    results[user_id][session_id].update({query: []})#add the query to the session in the results dicitonary
                search_news(driver, query)#search the query
                url_navigation(driver, results, query, session_id, user_id)#explore the results and save the vistited urls
            else:
                print('problem with len(queries:copy)')
    #save the results of the user session
    with open(res_str + "_session"+session_id+"_user"+user_id+".json", "w") as outfile:
        json.dump(results, outfile)
    driver.close()
#########################

#to check the obtained results
def explore_results(results, session_id):
    print("number of users: ", len(list(results.keys())))
    for users in results.keys():
        if session_id in list(results[users].keys()):
            print("user ", users," number of queries", len(list(results[users][session_id].keys())))
            for queries in results[users][session_id].keys():
                print("urls ", len(results[users][session_id][queries]))
        else:
            print('problem with user: ', users)

#single user session
def window(res_str, results_rightwing, id, session_id, q_rw):
    user_session(res_str, results_rightwing, str(id), str(session_id), q_rw)
    time.sleep(10)

def main():
    session_id = sys.argv[1]
    print(session_id)
    results_rightwing = create_results('users_right.txt')
    results_leftwing = create_results('users_left.txt')

    q_lw = query_todict("Qleft.txt")
    q_rw = query_todict("Qright.txt")

    report("report.txt", "Starting session", str(session_id))
    for id in list(range(1,11)):
        print('right wing ', str(id))
        t1 = threading.Thread(target=window, args=("resultsRW", results_rightwing, id, session_id, q_rw))
        print('left wing ', str(id))
        t2 = threading.Thread(target=window, args=("resultsLW", results_leftwing, id, session_id, q_lw))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    report("report.txt", "Ending session", str(session_id))
    with open("results_rw_" + str(session_id) +".json", "w") as outfile:
         json.dump(results_rightwing, outfile)
    with open("results_lw_" + str(session_id) +".json", "w") as outfile:
         json.dump(results_leftwing, outfile)

main()
