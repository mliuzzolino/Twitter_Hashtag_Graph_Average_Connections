import json
from tweet import Tweet


def build_tweet_list(input_file_path):
    """
    Builds tweet list from input_file_path txt file containing txt in json format
    Returns list with each tweet as an element
    """
    tweets= []
    for line in open(input_file_path, 'r'):
        tweet_json = json.loads(line)
        tweet = Tweet(tweet_json)

        # Appends tweet only if 'created_at' tag exists; 
        if tweet.success:
            tweets.append(tweet)
        # otherwise, tweet is ignored
        else:
            continue

    return tweets


def generate_graph(tweet_list, time_window, output_file_path):
    """
    Generates the hashtag graph from the tweet_list as a feed.
    Each new tweet in the feed is fed to the time window in which a 
    "tweet landscape" is constructed over a 60-second window of time. 
    Each new tweet is processed to update the time_window.
    The hashtag graph is only updated when the new tweet contains two or more hashtags
    that are distinct.
    Expired tweets are removed from the time_window and the running average for the 
    number connections within the hashtag graph is calculated and appended to the
    output_file_path text file.
    """
    for tweet in tweet_list:
        time_window.update(tweet)

        with open(output_file_path, "a") as outfile:
            average_connections = "{:.3f}".format(time_window.running_average_connections)
            average_connections = average_connections[:-1] + "\n"
            outfile.write(average_connections)
        