from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/hello")
def helloagain():
    return "Hellow from another route"

if __name__ == "__main__":
    app.run()