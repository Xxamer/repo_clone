#!/usr/bin/env python3
import os
from venv import create
import requests
import inquirer
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('GITHUB_USER_REPOSITORIES')
TOKEN = os.getenv('GITHUB_BEARER')
ALREADY_EXIST = 0
REPOSITORIES = []
def main():
    repositories_name = getListOfRepositories()
    repository_to_clone = createList(repositories_name)
    print("Cloning..." + repository_to_clone)
    if ALREADY_EXIST:
        os.system("git pull " + repository_to_clone )
    else:
        os.system("git clone " + repository_to_clone)

def createList(repositories_name):
    global ALREADY_EXIST
    question = [
    inquirer.List('repository_name',
                message= "Which one do you want to clone?",
                choices= repositories_name,
            ),
    ]
    answer = inquirer.prompt(question)
    repository_to_clone = answer['repository_name']
        
    for repository_link in REPOSITORIES:
        if repository_link['name'] == repository_to_clone:  
                if os.path.exists(repository_link['folder_name']):
                    ALREADY_EXIST = 1
                    return repository_link['url']
                else:
                    ALREADY_EXIST = 0
                    return repository_link['url']
        

def getListOfRepositories():
    names = []
    headers = { 'Authorization': "Bearer " + TOKEN }
    # List repositories
    github_repositories = requests.get(URL, headers = headers)
    data = github_repositories.json()
    # Display names and  push it to display them
    for item in data:
     REPOSITORIES.append({ "name":item['full_name'], 
                           "folder_name": item['name'], 
                           "url": item['ssh_url'] })
     names.append(item['full_name'])
    return names

if __name__ == '__main__':
    main()
    