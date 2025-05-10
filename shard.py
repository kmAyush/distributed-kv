import requests
import sys
import os
import time
import functools
store={}
latencies=[]
start_time=time.time()

from flask import Flask, request, jsonify
app = Flask(__name__)

kv_store = {}
IS_LEADER = os.getenv("IS_LEADER","1") == '1'

FOLLOWERS = os.getenv("FOLLOWERS","").split(",")


def track_latency(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        latency_ms = (time.time()-start)*1000
        latencies.append(latency_ms)
        return result
    return wrapper

@app.route('/replicate', methods=['POST'])
def replicate():
    data = request.json
    key, value = data['key'], data['value']
    kv_store[key] = value
    return jsonify({'status':"Successful"}), 200

@app.route("/put", methods =['POST'])
@track_latency
def put():
    data = request.json
    key  = data.get("key")
    value = data.get("value")

    try:
        kv_store[key]=value
        if IS_LEADER:
            for url in FOLLOWERS:
                try:
                    print("Follower url:",url)
                    requests.post(f"http://{url}/replicate", json=data)
                except Exception as e:
                    print(f"Replication failed to {url}: {e}")
        return jsonify({'status':"Successful"}), 200
    except:
        return jsonify({'status':"Failed"})    


@app.route("/get", methods =['GET', 'POST'])
@track_latency
def get():
    key = request.args.get('key')
    try:
        return jsonify({'key':key, 'value':kv_store[key]}), 200
    except:
        return jsonify({'status':"Key not found"})
    

@app.route('/delete')
@track_latency
def delete():
    key = request.args.get("key")
    try:
        kv_store.pop(key)
        if IS_LEADER:
            for url in FOLLOWERS:
                try:
                    requests.post(f"http://{url}/delete?key={key}")
                except Exception as e:
                    print(f"Replication delete failed to {url}: {e}")
        return jsonify({'status':"Delete successful"}), 200
    except:
        return jsonify({'status':"Key not found"})

@app.route("/print", methods =['GET'])
def printDict():
    try:
        return kv_store
    except:
        return jsonify({'status':"Failed"})
    

@app.route("/metrics")
def metrics():
    avg_latency = sum(latencies)/len(latencies) if latencies else 0
    return jsonify({
        "Avg_latency_ms": round(avg_latency,2),
        "Num_requests_tracked":len(latencies),
        "key_count":len(kv_store),
        "uptime_seconds":int(time.time()-start_time)
    })

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port, host="0.0.0.0")