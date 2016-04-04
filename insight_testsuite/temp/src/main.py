from __future__ import division
from modules.time_window import TimeWindow
import sys
import modules.tools as tools


def main(input_file_path, output_file_path):

	# Build tweet dictionary
    tweet_dictionary = tools.build_tweet_dictionary(input_file_path)

    # Initialize time window with time-width of 60 seconds
    time_window = TimeWindow(time_width_mins=1)

    # Generate Hashtag Graph
    tools.generate_graph(tweet_dictionary, time_window, output_file_path)
    

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    main(infile, outfile)