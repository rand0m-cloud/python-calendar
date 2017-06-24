from flask import *
import requests as r
import webbrowser
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()




state = "test1234"

global accessToken
accessToken = ""

@app.route("/")
def root():
    url = oauth["redirect_format"].format(oauth["client_id"],oauth["redirect_uri"],state)
    return redirect(url)
@app.route("/callback")
def callback():

    access_token = r.post("https://www.wunderlist.com/oauth/access_token",data={"code":request.args["code"],"client_id":oauth["client_id"],"client_secret":oauth["client_secret"]})
    
    t = json.loads(access_token.text)
    global accessToken
    accessToken = t["access_token"]
    shutdown_server()
    return """
    <html>
    <body>
    you good. can close
    </body>
    </html>

""",200

def getWunderAccess(p_oauth):
    webbrowser.open("http://localhost:5000")
    global oauth
    oauth = p_oauth
    app.run('0.0.0.0',5000)
    return accessToken

if __name__== "__main__":
    print getWunderAccess()
