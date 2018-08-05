#!/usr/bin/python

import argparse
import sys
from pprint import pprint
from twilio import *
import twilio.rest
from twilio.rest import TwilioRestClient
from twilio.rest import Client
import praw

class SubReddit_Postings:


	def __init__(self, name, phone):
		"""Creates an instance of class SubReddit_Postings

		Arguments:
		name -- Name of a SubReddit
		phone -- Phone number of recipient

		"""
		self.post_text  = '  '
		self.account_sid = ' '
		self.auth_token = ' '
		self.subreddit_name = name
		self.phone_number = phone
		self.twilio_number = None

	def subreddit_extract_post(self):
		"""Extracts a list of SubReddit posts
		"""

		POST_LIMIT = 10
		client_id = ("s5BjxO2YReoiUw")
		client_secret = ("Rz54TgvxHDzgk_6oEz6u_ttqdzk")
		user_agent = ("extract_top_posts:v 1.0 (by /u/nubianmonk)")

		r = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

		print(r.read_only)

		subreddit_posts = r.subreddit(self.subreddit_name,).top(limit = POST_LIMIT)
		print(subreddit_posts)
		if subreddit_posts:

			for post in subreddit_posts:
				print(post)
				self.post_text = post.title.lower()
				self.post_text += "  " + post.url
		else:

				print("No such subreddit")

	def twilio_setup( self,account_sid, auth_token, twilio_number):
		self.account_sid = account_sid
		self.auth_token = auth_token
		self.twilio_number = twilio_number

	def sms_subreddit_post(self):
		"""Sends an SMS of top SubReddit posts
		"""

		if self.twilio_number:
			TWILIO_NUMBER = self.twilio_number
			account_sid = self.account_sid
			auth_token = self.auth_token
		else:
			TWILIO_NUMBER = "+16105802717"
			account_sid = "AC1638cb476ea771863423befa603de505"
			auth_token = "f9ccb83192414ba7f19e5151e6b7fc34"

		client = Client(account_sid, auth_token)
		message = client.messages.create(to=self.phone_number, from_=TWILIO_NUMBER, body=self.post_text)


if __name__ == "__main__":

	try:

			parser = argparse.ArgumentParser(add_help=True)
			parser.add_argument('-subreddit', '--subreddit_title',required=True,action="store",help='Enter a subreddit title')
			parser.add_argument('-phone', '--phone_number', required=True, action="store", type = int, help='Enter a destination phone number')

			args = parser.parse_args()

			if not args.subreddit_title:
				print("You have to enter a valid  subreddit title")
			elif not args.phone_number:
				print("You have to enter a valid phone number")

			subreddit_title = args.subreddit_title
			print(subreddit_title)
			phone = args.phone_number
			print(phone)

			sub = SubReddit_Postings(subreddit_title,phone)
			sub.subreddit_extract_post()
			result=sub.sms_subreddit_post()
			print(result)

	except IndexError as ie:
		print("Usage: {} text_filename".format(sys.argv[0]))
