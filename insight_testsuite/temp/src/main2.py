from __future__ import division
import json, sys, os
import numpy as np
from dateutil.parser import parse
from datetime import datetime
from dateutil.relativedelta import *
from modules.hash_tag_graph import HashTagGraph



def main(input_file_path, output_file_path):

	tweets = []
	for line in open(input_file_path, 'r'):
		tweets.append(json.loads(line))


	time_stamps = []
	tweet_log = []
	tweet_dictionary = {}
	hashtag_graph = HashTagGraph(output_file_path)

	for index, tweet in enumerate(tweets):

		# get user_id for dictionary keys 
		try: 
			current_user_id = tweet['id']
		except KeyError:
			continue
		

		# Obtain created_at (timestamp)
		try:
			# Used for creating time frame
			current_time_stamp = parse(tweet['created_at'])
			time_stamps.append(current_time_stamp)
		except KeyError:
			continue

		tweet_log.append((current_user_id, current_time_stamp))
		tweet_dictionary[(current_user_id, current_time_stamp)] = []

		# Determine time window
		
		time_window_oldest = min(time_stamps)
		time_window_newest = max(time_stamps)
		cutoff_time = time_window_newest+relativedelta(minutes=-1)


		current_hashtags = tweet['entities']['hashtags']
		for current_hashtag in current_hashtags:
			current_hashtag_text = current_hashtag['text'].encode('utf-8')
			tweet_dictionary[(current_user_id, current_time_stamp)].append(current_hashtag_text)

		current_hash_tags = tweet_dictionary[(current_user_id, current_time_stamp)]

		hashtag_graph.add_tweet(current_hash_tags)
		hashtag_graph.update_connection_average()

		# Prunes the expired tweets
		for index, time_stamp in enumerate(time_stamps):
			if time_window_oldest < cutoff_time:
				del time_stamps[index]
				#hashtag_graph.remove_tweet(tweet_log[index])



if __name__ == "__main__":
	infile = sys.argv[1]
	outfile = sys.argv[2]
	main(infile, outfile)
