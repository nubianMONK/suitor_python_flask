from flask import Flask, render_template, request, redirect, url_for,flash,session
from flask.ext.session import Session
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from suitor_python import SubReddit_Postings


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
CsrfProtect(app)
suitor_flask_session = Session


class SubRedditForm(Form):

	form_name = StringField('What is the subreddit name?', validators=[Required()])
	form_phone_number = StringField('What is the recipients phone number?', \
	validators=[Required()])

	form_twilio_number = StringField('Your Twilio Tel Number - optional')
	form_account_sid = StringField('Your account_sid - optional')
	form_auth_token = StringField('Your auth_token - optional')
	form_submit = SubmitField('Submit')

@app.errorhandler(403)
def page_forbidden(e):
	return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def subreddit_post():
	form = SubRedditForm()
	if form.validate_on_submit():

		name=form.form_name.data
		phone_number = form.form_phone_number.data

		twilio_number = form.form_twilio_number.data
		account_sid = form.form_account_sid.data
		auth_token = form.form_auth_token.data

		subreddit = SubReddit_Postings(name,phone_number)
		if twilio_number:
			subreddit.twilio_setup(account_sid,auth_token,twilio_number)

		subreddit.subreddit_extract_post()
		valid = subreddit.sms_subreddit_post()
		if valid:
			flash("SMS successfully sent!!!")
		else:
			flash("SMS not sent, error with number or Twilio account !!!")

		return redirect(url_for('subreddit_post'))

	return render_template('suitor_flask.html', form=form)

if __name__ == '__main__':

	app.debug = True
	app.run()
