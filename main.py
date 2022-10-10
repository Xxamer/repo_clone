#!/usr/bin/env python3
import os
from venv import create
import requests
import inquirer
from dotenv import load_dotenv
load_dotenv()
URL = os.getenv('GITHUB_USER_REPOSITORIES')
TOKEN = os.getenv('GITHUB_BEARER')
REPOSITORIES = []
def main():
    repositories_name = getListOfRepositories()
    repository_to_clone = createList(repositories_name)
    print("Cloning..." + repository_to_clone)
    os.system("git clone " + repository_to_clone )
  

def createList(repositories_name):
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
            return repository_link['url']

def getListOfRepositories():
    names = []
    headers = { 'Authorization': "Bearer " + TOKEN }
    # # List repositories
    github_repositories = requests.get(URL, headers = headers)
    data = github_repositories.json()
    # Display names and  push it to display them
    for item in data:
     REPOSITORIES.append({ "name":item['full_name'], 
                          "url": item['ssh_url'] })
     names.append(item['full_name'])
    return names

if __name__ == '__main__':
    main()
    