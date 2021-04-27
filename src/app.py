from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import handleInput
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/bot")
def getBotResponse():
    userInputText = request.args.get('user-chat')
    return handleInput.HandleInput(userInputText)


if __name__ == "__main__":
    app.run(debug=True)
