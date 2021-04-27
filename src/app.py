from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        time = datetime.now()
        currentTime = time.strftime("%H:%M")
        chat = request.form['user-chat']
        arrayChatUser.append([chat, currentTime])
        return redirect('/')
    else:
        botTime = datetime.now()
        currentBotTime = botTime.strftime("%H:%M")
        return render_template('index.html', arrayChatUser = arrayChatUser, currentBotTime = currentBotTime)

if __name__ == "__main__":
    arrayChatUser = []
    arrayChatBot = []
    app.run(debug=True)
