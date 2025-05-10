from flask import Flask, request, jsonify
import requests
import hashlib

app = Flask(__name__)

NUM_SHARDS = 3
API_URL = "http://127.0.0.1"
shards={
    0: {
        'leader':"http://shard0-leader:5001",
        'follower':"http://shard0-follower:6001",
    }, 
    1: {
        'leader':"http://shard1-leader:5002",
        'follower':"http://shard1-follower:6002",
    }, 
    2: {
        'leader':"http://shard2-leader:5003",
        'follower':"http://shard2-follower:6003",
    }, 
}

def get_shard_index(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16) % NUM_SHARDS

@app.route("/put", methods =['POST'])
def route_put():
    print("Recieved PUT request")
    try:
        data = request.json
        key  = data.get("key")
        idx = get_shard_index(key)
        url = f"{shards[idx]['leader']}/put"
        print(url)
        res = requests.post(url, json=data)
        return res.content
    except Exception as error:
        data = request.json
        key  = data.get("key")
        idx = get_shard_index(key)
        url = f"{shards[idx]['leader']}/put"
        return jsonify({'error':str(error)}), 500
    
@app.route("/get", methods =['GET', 'POST'])
def route_get():
    key = request.args.get('key')
    idx = get_shard_index(key)
    try:
        url = f"{shards[idx]['follower']}/get?key={key}"
        res = requests.get(url)
        return res.content, res.status_code
    except Exception as error:
        try:
            res = requests.get(f"{shards[idx]['leader']}/get?key={key}")
            return res.content, res.status_code
        except Exception as error:
            return jsonify({'error':str(error)}), 500


@app.route('/delete', methods=['DELETE'])
def route_delete():
    try:
        key = request.args.get("key")
        idx = get_shard_index(key)
        url = f"{shards[idx]}/delete?key={key}"
        res = requests.delete(url)
        return res.content, res.status_code
    except Exception as error:
        return jsonify({'error':str(error)}), 500


@app.route("/print", methods =['GET'])
def printDict():
    try:
        p_shards = {}
        for idx,shard in enumerate(shards):
            url = f"{shards[idx]['follower']}/print"
            res = requests.get(url)
            p_shards[idx] = (str)(res.content)
        return jsonify(p_shards), 200
    except Exception as error:
        return jsonify({'status':f"Failed: {error}"})
    
if __name__ == '__main__':
    app.run(debug=True, port=5000,  host="0.0.0.0")