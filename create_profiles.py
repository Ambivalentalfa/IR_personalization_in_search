from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json
from selenium.webdriver.chrome.service import Service

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
    time.sleep(3)

def url_navigation(driver, results, query, session_id, user_id):
    for i in range(3):#explore 3 of the results
        # get all the titles, have to do it inside the for otherwise doesn't work
        allurls = driver.find_elements(By.CLASS_NAME, 'title')

        #click on random one and save it in the dictionary
        url = allurls[random.randint(1, len(allurls) - 1)].get_attribute('href')
        driver.get(url)
        time.sleep(5)
        results[user_id][session_id][query].append(url)

        driver.back()

def browsing_session(results, user_id, session_id, queries):
    queries_copy = queries #use a copy to be able to remove the visited queries and not visit the same query more times in the same session
    driver = login(set_driver(), results, user_id)
    #at this point the driver is in the bing news page, logged

    results[user_id].update({session_id: {}})#add the session to the user in the results dictionary
    for i in range(5):
        query = queries_copy[random.randint(0, len(queries_copy) - 1)]
        results[user_id][session_id].update({query: []})#add the query to the session in the results dicitonary
        search_news(driver, query)#search the query

        url_navigation(driver, results, query, session_id, user_id)#explore the results and save the vistited urls
        time.sleep(3)
        queries_copy.remove(query)
    driver.close()

def create_results():
    #create the results dictionary
    usernames = ['ggjlbwviowbepibw@outlook.com'] #usernames list
    passwords = ['lea0p0begathe0'] #passwords list
    user_ids = list(range(1, 21)) #userids list

    results = {}
    for id in user_ids[:1]:
        id_dict = {'username': usernames[id - 1], 'password': passwords[id - 1]}
        results.update({str(id): id_dict})

    return results

def main():
    #TO RUN JUST IN THE FIRST SESSION, to create the dictionary
    results_rightwing = create_results()
    #we save the dicitionary in a json and we reuploaded it for the next sessions
    #with open('results_rw.json') as json_file:
        #results_rightwing = json.load(json_file)

    #lists of queries
    q_rw_politics = ['PP espana', 'VOX espana', 'noticias estados unidos', 'migracion ilegal']

    #run in the decided browsing session schedule, with the correspondant session_id
    for user in list(range(1, 2)):
        browsing_session(results_rightwing, str(user), str(2), q_rw_politics)

    #save the session results in the results dictionary
    with open("results_rw.json", "w") as outfile:
         json.dump(results_rightwing, outfile)

main()


#general plan
#users
#30, females
#VPN, location Madrid
#20 users rw and 20 lw
#browsing session
#1 right, 1 left
#4 days, two browsing sessions per day
#save the number of queries and links visited
#10 minutes between each query ?
#number of queries: 1 query for category
#number of links: random number between 2 and 3 for each query
#between 10 and 15 seconds in each link

#enviromental
#do it once before starting and once at the end
#5 enviromental queries for all the users
#save all the results and the rank

#have to decide how to schedule the browsing sessions, maybe one in the morning and one in the afternoon for every user
#for x days, also have to decide the structure of the sessions, how many queries from each list, how many time for each query, ...
#save browsing history in a dictionary like this
#results{
#user id:dict{
    #username: username
    #password: password
    #session_id_value:{
        #query_value: [links visited for the query] }
# } ...
# }
#one dictionary for right wing users one for left wing users
#things to do:
# - create all the profiles, to have usernames and passwords, with the decided age and location
# - finish the queries
# - pass these to this code
# - write a new method to save the results of the enviromental queries results
#   for that queries I think we should save all the results and the rank, this code is just to 'train' the profiles
#   and save the browsing data for completness