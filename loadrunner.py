import gevent
from locust import HttpUser, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history

from swagger_parser import SwaggerParser


class GeneratedUser(HttpUser):
    wait_time = between(0.1, 2)
    host = "https://postman-echo.com"
    tasks = []


class LoadRunner:
    def __init__(self, config_file):
        self._config = config_file
        self._load_profile = None

        self._load_user = GeneratedUser

    def parse_swagger(self, swagger_json):
        self._load_profile = SwaggerParser(swagger_json).parse()

    def create_load_tasks(self):
        for task in self._load_profile:
            generated_name = f"generated_task_{task['method']}{task['path'].replace('/', '_')}"
            exec(f'def {generated_name}(user):  print(user.client.request("{task["method"]}", url="{task["path"]}", data="{task.get("data")}").json())')
            exec(f'self._load_user.tasks.append({generated_name})')

    def load_targer(self, hostname):
        self._load_user.host = hostname
        # setup Environment and Runner
        env = Environment(user_classes=[GeneratedUser])
        env.create_local_runner()

        # start a WebUI instance
        env.create_web_ui("127.0.0.1", 8089)

        # start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(env.stats))

        # start a greenlet that save current stats to history
        gevent.spawn(stats_history, env.runner)

        # start the test
        env.runner.start(self._config["user_count"], spawn_rate=self._config["spawn_rate"])

        # in 60 seconds stop the runner
        gevent.spawn_later(self._config["duration"], lambda: env.runner.quit())

        # wait for the greenlets
        env.runner.greenlet.join()

        # stop the web server for good measures
        env.web_ui.stop()
