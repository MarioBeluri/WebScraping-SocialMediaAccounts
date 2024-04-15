"""
	venv/bin/python3 -m utils.find_handles
"""
import json
import utils.utility as utilityModule

INSTAGRAM = True
YOUTUBE = True
TIKTOK = True
FACEBOOK = True

def union_sets(*args):
    
    union = set().union(*args)
    return union

def get_instagram_usernames(filename, platform):

	"""
	gets instagram usernames from the JSON reports
	"""
	usernames = set()
	
	with open(filename, 'r') as fd:
		records = json.load(fd)
		for record in records:

			if platform == "toofame" or platform == "midman":
				username = record["username"].strip()
				if(len(username) > 0):
					usernames.add(username)

			if platform == "accs_market":
				
				url = record["social_media_address"].strip()
				if len(url) > 0:
					username = url.replace("https://www.instagram.com/", "")
					if "?" in username:
						username = username[0: username.index('?')]

					if '/' in username:
						username = username[0: username.index('/')]
					usernames.add(username)

	return usernames


def get_youtube_channel_urls(filename, platform):
	
	# list of urls of youtube channels
	channels = set()
	
	with open(filename, 'r') as fd:
		records = json.load(fd)
		for record in records:
			if platform == "accs_market":
				if "social_media_address" in record:
					channel = record["social_media_address"]
					if len(channel) > 0 and channel.startswith("https://www.youtube.com"):
						
						if channel.endswith('/videos'):
							channel = channel.replace('/videos', '')
						channels.add(channel)

			if platform == "midman":
				if "channel" in record:
					channel = record["channel"]
					if channel.endswith('/videos'):
						channel = channel.replace('/videos', '')					
					channels.add(channel)

	return channels


def get_tiktok_urls(filename, platform):
	
	# list of urls of youtube channels
	urls = set()
	
	with open(filename, 'r') as fd:
		records = json.load(fd)
		for record in records:
			if platform == "accs_market":
				if "social_media_address" in record:
					channel = record["social_media_address"]
					if len(channel) > 0 and channel.startswith("https://www.tiktok.com"):
						urls.add(channel)

			if platform == "midman":
				if "channel" in record:
					channel = record["channel"]			
					urls.add(channel)

	return urls


def get_facebook_urls(filename, platform):
	
	# list of urls of youtube channels
	urls = set()
	
	with open(filename, 'r') as fd:
		records = json.load(fd)
		for record in records:
			if platform == "accs_market":
				if "social_media_address" in record:
					channel = record["social_media_address"]
					if len(channel) > 0 and "facebook" in channel:
						urls.add(channel)

			if platform == "midman":
				if "channel" in record:
					channel = record["channel"]			
					urls.add(channel)

	return urls


def main():

	timestamp = utilityModule.get_timestamp().split('_')[0]

	if INSTAGRAM:

		u1 = get_instagram_usernames("./data/toofame_2024-02-22_09-47-12.json", "toofame")
		u2 = get_instagram_usernames("./data/toofame_2024-04-04_19-11-23.json", "toofame")
		u3 = get_instagram_usernames("./data/midman_instagram_2024-04-05_16-23-48.json", "midman")
		u4 = get_instagram_usernames("./data/accs_market_instagram_2024-04-04_23-59-59.json", "accs_market")
		u5 = get_instagram_usernames("./data/midman_instagram_2024-04-10_17-32-08.json", "midman")
		union = union_sets(u1, u2, u3, u4, u5)

		with open(f'./handles/instagram_usernames_{timestamp}.txt', 'w+') as fd:
			for item in union:
				fd.write(item+'\n')


	if YOUTUBE:
		u1 = get_youtube_channel_urls("./data/accs_market_youtube_2024-04-05_07-55-13.json", "accs_market")
		u2 = get_youtube_channel_urls("./data/midman_youtube_2024-04-05_16-27-08.json", "midman")
		u3 = get_youtube_channel_urls("./data/midman_youtube_2024-04-10_13-50-40.json", "midman")
		union = union_sets(u1, u2, u3)
		with open(f'./handles/youtube_channels_{timestamp}.txt', 'w+') as fd:
			for item in union:
				fd.write(item+'\n')

	if TIKTOK:
		u1 = get_tiktok_urls("./data/accs_market_tiktok_2024-04-06_12-38-11.json", "accs_market")
		u2 = get_tiktok_urls("./data/midman_tiktok_2024-04-05_16-31-00.json", "midman")
		u3 = get_tiktok_urls("./data/midman_tiktok_2024-04-10_15-14-46.json", "midman")
		union = union_sets(u1, u2, u3)
		with open(f'./handles/tiktok_channels_{timestamp}.txt', 'w+') as fd:
			for item in union:
				fd.write(item+'\n')


	if FACEBOOK:
		u1 = get_facebook_urls("./data/accs_market_facebook_2024-04-06_09-11-26.json", "accs_market")
		u2 = get_facebook_urls("./data/midman_facebook_2024-04-05_16-28-44.json", "midman")
		u3 = get_facebook_urls("./data/midman_facebook_2024-04-10_14-24-32.json", "midman")
		union = union_sets(u1, u2, u3)
		with open(f'./handles/facebook_pages_{timestamp}.txt', 'w+') as fd:
			for item in union:
				fd.write(item+'\n')


if __name__ == "__main__":
	main()









