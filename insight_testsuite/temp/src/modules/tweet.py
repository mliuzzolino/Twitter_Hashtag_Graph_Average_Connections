from dateutil.parser import parse

class Tweet(object):

	def __init__(self, tweet_json):
		self.tweet_json = tweet_json
		self.number_of_hashtags = 0

		# Cleans tweet and determines if Tweet has acceptable format / information
		if self.clean_tweet_json():
			self.success = True
		else:
			self.success = False

	def __repr__(self):
		representation = "{}".format(self.timestamp) + "\n"
		if self.number_of_hashtags == 0:
			representation += "#None"
		else:
			for hashtag in self.hashtags:
				representation += "#{}\n".format(hashtag)
		return representation

	
	def clean_tweet_json(self):
		""" Obtains the timestamp and hashtags from tweet_json
			If a timestamp is absent then tweet is ignored
		"""
		# Obtain timestamp
		try: 
			self.timestamp = parse(self.tweet_json['created_at'])
		except KeyError:
			return False

		# Obtain hashtags
		self.hashtags = []
		hashtags_json = self.tweet_json['entities']['hashtags']
		for hashtags in hashtags_json:
			self.hashtags.append(hashtags['text'].encode('utf-8'))
			self.number_of_hashtags += 1

		return True


