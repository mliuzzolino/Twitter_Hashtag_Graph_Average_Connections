from __future__ import division
from datetime import datetime
from dateutil.relativedelta import *


class TimeWindow(object):

    def __init__(self, time_width_mins=1):
        """
        Constructs the timewindow, taking the number of minutes desired for the time domain of window.
        """
        self.time_frame_mins = time_width_mins

        # Instantiates timestamp list to keep track of timestamps of tweets within timewindow
        # and sets initial cutoff time to None
        self.running_timestamp_list = []
        self.cutoff_time = None

        # Stores tweets within current time_window of time_width_mins
        self.tweets = []

        # Stores hashtags of tweets within current time_window
        self.hashtags = []

        # Instantiates hashtag_graph and sets the initial running_average to zero
        self.hashtag_graph = {}
        self.running_average_connections = 0
        

    def update(self, new_tweet):
        """
        Main update method.
        Takes new tweet into time_window and updates the timeframe of the window.
        Program first checks if cutoff_time is None (new time_window) or that the tweet's
        timestamp falls within or beyond (not before) the timeframe. If before, ignore the tweet.
        The new tweet is then checked to see if it satifies 
            1. Number of hashtags >= 2
            2. Hashtags of new tweet are a distinct set from other tweets' currently in window
        If above conditions are satisfied, new tweet is added to window and the hashtable graph
        is updated.

        The time_window is then checked to ensure that all current tweets are within the 
        appropriate window of time. If not, the out-of-date tweets are ejected from the time
        window and the hashtag graph is updated to reflect the new tweet-landscape

        Lastly, the running connection average of the hashtag graph is calculated and is
        stored to an output file to 2 decimals of precision. 
        """
        # If new_tweet's timestamp is greater than the cutoff_time
        if self.cutoff_time is None or new_tweet.timestamp >= self.cutoff_time:
        	# Update timeframe regardless of number of hashtags in tweet
        	self.update_timeframe(new_tweet)
        # Else the new tweet is to be ignored due to it pre-"dating" the cutoff time of the window
        else:
        	return

        # Update tweets if tweet hashtag number >= 2 and tweet's set of hashtags is DISTINCT
        if new_tweet.number_of_hashtags >= 2 and self.check_distinct(new_tweet):
            self.add_tweet(new_tweet)
                    
        # Check tweets within time_window and eject any expired tweets
        self.remove_outdated_tweets()

        # Calculate running average
        self.running_average()


    def check_distinct(self, new_tweet):
        """
        Checks if the new tweet's hashtags are distinct from all other tweets' hashtags
        currently within the time_window
        """

        # If the hashtag graph is currently empty, the new tweet will obviously be unique
        if len(self.tweets) == 0:
            return True

        # Else, check each tweet, sort the hashtags, and ensure the new tweet's hashtags are distinct
        for tweet in self.tweets:
            if new_tweet.number_of_hashtags == tweet.number_of_hashtags:
                existing_hashtags = sorted(tweet.hashtags)
                new_hashtags = sorted(new_tweet.hashtags)
                
                # The new tweet's hashtags aren't distinct from the current tweet's hashtags.
                if new_hashtags == existing_hashtags:
                    return False

        # New tweet has distinct set of hashtags. Return true
        return True
                
                
    def add_tweet(self, new_tweet):
        """
        Adds new tweet to time_window object and updates the hashtag graph
        """
        self.tweets.append(new_tweet)

        # Update time_window hashtags and constructs hashtag graph
        for hashtag in new_tweet.hashtags:
            self.hashtags.append(hashtag)
            linked_hashtags = list(set(new_tweet.hashtags) - set([hashtag]))

            # If current hashtag isn't already in the graph, it creates a new node and edges
            if hashtag not in self.hashtag_graph:
                self.hashtag_graph[hashtag] = linked_hashtags
            # Else the existing hashtag node has it's edges updated with new hashtag connections
            else:
                for linked_hashtag in linked_hashtags:
                    self.hashtag_graph[hashtag].append(linked_hashtag)


    def remove_outdated_tweets(self):
        """
        Removes outdated tweets and adjusts the hashtag graph
        """
        for index, tweet in enumerate(self.tweets):
            if tweet.timestamp <= self.cutoff_time:
                
                # Delete tweet from tweets array within time_window object
                del self.tweets[index]

                # Update time_window hashtags 
                for hashtag in tweet.hashtags:
                    self.hashtags.remove(hashtag)
                    
                    # Determine the hashtags within the deleted tweet
                    # that are linked to current hashtag
                    linked_hashtags = set(tweet.hashtags) - set([hashtag])

                    # Remove the appropriate edges from the hashtag graph
                    for linked_hashtag in linked_hashtags:      
                        if linked_hashtag in self.hashtag_graph[hashtag]:
                            self.hashtag_graph[hashtag].remove(linked_hashtag)

                            # Checks if hashtag no longer has any connections. If so, remove from graph
                            if len(self.hashtag_graph[hashtag]) == 0:
                            	del self.hashtag_graph[hashtag]


    def update_timeframe(self, tweet):
        """
        Updates the timeframe window by checking new tweets timestamp.
        The timestamp is appended to the running_timestamp_list that contains
        all valid 60-sec interval timestamps. The newest timestamp can be determined
        by taking the max of this array, and the cuttoff time (lower bound of time_window)
        is then determined by subtracting 60 seconds from the most recent timestamp
        """
        self.running_timestamp_list.append(tweet.timestamp)
        newest_timestamp = max(self.running_timestamp_list)
        self.cutoff_time = newest_timestamp+relativedelta(minutes=-self.time_frame_mins)


    def running_average(self):
        """
        Calculates running average number of connections within hashtag graph
        """
        total_graph_hashtag_number = len(self.hashtag_graph.keys())
        number_connections = 0

        for values in self.hashtag_graph.values():
            number_connections += len(set(values))

        try:
            self.running_average_connections = number_connections / total_graph_hashtag_number    
        except ZeroDivisionError:
            self.running_average_connections = 0

        print(self.running_average_connections)
