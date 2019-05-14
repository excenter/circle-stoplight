import requests
import json
import os
from time import sleep


def configErrorHelper():
    print("ERROR: a required config is missing, please make sure you have a complete config.json")
    # TODO what else would be helpful here? leave a github issue if you have suggestions. #SUG-1


def bootstrap():
    # initialize the variables
    try:
        with open('config.json') as json_file:
            config = json.load(json_file)
    except:
        print("AN ERROR HAS OCCURRED READING THE CONFIG")
        return None

    token = config.get("CircleCiToken")
    if not token:
        configErrorHelper()
        return None
    branches = config.get("branches")
    if not branches:
        configErrorHelper()
        return None
    seconds_delay = config.get("timeDelay")
    if not seconds_delay:
        configErrorHelper()
        return None
    repos = config.get("repos")
    if not repos:
        configErrorHelper()
        return None
    main_loop(seconds_delay=seconds_delay,
              branches=branches,
              token=token,
              repos=repos)


def get_statuses(**kwargs):
    branches = kwargs.get('branches')
    url = kwargs.get('url')
    repos = kwargs.get("repos")
    current_statuses = []

    response = requests.get(url).json()
    # print(response)
    for project in response:
        repoName = project.get("reponame")
        # print(repoName)
        if repoName in repos:
            # print(repoName)
            for branch in branches:
                # print(branch)
                # print(project.get("branches").get(branch))
                # print(project.get("branches").get(
                #     branch).get("latest_workflows"))
                last_worflows = project.get("branches").get(
                    branch).get("latest_workflows")

                # handle build error in the response
                if last_worflows.get("Build%20Error"):
                    del last_worflows["Build%20Error"]
                # print(len(last_worflows))
                for workflow in last_worflows:
                    # print(workflow)
                    status = last_worflows.get(workflow).get("status")
                    # print(status)
                    object = {
                        "repo": repoName,
                        "branch": branch,
                        "status": status
                    }
                    current_statuses.append(object)
    return current_statuses


def main_loop(**kwargs):
    # could this be not, kwarged... probably. but I did it anyway!
    seconds_delay = kwargs.get('seconds_delay')
    branches = kwargs.get('branches')
    token = kwargs.get('token')
    repos = kwargs.get("repos")
    url = ''.join(
        ("https://circleci.com/api/v1.1/projects?circle-token=", token))
    print(url)
    while True:
        current_statuses = get_statuses(
            url=url, repos=repos, branches=branches)

        print(current_statuses)
        sleep(seconds_delay)


bootstrap()
