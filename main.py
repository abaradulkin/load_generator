import json
import argparse

from loadrunner import LoadRunner

import requests  # https://github.com/gevent/gevent/issues/1016


def fetch_file(file_path):
    if file_path.startswith("http"):
        return requests.get(file_path).json()
    else:
        with open(file_path, "r") as file:
            return json.load(file)



def __parse_args():
    args = argparse.ArgumentParser()
    args.add_argument("target", help="Host URL to be loaded", type=str)
    args.add_argument("swagger_json", help="Path or URL to swagger file", type=str)
    args.add_argument("config", help="Path to load config file", type=str)
    return args.parse_args()


def main():
    args = __parse_args()

    swagger_json = fetch_file(args.swagger_json)
    # swagger_json = fetch_file("https://apiconsole.ru1.wallarm.ru/swagger.json")
    config_json = fetch_file(args.config)
    # config_json = fetch_file("./config.json")
    hostname = args.target
    # hostname = "http://postman-echo.com"

    loadrunner = LoadRunner(config_json)
    loadrunner.parse_swagger(swagger_json)
    loadrunner.create_load_tasks()
    loadrunner.load_targer(hostname)


if __name__ == "__main__":
    main()


