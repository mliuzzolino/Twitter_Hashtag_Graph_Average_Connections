from __future__ import division
import matplotlib.pyplot as plt

class HashTagGraph(object):

	def __init__(self, output_file_path):
		# Stuff	
		self.graph = {}
		self.average_connections = 0
		self.average_history = []
		self.output_file_path = output_file_path

	def add_tweet(self, tweets):
		# Adds key
		for tweet in tweets:
			if tweet not in self.graph.keys():
				self.graph[tweet] = set()
					
			if tweet in self.graph.keys():
				intra_tweet_hashtags = set(tweets[:]) - set([tweet])
				for linked_hashtag in intra_tweet_hashtags:
					self.graph[tweet].add(linked_hashtag)
		

	def update_connection_average(self):
		# Update self.average
		number_of_nodes = len(self.graph.keys())
		total_connections = 0

		for values in self.graph.values():
			total_connections += len(values)

		# Calculate average
		try:
			self.average_connections = total_connections / number_of_nodes
		except ZeroDivisionError:
			return

		# Log average
		self.average_history.append(self.average_connections)

		# Write to output.txt
		self.write_output_to_file()


	def write_output_to_file(self):
		with open(self.output_file_path, "a") as outfile:

			output = str("{0:.2f}".format(self.average_connections)) + "\n"
			outfile.write(output)
				

	def plot_history(self):
		plt.scatter([i for i in range(len(self.average_history))], self.average_history)
		plt.show()