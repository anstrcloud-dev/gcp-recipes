from flask import Flask, render_template, request, redirect, url_for#from google.cloud import firestore

app = Flask(__name__)#db = firestore.Client()@app.route('/')def hello():
	return "Hello Recipes!"



if __name__ == '__main__':	app.run(host='0.0.0.0', port=8080)