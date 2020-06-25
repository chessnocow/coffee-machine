import requests
import os
from collections import deque
from sys import argv
from bs4 import BeautifulSoup
from colorama import Fore, Style


def check_url(url_in):
    if "https://" in url_in:
        return url_in
    else:
        return "https://" + url_in


def create_shortcut(url_in):
    return url_in.rsplit(".", 1)[0]


def create_tab(shortcut_in, body):
    with open(f"{dir_name}/{shortcut_in}.txt", "w") as new_tab:
        new_tab.write(body)


if len(argv) > 1:
    dir_name = argv[1]
else:
    dir_name = "tabs"
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
shortcut_list = []
history = deque()

while True:
    url_input = input()
    if url_input == "exit":
        break
    elif url_input in shortcut_list:
        history.append(url_input)
        with open(f"{dir_name}/{url_input}.txt", "r") as download_page:
            print(Fore.BLUE + download_page.read())
    elif url_input == "back":
        shortcut = history.popleft()
        with open(f"{dir_name}/{shortcut}.txt", "r") as download_page:
            print(download_page.read())
    else:
        try:
            r = requests.get(check_url(url_input))
        except requests.exceptions.ConnectionError:
            print("Error: Incorrect URL")
        else:
            soup = BeautifulSoup(r.content, 'html.parser')
            site = soup.find_all(['p', 'headers', 'a', 'ul', 'ol'])
            lst = [st.get_text() for st in site]
            text = "\n".join(lst)
            for block in site:
                if block.name == 'a':
                    print(Fore.BLUE + block.text)
                else:
                    print(Fore.WHITE + block.text)
            #print(Fore.BLUE + text)

            shortcut = create_shortcut(url_input)
            history.append(shortcut)
            shortcut_list.append(shortcut)
            create_tab(shortcut, text)
