import math
from func import proc
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def main():
    return 'Hello, this is willywangkaa first Heroku project!'

@app.route('/test')
def test():
    return 'test 12 12'

@app.route('/package')
def package():
    return str(math.pi)

@app.route('/page')
def htmlpage():
    with open('main_page.html', 'r') as f:
        contents = f.read()
    return contents

@app.route('/coop')
def coop():
    return proc()

if __name__ == "__main__":
    app.run()