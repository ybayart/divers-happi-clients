from imports import *

def choice_friend(g_data):
	None

def friends(g_data):
	friends = get_happi("users/{}/friends/".format(g_data['user']['id']))
	if friends.status_code != 200:
		try:
			print(json_formatted(friends.json()))
		except:
			print(red("An error occured (status code {})".format(friends.status_code)))
		return None
	friends = friends.json()['results'][0]['friends']
	print(yellow("{} friends:\n|".format(g_data['user']['username'])), yellow("\n| ").join(sorted(blue(user['username']) for user in friends)), "\n")
