import sys 
import argparse
import json
import selenium
from selenium import webdriver


def get_links(name):
    with open('bookmark_urls') as fi:
        dic = json.load(fi)
    return dic.get(name,0)


def get_all_names():
    with open('bookmark_urls') as fi:
        dic = json.load(fi)
    return list(dic.keys(),)


def initialize_driver(bookmark_name):
    urls = get_links(bookmark_name)
    if not urls:
        sys.exit(f"{bookmark_name} is not in {get_all_names()}")
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(urls[0])
    for url in urls[1:]:
        driver.execute_script('window.open("{}", "_blank");' .format(url))
    return driver


def retrive_urls(driver):
    urls = []
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        urls.append(driver.current_url)
    return urls


def save(name, urls):    # problem if the old name is used it will get overwrite in case 1 & 3
    with open("bookmark_urls") as f:
        dic = json.load(f)
    dic[name] = urls
    
    with open("bookmark_urls","w") as f:
        json.dump(dic,f,indent=4)

    with open("backup.txt",'a') as f:
        f.write(name+"\n")
        for url in urls:
            f.write(url+"\n")



#driver = webdriver.Chrome(executable_path='chromedriver')
parser = argparse.ArgumentParser()
parser.add_argument("-n","--bookmark_name",help="enter the bookmark_name",default="newDict")
args = parser.parse_args()

new_bookmark = 0
if args.bookmark_name == "newDict":
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("https://www.google.com")
    new_bookmark = 1
else:
    driver = initialize_driver(args.bookmark_name)

while True:
    answer = input()
    try:
        driver.current_url
    except Exception:
        sys.exit('browser was already closed')

    if answer.strip().lower() in ["quit","exit","close","abort"]:
        urls = retrive_urls(driver)
        driver.set_window_size(1000,20)
        if new_bookmark:
            choice =  input("enter a name to save the bookmark or type 'q' to quit without saving  ")
            if choice.strip() != "N":
                save(choice.strip(), urls);  # case 1
        else:
            choice = input("enter \n'1' to save with old name\n'2' to save with new name\n'3' to quit\n")
            if choice.strip() == "1":
                save(args.bookmark_name, urls);   # case 2
            if choice.strip() == "2":
                save(input("enter name to save bookmark").strip(), urls);  # case 3

        driver.quit()
        break
    else:
        print("enter exit to quit")








