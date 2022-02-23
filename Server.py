from flask import Flask, render_template, jsonify

messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/create/', methods=('GET', 'POST'))
def create():
    return render_template('create.html') #render_template --> always use this. We can use this to send data from server.


@app.route('/data/', methods=('GET', 'POST'))
def data():
	return 12 #note: must have strings
@app.route('/message/', methods=('GET','POST'))
def message():
	return render_template('message.html', messages = messages)
@app.route('/test/<int:i>')
def hold():
	return None
if __name__ == '__main__':
    app.run(debug=True)


