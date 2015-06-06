from flask import Flask, render_template, request, redirect, url_for,flash,session
from flask.ext.session import Session
from suitor_python import SubReddit_Postings


app = Flask(__name__)
suitor_flask_session = Session


@app.route('/', methods=['GET', 'POST'])
def subreddit_post():
    if request.method == 'POST':
        
		name=request.form['name']
		phone_number = request.form['phone']
		
		subreddit = SubReddit_Postings(name,phone_number)
		subreddit.subreddit_extract_post()
		subreddit.sms_subreddit_post()
		
		flash("SMS successfully sent!!!")
		
		
		return redirect(url_for('subreddit_post'))
	
    else:
		
		return render_template('suitor_flask.html')


if __name__ == '__main__':
	

	app.secret_key = 'super secret key'
	
	app.debug = True
	app.run(host='0.0.0.0', port=5000)