from flask import Flask, request
import os
import redis

app = Flask(__name__)
redis_host = os.getenv('REDIS_HOST')
redis_port = 6379
redis_password = os.getenv('REDIS_PASSWORD')

def redis_conn():
    return redis.Redis(host=redis_host,
                       port=redis_port,
                       password=redis_password)

@app.route('/get', methods=['GET'])
def get():
    key = request.args.get('key')
    if not key:
        return {'Status': 'Missing key parameter'}, 400
    conn = redis_conn()
    value = conn.get(key)
    if value is None:
        return {'Status': 'Missing key/value pair'}, 400
    else:
        return {'key': key, 'value': value.decode('utf-8')}

@app.route('/put', methods=['POST'])
def put():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    if not key or not value:
        return {'Status': 'Missing key or value parameter'}, 400
    conn = redis_conn()
    conn.set(key, value)
    return {'Status': 'Value set successfully'}, 200

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = redis_conn()
        conn.client_list()
        return {'Status': 'OK'}, 200
    except redis.exceptions.ConnectionError:
        return {'Status': 'ERROR'}, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
