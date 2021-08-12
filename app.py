from flask import Flask
from handlers.dataroutes import configure

app = Flask(__name__)
app.secret_key = "aviwashere"

configure(app)

if __name__ == '__main__':
    app.run()
