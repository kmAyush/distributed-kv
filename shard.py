import sys
from flask import Flask, request, jsonify
app = Flask(__name__)

kv_store = {}

@app.route("/put", methods =['POST'])
def put():
    data = request.json
    key  = data.get("key")
    value = data.get("value")
    try:
        kv_store[key]=value
        return jsonify({'status':"Successful"}), 200
    except:
        return jsonify({'status':"Failed"})
    
@app.route("/get", methods =['GET', 'POST'])
def get():
    key = request.args.get('key')
    try:
        return jsonify({key,kv_store[key]}), 200
    except:
        return jsonify({'status':"Not found"})
    

@app.route('/delete')
def delete():
    key = request.args.get("key")
    try:
        kv_store.pop(key)
        return jsonify({'status':"Delete successful"}), 200
    except:
        return jsonify({'status':"Key not found"})

@app.route("/print", methods =['GET'])
def printDict():
    try:
        return jsonify(kv_store)
    except:
        return jsonify({'status':"Failed"})
    
if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(port=port, host="0.0.0.0")