from __future__ import division
from modules.time_window import TimeWindow
import sys
import modules.tools as tools


def main(input_file_path, output_file_path):
    """
    Main function that takes input and output file paths as inputs
    A tweet feed is constructed from the input file, then a time_window object is created
    both of which are passed to the graph generator that calculates a running average for
    the number of connections within the hashtag graph. These averages are then written
    to an output text file via output_file_path
    """

    # Build tweet dictionary
    tweet_feed = tools.build_tweet_list(input_file_path)

    # Initialize time window with time-width of 60 seconds
    time_window = TimeWindow(time_width_mins=1)

    # Generate Hashtag Graph
    tools.generate_graph(tweet_feed, time_window, output_file_path)


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    main(infile, outfile)