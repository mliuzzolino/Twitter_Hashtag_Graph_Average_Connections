from __future__ import division
from collections import Counter
from datetime import datetime
from dateutil.relativedelta import *
import time

class TimeWindow(object):

	def __init__(self, time_width_mins=1):
		self.time_frame_mins = time_width_mins

		self.running_timestamp_array = []
		self.cutoff_time = None

		self.tweets = []

		self.hashtags = []



		self.hashtag_graph = {}
		


	def update(self, new_tweet):

		# Update timeframe regardless of number of hashtags in tweet
		self.update_timeframe(new_tweet)


		# Update tweets if tweet hashtag number >= 2 and is DISTINCT
		if new_tweet.number_of_hashtags >= 2 and self.check_distinct(new_tweet):
			self.add_tweet(new_tweet)
					
		# Check for removal of tweet
		self.remove_outdated_tweets()
		

		# Calculate running average
		self.running_average()


	def check_distinct(self, new_tweet):

		if len(self.tweets) == 0:
			return True

		for tweet in self.tweets:
			if new_tweet.number_of_hashtags == tweet.number_of_hashtags:
				existing_hashtags = sorted(tweet.hashtags)
				new_hashtags = sorted(new_tweet.hashtags)
				
				if new_hashtags == existing_hashtags:
					return False

		return True
				
				
							

	def add_tweet(self, new_tweet):
		
		self.tweets.append(new_tweet)

		# Update hashtags, unique hashtags array, and hashtag counter
		for hashtag in new_tweet.hashtags:
			self.hashtags.append(hashtag)
			linked_hashtags = set(new_tweet.hashtags) - set([hashtag])

			if hashtag not in self.hashtag_graph:
				self.hashtag_graph[hashtag] = linked_hashtags
			else:
				for linked_hashtag in linked_hashtags:
					self.hashtag_graph[hashtag].add(linked_hashtag)



	def remove_outdated_tweets(self):
		for index, tweet in enumerate(self.tweets):
			if tweet.timestamp <= self.cutoff_time:
				
				# Delete tweet from tweets array within time_window object
				del self.tweets[index]

				# Update hashtags, unique hashtags array, and hashtag counter
				for hashtag in tweet.hashtags:
					self.hashtags.remove(hashtag)
				
				for hashtag in tweet.hashtags:
					
					linked_hashtags = set(tweet.hashtags) - set([hashtag])

					for linked_hashtag in linked_hashtags:		
						if linked_hashtag in self.hashtag_graph[hashtag]:
							self.hashtag_graph[hashtag].remove(linked_hashtag)
				
		

	def update_timeframe(self, tweet):
		self.running_timestamp_array.append(tweet.timestamp)
		newest_timestamp = max(self.running_timestamp_array)
		self.cutoff_time = newest_timestamp+relativedelta(minutes=-self.time_frame_mins)

		#print("Timeframe: {} - {}".format(self.cutoff_time, newest_timestamp))


	def running_average(self):
		total_graph_hashtag_number = len(self.hashtag_graph.keys())
		number_connections = 0
		for values in self.hashtag_graph.values():
			number_connections += len(values)

		self.running_average_connections = number_connections / total_graph_hashtag_number
	
