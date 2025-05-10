import requests
import sys
import os

from flask import Flask, request, jsonify
app = Flask(__name__)

kv_store = {}
IS_LEADER = os.getenv("ISLEADER","1") == '1'
FOLLOWERS = os.getenv("FOLLOWERS","").split(",")

@app.route("/put", methods =['POST'])
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
    
@app.route('/replicate', methods=['POST'])
def replicate():
    data = request.json
    key, value = data['key'], data['value']
    kv_store[key] = value
    return jsonify({'status':"Successful"}), 200

@app.route("/get", methods =['GET', 'POST'])
def get():
    key = request.args.get('key')
    try:
        return jsonify({'key':key, 'value':kv_store[key]}), 200
    except:
        return jsonify({'status':"Key not found"})
    

@app.route('/delete')
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
    
if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port, host="0.0.0.0")