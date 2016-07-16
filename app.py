from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/login', methods = ['POST'])
def login():
	return render_template('dashboard.html')
	
@app.route("/")
def main():
	return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')