from locust import HttpUser, task, between
import json

class ShardUser(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def get_key(self):
        key = "sample_key"
        self.client.get(f"/get?key={key}")
    
    @task(1)
    def set_key(self):
        key="sample_key"
        value="sample_value"
        json_payload = json.dumps({"key":key, "value":value})
        self.client.post("/put", data=json_payload, headers={"Content-Type":"application/json"})