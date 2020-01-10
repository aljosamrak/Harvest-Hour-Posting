# Harvest-Hour-Posting
Python scripts that fill the hours up to a quota

## Requirements
Any aditional packages that nees to be installed are installed by executing the [install.sh](install.sh) script.
```sh
$ chmod +x install.sh
$ ./install.sh
```

## Configuration
To run the script, you must define the config.ini file. An [example config file](config-example.ini) is provided.

**access_token** Generate it on https://id.getharvest.com/developers
**account_id**  Once access token is created click on the account id will be written there
**wanted_hours** is the amount of hours wanted to be logged
**project_id** and **task_id** can be found by running the script and cop-ing the ids of the desired project and task form the out of the program