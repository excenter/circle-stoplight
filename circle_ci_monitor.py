# -*- coding: utf-8 -*-
import requests
import json
import os
from time import sleep
from stoplight import Stoplight
import threading
import vox


def configErrorHelper(missingConfig):
    print("ERROR: a required config is missing, please make sure you have a complete config.json")
    print(missingConfig)
    # TODO what else would be helpful here? leave a github issue if you have suggestions. #SUG-1


def bootstrap():
    # read config file
    try:
        with open('config.json') as json_file:
            config = json.load(json_file)
    except:
        print("AN ERROR HAS OCCURRED READING THE CONFIG")
        return None
    print("config read")
    # initialize the config variables
    if True:
        token = config.get("CircleCiToken")
        if not token:
            configErrorHelper("token")
            return None
        branches = config.get("branches")
        if not branches:
            configErrorHelper("branches")
            return None
        seconds_delay = config.get("timeDelay")
        if not seconds_delay:
            configErrorHelper("timeDelay")
            return None

        repos = config.get("repos")
        if not repos:
            configErrorHelper("repos")
            return None

        gpio = config.get("gpio")
        if not gpio:
            configErrorHelper("gpio")
            return None
        fakeGpio = config.get("fakeGpio")
        states = config.get("states")
        if not states:
            configErrorHelper("states")
            return None
    print("config initialized")
    # initialize the stoplight class
    lights = Stoplight(states, gpio, fakeGpio)
    print("class initialized")
    # enter the main loop
    print("diving in to the main loop!")
    main_loop(seconds_delay=seconds_delay,
              branches=branches,
              token=token,
              repos=repos,
              lights=lights)


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


def status_to_state(statuses):
    pass
    state = ""
    # this is assuming 1, but built to support multiple
    for status_object in statuses:
        print("printing status_object")
        print(status_object)
        status = status_object.get("status")
        if status == "success" or status == "canceled":
            state = "good"
        elif status == "running" or status == "queued" or status == "not_running" or status == "failing":
            state = "building"
        elif status == "failed" or status == "timedout":
            state = "broken"
    print("state: " + state)
    return state


def main_loop(**kwargs):
    # could this be not, kwarged... probably. but I did it anyway!
    seconds_delay = kwargs.get('seconds_delay')
    branches = kwargs.get('branches')
    token = kwargs.get('token')
    repos = kwargs.get("repos")
    lights = kwargs.get("lights")
    url = ''.join(
        ("https://circleci.com/api/v1.1/projects?circle-token=", token))
    print(url)
    # blink_thread = threading.Thread(
    #     target=lights.blink, args=("green", 0.75, 15))
    previous_state = "null"

    while True:
        current_statuses = get_statuses(
            url=url, repos=repos, branches=branches)

        # print(current_statuses)
        state = status_to_state(current_statuses)
        print("state has been received")

        if previous_state != state:
            vox.play_audio_from_state(previous_state, state)
            if state == "good":
                print("about to start  thread")
                lights.assert_state("null")
                lights.blink("green", 0.75, 5)
                # blink_thread.start()
            else:
                print("state is being asserted")
                lights.assert_state(state)
            sleep(10)
            vox.fadeout(5000)
        else:
            print("received duplicate state")
        # pass statuses to the pi to handle it
        sleep(seconds_delay)
        previous_state = state


if __name__ == "__main__":
    bootstrap()
