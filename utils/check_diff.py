
"""	
	identify new twitter handles from the scapred data
	$ venv/bin/python3 -m utils.check_diff 
"""

import json
from urllib.parse import urlparse

fp = open('./handles/twitter_collated_ids.txt', 'r')
twitter_handles = [e.rstrip('\n') for e in fp.readlines()]
fp.close()


fp = open('./data/accs_market_twitter_2024-04-04_19-10-59.json', 'r')
twitter_1 = json.load(fp)
fp.close()

fp = open('./data/midman_twitter_2024-04-05_16-04-41.json', 'r')
twitter_2 = json.load(fp)
fp.close()

fp = open('./data/midman_twitter_2024-04-04_17-36-41.json', 'r')
twitter_3 = json.load(fp)
fp.close()


new_handles = []
for item in twitter_1:
	profile_url = item["social_media_address"]
	if not profile_url == "(the seller has hidden the link)":
		parsed = urlparse(profile_url)
		username = parsed.path.lstrip('/').split('/')[0]
		if username not in twitter_handles:
			new_handles.append(username)


for item in twitter_2:
	username = item["username"]
	if len(username) > 0 and username not in twitter_handles:
		new_handles.append(username)

for item in twitter_3:
	username = item["title"]
	if username not in twitter_handles:
		new_handles.append(username)

with open('./handles/twitter_new_handles.txt', 'w+') as fd:
	for h in new_handles:
		fd.write(h+'\n')




