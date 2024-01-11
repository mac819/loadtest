import os
import json
import requests
from pathlib import Path
from locust import TaskSet, HttpUser, between, task, events
from event_influx_handler import EventInfluxHandler

HOME_DIR = str(Path.cwd())
# IP="127.0.0.1"

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("........... Initialize Load Test .......... ON_TEST_START")

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print(".......... Load Test Completed .......... ON_TEST_STOP")


class MlappTask(TaskSet):

    def on_start(self):
        print(".......... Hitting ml_app: Task execution started ..........")
        print("===== Loading Payload =====")
        self.payload = self.__load_payload(filename=os.path.join(HOME_DIR, "data", "api_input.json"))

    def __load_payload(self, filename):
        with open(filename, "r") as f:
            payload = json.load(f)
        return payload

    def on_stop(self):
        print(".......... Hitting ml_app: Task execution completed ..........")

    @task
    def hit_ml_app(self,):
        print(".......... Calling ml_app ..........")
        with self.client.post("/predict", json=self.payload, catch_response=True) as response:

            if response.status_code != 200:
                print("Request NOT successfull")
            elif isinstance(json.loads(response.text), dict):
                if json.loads(response.text).get("result"):
                    response.success()
                else:
                    response.failure(f"Failed to hit ml app, Text: {response.text}")
            else:
                response.failure(f"Failed to hit ml app with status code: {response.status_code}")


class MyUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [MlappTask]

    def on_start(self):
        print(".......... MyUser: Hatching New User ..........")

    def on_stop(self):
        print(".......... MyUser: Deleting User ..........")




# if __name__=="__main__":

#     endpoint = "http://127.0.0.1:49899/predict"
#     header = {
#         "Content-Type": "application/json"
#     }
#     print(HOME_DIR)

#     with open(os.path.join(HOME_DIR, "data", "api_input.json"), "r") as f:
#         ml_app_input_json = json.load(f)

#     print(ml_app_input_json)
    
#     response = requests.post(url=endpoint, json=ml_app_input_json, headers=header)

#     # print(response.status_code)
#     # print(json.loads(response.text))
#     # print(type(json.loads(response.text)))

#     response = json.loads(response.text)
#     if isinstance(response, dict):
#         if response.get("result"):
#             print(response['result'])
#         else:
#             print("Bad Request")