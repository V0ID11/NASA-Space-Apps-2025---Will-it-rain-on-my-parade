from flask import Flask
import socket 

app = Flask(__name__)

@app.route("/")
def Index():
    return "Start of Website"



if __name__  == '__main__':
    ip = socket.gethostbyname('climate-coders.earth')
    print(ip)
    app.run(host = '127.0.0.1', port = 80, debug = True)
