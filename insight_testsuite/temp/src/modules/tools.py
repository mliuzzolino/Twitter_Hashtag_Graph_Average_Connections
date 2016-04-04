import json
from tweet import Tweet

def build_tweet_dictionary(input_file_path):
	# Read tweets from input file and builds tweet dictionary
    tweets= []
    for line in open(input_file_path, 'r'):
    	tweet_json = json.loads(line)
    	tweet = Tweet(tweet_json)

    	if tweet.success:
    		tweets.append(tweet)
        else:
        	continue

    return tweets


def generate_graph(tweet_dictionary, time_window, output_file_path):
    for tweet in tweet_dictionary:
        time_window.update(tweet)

        
        with open(output_file_path, "a") as outfile:
            average_connections = "{:.2f}\n".format(time_window.running_average_connections)
            outfile.write(average_connections)
        