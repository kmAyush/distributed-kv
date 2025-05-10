import time
import threading
import requests
import os

LEADER_URL = os.getenv("LEADER_URL")
MY_PORT = os.getenv("MY_PORT")
SHARD_ID = os.getenv("SHARD_ID")
PROMOTE_URL = f"http://localhost:{MY_PORT}/promote"

def monitor_leader():
    while True:
        try:
            r = requests.get(f"{LEADER_URL}/ping", timeout=1)
    
            if r.status_code != 200:
                raise Exception("{LEADER_URL} not ok")
        except:
            print("[!] Leader ping failed, promoting follower",PROMOTE_URL)
            data = {"SHARD_ID":SHARD_ID}
            requests.post(PROMOTE_URL, json=data)
            break
        time.sleep(10)

if __name__ == "__main__":
    monitor_leader()
            