from flask import Flask, request

app = Flask(__name__)

@app.before_request
def log_request():

    print('--- Incoming Request ---')
    print(f'Method: {request.method}')
    print(f'Path: {request.path}')
    print('Headers:')
    for header, value in request.headers.items():
        print(f'    {header}: {value}')
    print('Body:')
    print(request.get_data(as_text=True))
    print('-----------------------')

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
def catch_all(path):
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
