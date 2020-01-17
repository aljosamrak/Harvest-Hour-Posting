#!/usr/bin/python

import configparser
import datetime
import json
import urllib.request
from urllib.parse import urlencode
from tabulate import tabulate


def make_rest_call(url, header, data=None):
    request = urllib.request.Request(url=url, headers=header, data=data)
    response = urllib.request.urlopen(request, timeout=5)
    response_body = response.read().decode("utf-8")
    return json.loads(response_body)


def get_client_id(header):
    url = "https://api.harvestapp.com/v2/users/me"
    return make_rest_call(url, header)['id']


def print_project_task_ids(header):
    url = "https://api.harvestapp.com/v2/time_entries"
    time_entries = make_rest_call(url, header).get("time_entries")

    data = set()
    for time_entry in time_entries:
        project = time_entry['project']
        task = time_entry['task']
        data.add((project['name'], project['id'], task['name'], task['id']))

    print(tabulate(data, headers=['Project', 'Project ID', 'Task', 'Task ID']))


def get_hours_for_day(date, header):
    url = "https://api.harvestapp.com/v2/time_entries?from=%s&to=%s" % (date, date)
    time_entries = make_rest_call(url, header).get("time_entries")

    current_hours = 0
    for time_entry in time_entries:
        current_hours += time_entry['hours']

    return current_hours


def create_time_entry(project_id, task_id, date, hours, header):
    url = "https://api.harvestapp.com/v2/time_entries"

    client_id = get_client_id(header)

    data = urlencode(
        {
            "user_id": client_id,
            "project_id": project_id,
            "task_id": task_id,
            "spent_date": date,
            "hours": hours
        }).encode()
    return make_rest_call(url, header, data)


def main():
    # read config file
    config = configparser.ConfigParser()
    config.read("config.ini")

    access_token = config['global']['access_token']
    account_id = config['global']['account_id']
    wanted_hours = config.getfloat('global', 'wanted_hours')
    project_id = config['global']['project_id']
    task_id = config['global']['task_id']

    # generate header for rest calls
    header = {
        "User-Agent": "Python Harvest API Sample",
        "Authorization": "Bearer " + access_token,
        "Harvest-Account-ID": account_id
    }

    current_date = datetime.datetime.today().strftime('%Y-%m-%d')

    # print project and tasks info
    print_project_task_ids(header)

    # get hours for today
    current_hours = get_hours_for_day(current_date, header)
    still_needed_hours = wanted_hours - current_hours

    # track missing hours
    if still_needed_hours > 0:
        print(create_time_entry(project_id, task_id, current_date, still_needed_hours, header))


if __name__ == "__main__":
    main()
