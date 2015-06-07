#!/usr/bin/python

import argparse
import sys
from pprint import pprint
import twilio.rest
from twilio.rest import TwilioRestClient
import praw

class SubReddit_Postings:
	
	
	def __init__(self, name, phone):
		"""Creates an instance of class SubReddit_Postings
		
		Arguments:
		name -- Name of a SubReddit
		phone -- Phone number of recipient 
		
		"""		
		self.post_text  = '  '  
		self.subreddit_name = name
		self.phone_number = phone
		
	def subreddit_extract_post(self):
		"""Extracts a list of SubReddit posts
		"""	
		
		POST_LIMIT = 0
		user_agent = ("Top Subreddit Posts 1.0 by /u/ruby_relay_bot")
		r = praw.Reddit(user_agent=user_agent)

		
		subreddit_posts_valid = r.get_subreddit(self.subreddit_name, fetch=True)
		if subreddit_posts_valid.has_fetched == True:
			subreddit_posts = r.get_subreddit(self.subreddit_name,).get_top(limit = POST_LIMIT)

			for post in subreddit_posts:
				self.post_text = post.title.lower() 
				self.post_text += "  " + post.url
		else: 

				print "No such subreddit"
		

	def sms_subreddit_post(self):
		"""Sends an SMS of top SubReddit posts
		"""	
		
		try:
			TWILIO_NUMBER = "+18574454093"
			account_sid = "ACbb8840b48cc93d4b05e987d82f7a281a"
			auth_token = "0f065f163e588424cf645b07e3dbc0cb"
		
			client = TwilioRestClient(account_sid, auth_token)
			message = client.messages.create(body=self.post_text,
			to=self.phone_number,
			from_=TWILIO_NUMBER)
			print "SMS Sent"

			pprint(self.post_text)
			
		except twilio.TwilioRestException as e:
			print e

			
if __name__ == "__main__":
	 
	try:
		
			parser = argparse.ArgumentParser(add_help=True)
			parser.add_argument('-subreddit', '--subreddit_title',required=True,action="store",help='Enter a subreddit title')
			parser.add_argument('-phone', '--phone_number', required=True, action="store", type = int, help='Enter a destination phone number')
		
			args = parser.parse_args()
		
			if not args.subreddit_title:
				print "You have to enter a valid  subreddit title"
			elif not args.phone_number:
				print "You have to enter a valid phone number"
			
			subreddit_title = args.subreddit_title
			phone = args.phone_number
		
			sub = SubReddit_Postings(subreddit_title,phone)
			sub.subreddit_extract_post()
			sub.sms_subreddit_post()
		
	except IndexError as ie:
		print "Usage: {} text_filename".format(sys.argv[0])
	
		
		
	

